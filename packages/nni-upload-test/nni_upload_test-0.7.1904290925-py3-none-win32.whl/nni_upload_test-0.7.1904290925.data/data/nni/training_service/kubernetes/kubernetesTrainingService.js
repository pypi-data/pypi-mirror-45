'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const cpp = require("child-process-promise");
const path = require("path");
const events_1 = require("events");
const experimentStartupInfo_1 = require("../../common/experimentStartupInfo");
const log_1 = require("../../common/log");
const utils_1 = require("../../common/utils");
const kubernetesData_1 = require("./kubernetesData");
const kubernetesApiClient_1 = require("./kubernetesApiClient");
const azureStorageClientUtils_1 = require("./azureStorageClientUtils");
const typescript_string_operations_1 = require("typescript-string-operations");
var azure = require('azure-storage');
var base64 = require('js-base64').Base64;
class KubernetesTrainingService {
    constructor() {
        this.NNI_KUBERNETES_TRIAL_LABEL = 'nni-kubernetes-trial';
        this.stopping = false;
        this.versionCheck = true;
        this.log = log_1.getLogger();
        this.metricsEmitter = new events_1.EventEmitter();
        this.trialJobsMap = new Map();
        this.trialLocalNFSTempFolder = path.join(utils_1.getExperimentRootDir(), 'trials-nfs-tmp');
        this.experimentId = experimentStartupInfo_1.getExperimentId();
        this.nextTrialSequenceId = -1;
        this.CONTAINER_MOUNT_PATH = '/tmp/mount';
        this.genericK8sClient = new kubernetesApiClient_1.GeneralK8sClient();
        this.logCollection = 'none';
    }
    generatePodResource(memory, cpuNum, gpuNum) {
        return {
            'memory': `${memory}Mi`,
            'cpu': `${cpuNum}`,
            'nvidia.com/gpu': `${gpuNum}`
        };
    }
    async listTrialJobs() {
        const jobs = [];
        for (const [key, value] of this.trialJobsMap) {
            if (value.form.jobType === 'TRIAL') {
                jobs.push(await this.getTrialJob(key));
            }
        }
        ;
        return Promise.resolve(jobs);
    }
    async getTrialJob(trialJobId) {
        const kubernetesTrialJob = this.trialJobsMap.get(trialJobId);
        if (!kubernetesTrialJob) {
            return Promise.reject(`trial job ${trialJobId} not found`);
        }
        return Promise.resolve(kubernetesTrialJob);
    }
    addTrialJobMetricListener(listener) {
        this.metricsEmitter.on('metric', listener);
    }
    removeTrialJobMetricListener(listener) {
        this.metricsEmitter.off('metric', listener);
    }
    get isMultiPhaseJobSupported() {
        return false;
    }
    getClusterMetadata(key) {
        return Promise.resolve('');
    }
    get MetricsEmitter() {
        return this.metricsEmitter;
    }
    generateSequenceId() {
        if (this.nextTrialSequenceId === -1) {
            this.nextTrialSequenceId = experimentStartupInfo_1.getInitTrialSequenceId();
        }
        return this.nextTrialSequenceId++;
    }
    async createAzureStorage(vaultName, valutKeyName, accountName, azureShare) {
        try {
            const result = await cpp.exec(`az keyvault secret show --name ${valutKeyName} --vault-name ${vaultName}`);
            if (result.stderr) {
                const errorMessage = result.stderr;
                this.log.error(errorMessage);
                return Promise.reject(errorMessage);
            }
            const storageAccountKey = JSON.parse(result.stdout).value;
            this.azureStorageClient = azure.createFileService(this.azureStorageAccountName, storageAccountKey);
            await azureStorageClientUtils_1.AzureStorageClientUtility.createShare(this.azureStorageClient, this.azureStorageShare);
            this.azureStorageSecretName = 'nni-secret-' + utils_1.uniqueString(8).toLowerCase();
            await this.genericK8sClient.createSecret({
                apiVersion: 'v1',
                kind: 'Secret',
                metadata: {
                    name: this.azureStorageSecretName,
                    namespace: 'default',
                    labels: {
                        app: this.NNI_KUBERNETES_TRIAL_LABEL,
                        expId: experimentStartupInfo_1.getExperimentId()
                    }
                },
                type: 'Opaque',
                data: {
                    azurestorageaccountname: base64.encode(this.azureStorageAccountName),
                    azurestorageaccountkey: base64.encode(storageAccountKey)
                }
            });
        }
        catch (error) {
            this.log.error(error);
            return Promise.reject(error);
        }
        return Promise.resolve();
    }
    async generateRunScript(platform, trialJobId, trialWorkingFolder, command, trialSequenceId, roleName, gpuNum) {
        let nvidia_script = '';
        if (gpuNum === 0) {
            nvidia_script = `export CUDA_VISIBLE_DEVICES='0'`;
        }
        const nniManagerIp = this.nniManagerIpConfig ? this.nniManagerIpConfig.nniManagerIp : utils_1.getIPV4Address();
        const version = this.versionCheck ? await utils_1.getVersion() : '';
        const runScript = typescript_string_operations_1.String.Format(kubernetesData_1.KubernetesScriptFormat, platform, trialJobId, path.join(trialWorkingFolder, 'output', `${roleName}_output`), trialJobId, experimentStartupInfo_1.getExperimentId(), trialWorkingFolder, trialSequenceId, nvidia_script, command, nniManagerIp, this.kubernetesRestServerPort, version, this.logCollection);
        return Promise.resolve(runScript);
    }
    async createNFSStorage(nfsServer, nfsPath) {
        await cpp.exec(`mkdir -p ${this.trialLocalNFSTempFolder}`);
        try {
            await cpp.exec(`sudo mount ${nfsServer}:${nfsPath} ${this.trialLocalNFSTempFolder}`);
        }
        catch (error) {
            const mountError = `Mount NFS ${nfsServer}:${nfsPath} to ${this.trialLocalNFSTempFolder} failed, error is ${error}`;
            this.log.error(mountError);
            return Promise.reject(mountError);
        }
        return Promise.resolve();
    }
    async cancelTrialJob(trialJobId, isEarlyStopped = false) {
        const trialJobDetail = this.trialJobsMap.get(trialJobId);
        if (!trialJobDetail) {
            const errorMessage = `CancelTrialJob: trial job id ${trialJobId} not found`;
            this.log.error(errorMessage);
            return Promise.reject(errorMessage);
        }
        if (!this.kubernetesCRDClient) {
            const errorMessage = `CancelTrialJob: trial job id ${trialJobId} failed because operatorClient is undefined`;
            this.log.error(errorMessage);
            return Promise.reject(errorMessage);
        }
        try {
            await this.kubernetesCRDClient.deleteKubernetesJob(new Map([
                ['app', this.NNI_KUBERNETES_TRIAL_LABEL],
                ['expId', experimentStartupInfo_1.getExperimentId()],
                ['trialId', trialJobId]
            ]));
        }
        catch (err) {
            const errorMessage = `Delete trial ${trialJobId} failed: ${err}`;
            this.log.error(errorMessage);
            return Promise.reject(errorMessage);
        }
        trialJobDetail.endTime = Date.now();
        trialJobDetail.status = utils_1.getJobCancelStatus(isEarlyStopped);
        return Promise.resolve();
    }
    async cleanUp() {
        this.stopping = true;
        for (let [trialJobId, kubernetesTrialJob] of this.trialJobsMap) {
            if (['RUNNING', 'WAITING', 'UNKNOWN'].includes(kubernetesTrialJob.status)) {
                try {
                    await this.cancelTrialJob(trialJobId);
                }
                catch (error) { }
                kubernetesTrialJob.status = 'SYS_CANCELED';
            }
        }
        try {
            if (this.kubernetesCRDClient) {
                await this.kubernetesCRDClient.deleteKubernetesJob(new Map([
                    ['app', this.NNI_KUBERNETES_TRIAL_LABEL],
                    ['expId', experimentStartupInfo_1.getExperimentId()]
                ]));
            }
        }
        catch (error) {
            this.log.error(`Delete kubernetes job with label: app=${this.NNI_KUBERNETES_TRIAL_LABEL},expId=${experimentStartupInfo_1.getExperimentId()} failed, error is ${error}`);
        }
        try {
            await cpp.exec(`sudo umount ${this.trialLocalNFSTempFolder}`);
        }
        catch (error) {
            this.log.error(`Unmount ${this.trialLocalNFSTempFolder} failed, error is ${error}`);
        }
        if (!this.kubernetesJobRestServer) {
            throw new Error('kubernetesJobRestServer not initialized!');
        }
        try {
            await this.kubernetesJobRestServer.stop();
            this.log.info('Kubernetes Training service rest server stopped successfully.');
        }
        catch (error) {
            this.log.error(`Kubernetes Training service rest server stopped failed, error: ${error.message}`);
            Promise.reject(error);
        }
        return Promise.resolve();
    }
}
exports.KubernetesTrainingService = KubernetesTrainingService;
