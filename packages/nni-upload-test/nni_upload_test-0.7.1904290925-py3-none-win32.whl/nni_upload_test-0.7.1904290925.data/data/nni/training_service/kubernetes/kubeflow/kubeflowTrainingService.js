'use strict';
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
Object.defineProperty(exports, "__esModule", { value: true });
const assert = require("assert");
const component = require("../../../common/component");
const cpp = require("child-process-promise");
const fs = require("fs");
const path = require("path");
const containerJobData_1 = require("../../common/containerJobData");
const experimentStartupInfo_1 = require("../../../common/experimentStartupInfo");
const trialConfigMetadataKey_1 = require("../../common/trialConfigMetadataKey");
const utils_1 = require("../../../common/utils");
const kubeflowConfig_1 = require("./kubeflowConfig");
const kubernetesData_1 = require("../kubernetesData");
const kubeflowJobRestServer_1 = require("./kubeflowJobRestServer");
const util_1 = require("../../common/util");
const azureStorageClientUtils_1 = require("../azureStorageClientUtils");
const kubeflowApiClient_1 = require("./kubeflowApiClient");
const kubernetesTrainingService_1 = require("../kubernetesTrainingService");
const kubeflowJobInfoCollector_1 = require("./kubeflowJobInfoCollector");
let KubeflowTrainingService = class KubeflowTrainingService extends kubernetesTrainingService_1.KubernetesTrainingService {
    constructor() {
        super();
        this.kubeflowJobInfoCollector = new kubeflowJobInfoCollector_1.KubeflowJobInfoCollector(this.trialJobsMap);
        this.experimentId = experimentStartupInfo_1.getExperimentId();
        this.nextTrialSequenceId = -1;
        this.log.info('Construct Kubeflow training service.');
    }
    async run() {
        this.log.info('Run Kubeflow training service.');
        this.kubernetesJobRestServer = component.get(kubeflowJobRestServer_1.KubeflowJobRestServer);
        if (!this.kubernetesJobRestServer) {
            throw new Error('kubernetesJobRestServer not initialized!');
        }
        await this.kubernetesJobRestServer.start();
        this.kubernetesJobRestServer.setEnableVersionCheck = this.versionCheck;
        this.log.info(`Kubeflow Training service rest server listening on: ${this.kubernetesJobRestServer.endPoint}`);
        while (!this.stopping) {
            await utils_1.delay(3000);
            await this.kubeflowJobInfoCollector.retrieveTrialStatus(this.kubernetesCRDClient);
            if (this.kubernetesJobRestServer.getErrorMessage) {
                throw new Error(this.kubernetesJobRestServer.getErrorMessage);
                this.stopping = true;
            }
        }
        this.log.info('Kubeflow training service exit.');
    }
    async submitTrialJob(form) {
        if (!this.kubernetesCRDClient) {
            throw new Error('Kubeflow job operator client is undefined');
        }
        if (!this.kubernetesRestServerPort) {
            const restServer = component.get(kubeflowJobRestServer_1.KubeflowJobRestServer);
            this.kubernetesRestServerPort = restServer.clusterRestServerPort;
        }
        const trialJobId = utils_1.uniqueString(5);
        const trialWorkingFolder = path.join(this.CONTAINER_MOUNT_PATH, 'nni', experimentStartupInfo_1.getExperimentId(), trialJobId);
        const kubeflowJobName = `nni-exp-${this.experimentId}-trial-${trialJobId}`.toLowerCase();
        const curTrialSequenceId = this.generateSequenceId();
        const trialLocalTempFolder = path.join(utils_1.getExperimentRootDir(), 'trials-local', trialJobId);
        await this.prepareRunScript(trialLocalTempFolder, trialJobId, trialWorkingFolder, curTrialSequenceId, form);
        const trialJobOutputUrl = await this.uploadCodeFiles(trialJobId, trialLocalTempFolder);
        const trialJobDetail = new kubernetesData_1.KubernetesTrialJobDetail(trialJobId, 'WAITING', Date.now(), trialWorkingFolder, form, kubeflowJobName, curTrialSequenceId, trialJobOutputUrl);
        const kubeflowJobConfig = await this.prepareKubeflowConfig(trialJobId, trialWorkingFolder, kubeflowJobName);
        await this.kubernetesCRDClient.createKubernetesJob(kubeflowJobConfig);
        this.trialJobsMap.set(trialJobId, trialJobDetail);
        return Promise.resolve(trialJobDetail);
    }
    async uploadCodeFiles(trialJobId, trialLocalTempFolder) {
        if (!this.kubeflowClusterConfig) {
            throw new Error('Kubeflow Cluster config is not initialized');
        }
        let trialJobOutputUrl = '';
        assert(!this.kubeflowClusterConfig.storage
            || this.kubeflowClusterConfig.storage === 'azureStorage'
            || this.kubeflowClusterConfig.storage === 'nfs');
        if (this.kubeflowClusterConfig.storage === 'azureStorage') {
            try {
                await azureStorageClientUtils_1.AzureStorageClientUtility.uploadDirectory(this.azureStorageClient, `nni/${experimentStartupInfo_1.getExperimentId()}/${trialJobId}`, this.azureStorageShare, `${trialLocalTempFolder}`);
                trialJobOutputUrl = `https://${this.azureStorageAccountName}.file.core.windows.net/${this.azureStorageShare}/${path.join('nni', experimentStartupInfo_1.getExperimentId(), trialJobId, 'output')}`;
            }
            catch (error) {
                this.log.error(error);
                return Promise.reject(error);
            }
        }
        else if (this.kubeflowClusterConfig.storage === 'nfs' || this.kubeflowClusterConfig.storage === undefined) {
            let nfsKubeflowClusterConfig = this.kubeflowClusterConfig;
            await cpp.exec(`mkdir -p ${this.trialLocalNFSTempFolder}/nni/${experimentStartupInfo_1.getExperimentId()}/${trialJobId}`);
            await cpp.exec(`cp -r ${trialLocalTempFolder}/* ${this.trialLocalNFSTempFolder}/nni/${experimentStartupInfo_1.getExperimentId()}/${trialJobId}/.`);
            const nfsConfig = nfsKubeflowClusterConfig.nfs;
            trialJobOutputUrl = `nfs://${nfsConfig.server}:${path.join(nfsConfig.path, 'nni', experimentStartupInfo_1.getExperimentId(), trialJobId, 'output')}`;
        }
        return Promise.resolve(trialJobOutputUrl);
    }
    async prepareRunScript(trialLocalTempFolder, trialJobId, trialWorkingFolder, curTrialSequenceId, form) {
        if (!this.kubeflowClusterConfig) {
            throw new Error('Kubeflow Cluster config is not initialized');
        }
        let kubeflowTrialConfig;
        if (this.kubeflowClusterConfig.operator === 'tf-operator') {
            kubeflowTrialConfig = this.kubeflowTrialConfig;
        }
        else if (this.kubeflowClusterConfig.operator === 'pytorch-operator') {
            kubeflowTrialConfig = this.kubeflowTrialConfig;
        }
        else {
            throw Error(`operator ${this.kubeflowClusterConfig.operator} is invalid`);
        }
        await cpp.exec(`mkdir -p ${path.dirname(trialLocalTempFolder)}`);
        await cpp.exec(`cp -r ${kubeflowTrialConfig.codeDir} ${trialLocalTempFolder}`);
        const runScriptContent = containerJobData_1.CONTAINER_INSTALL_NNI_SHELL_FORMAT;
        await fs.promises.writeFile(path.join(trialLocalTempFolder, 'install_nni.sh'), runScriptContent, { encoding: 'utf8' });
        await cpp.exec(`mkdir -p ${trialLocalTempFolder}`);
        if (kubeflowTrialConfig.worker) {
            const workerRunScriptContent = await this.generateRunScript('kubeflow', trialJobId, trialWorkingFolder, kubeflowTrialConfig.worker.command, curTrialSequenceId.toString(), 'worker', kubeflowTrialConfig.worker.gpuNum);
            await fs.promises.writeFile(path.join(trialLocalTempFolder, 'run_worker.sh'), workerRunScriptContent, { encoding: 'utf8' });
        }
        if (this.kubeflowClusterConfig.operator === 'tf-operator') {
            let tensorflowTrialConfig = this.kubeflowTrialConfig;
            if (tensorflowTrialConfig.ps) {
                const psRunScriptContent = await this.generateRunScript('kubeflow', trialJobId, trialWorkingFolder, tensorflowTrialConfig.ps.command, curTrialSequenceId.toString(), 'ps', tensorflowTrialConfig.ps.gpuNum);
                await fs.promises.writeFile(path.join(trialLocalTempFolder, 'run_ps.sh'), psRunScriptContent, { encoding: 'utf8' });
            }
        }
        else if (this.kubeflowClusterConfig.operator === 'pytorch-operator') {
            let pytorchTrialConfig = this.kubeflowTrialConfig;
            if (pytorchTrialConfig.master) {
                const masterRunScriptContent = await this.generateRunScript('kubeflow', trialJobId, trialWorkingFolder, pytorchTrialConfig.master.command, curTrialSequenceId.toString(), 'master', pytorchTrialConfig.master.gpuNum);
                await fs.promises.writeFile(path.join(trialLocalTempFolder, 'run_master.sh'), masterRunScriptContent, { encoding: 'utf8' });
            }
        }
        const trialForm = form;
        if (trialForm && trialForm.hyperParameters) {
            await fs.promises.writeFile(path.join(trialLocalTempFolder, utils_1.generateParamFileName(trialForm.hyperParameters)), trialForm.hyperParameters.value, { encoding: 'utf8' });
        }
    }
    async prepareKubeflowConfig(trialJobId, trialWorkingFolder, kubeflowJobName) {
        if (!this.kubeflowClusterConfig) {
            throw new Error('Kubeflow Cluster config is not initialized');
        }
        if (!this.kubeflowTrialConfig) {
            throw new Error('Kubeflow trial config is not initialized');
        }
        let kubeflowTrialConfig;
        if (this.kubeflowClusterConfig.operator === 'tf-operator') {
            kubeflowTrialConfig = this.kubeflowTrialConfig;
        }
        else if (this.kubeflowClusterConfig.operator === 'pytorch-operator') {
            kubeflowTrialConfig = this.kubeflowTrialConfig;
        }
        else {
            throw Error(`operator ${this.kubeflowClusterConfig.operator} is invalid`);
        }
        const workerPodResources = {};
        if (kubeflowTrialConfig.worker) {
            workerPodResources.requests = this.generatePodResource(kubeflowTrialConfig.worker.memoryMB, kubeflowTrialConfig.worker.cpuNum, kubeflowTrialConfig.worker.gpuNum);
        }
        workerPodResources.limits = Object.assign({}, workerPodResources.requests);
        let nonWorkerResources = {};
        if (this.kubeflowClusterConfig.operator === 'tf-operator') {
            let tensorflowTrialConfig = this.kubeflowTrialConfig;
            if (tensorflowTrialConfig.ps) {
                nonWorkerResources.requests = this.generatePodResource(tensorflowTrialConfig.ps.memoryMB, tensorflowTrialConfig.ps.cpuNum, tensorflowTrialConfig.ps.gpuNum);
                nonWorkerResources.limits = Object.assign({}, nonWorkerResources.requests);
            }
        }
        else if (this.kubeflowClusterConfig.operator === 'pytorch-operator') {
            let pyTorchTrialConfig = this.kubeflowTrialConfig;
            nonWorkerResources.requests = this.generatePodResource(pyTorchTrialConfig.master.memoryMB, pyTorchTrialConfig.master.cpuNum, pyTorchTrialConfig.master.gpuNum);
            nonWorkerResources.limits = Object.assign({}, nonWorkerResources.requests);
        }
        const kubeflowJobConfig = this.generateKubeflowJobConfig(trialJobId, trialWorkingFolder, kubeflowJobName, workerPodResources, nonWorkerResources);
        return Promise.resolve(kubeflowJobConfig);
    }
    async setClusterMetadata(key, value) {
        switch (key) {
            case trialConfigMetadataKey_1.TrialConfigMetadataKey.NNI_MANAGER_IP:
                this.nniManagerIpConfig = JSON.parse(value);
                break;
            case trialConfigMetadataKey_1.TrialConfigMetadataKey.KUBEFLOW_CLUSTER_CONFIG:
                let kubeflowClusterJsonObject = JSON.parse(value);
                this.kubeflowClusterConfig = kubeflowConfig_1.KubeflowClusterConfigFactory.generateKubeflowClusterConfig(kubeflowClusterJsonObject);
                if (this.kubeflowClusterConfig.storageType === 'azureStorage') {
                    let azureKubeflowClusterConfig = this.kubeflowClusterConfig;
                    this.azureStorageAccountName = azureKubeflowClusterConfig.azureStorage.accountName;
                    this.azureStorageShare = azureKubeflowClusterConfig.azureStorage.azureShare;
                    await this.createAzureStorage(azureKubeflowClusterConfig.keyVault.vaultName, azureKubeflowClusterConfig.keyVault.name, azureKubeflowClusterConfig.azureStorage.accountName, azureKubeflowClusterConfig.azureStorage.azureShare);
                }
                else if (this.kubeflowClusterConfig.storageType === 'nfs') {
                    let nfsKubeflowClusterConfig = this.kubeflowClusterConfig;
                    await this.createNFSStorage(nfsKubeflowClusterConfig.nfs.server, nfsKubeflowClusterConfig.nfs.path);
                }
                this.kubernetesCRDClient = kubeflowApiClient_1.KubeflowOperatorClient.generateOperatorClient(this.kubeflowClusterConfig.operator, this.kubeflowClusterConfig.apiVersion);
                break;
            case trialConfigMetadataKey_1.TrialConfigMetadataKey.TRIAL_CONFIG:
                if (!this.kubeflowClusterConfig) {
                    this.log.error('kubeflow cluster config is not initialized');
                    return Promise.reject(new Error('kubeflow cluster config is not initialized'));
                }
                assert(this.kubeflowClusterConfig !== undefined);
                let kubeflowTrialJsonObjsect = JSON.parse(value);
                this.kubeflowTrialConfig = kubeflowConfig_1.KubeflowTrialConfigFactory.generateKubeflowTrialConfig(kubeflowTrialJsonObjsect, this.kubeflowClusterConfig.operator);
                try {
                    await util_1.validateCodeDir(this.kubeflowTrialConfig.codeDir);
                }
                catch (error) {
                    this.log.error(error);
                    return Promise.reject(new Error(error));
                }
                break;
            case trialConfigMetadataKey_1.TrialConfigMetadataKey.VERSION_CHECK:
                this.versionCheck = (value === 'true' || value === 'True');
                break;
            case trialConfigMetadataKey_1.TrialConfigMetadataKey.LOG_COLLECTION:
                this.logCollection = value;
                break;
            default:
                break;
        }
        return Promise.resolve();
    }
    generateKubeflowJobConfig(trialJobId, trialWorkingFolder, kubeflowJobName, workerPodResources, nonWorkerPodResources) {
        if (!this.kubeflowClusterConfig) {
            throw new Error('Kubeflow Cluster config is not initialized');
        }
        if (!this.kubeflowTrialConfig) {
            throw new Error('Kubeflow trial config is not initialized');
        }
        if (!this.kubernetesCRDClient) {
            throw new Error('Kubeflow operator client is not initialized');
        }
        const replicaSpecsObj = {};
        let replicaSpecsObjMap = new Map();
        if (this.kubeflowTrialConfig.operatorType === 'tf-operator') {
            let tensorflowTrialConfig = this.kubeflowTrialConfig;
            replicaSpecsObj.Worker = this.generateReplicaConfig(trialWorkingFolder, tensorflowTrialConfig.worker.replicas, tensorflowTrialConfig.worker.image, 'run_worker.sh', workerPodResources);
            if (tensorflowTrialConfig.ps) {
                replicaSpecsObj.Ps = this.generateReplicaConfig(trialWorkingFolder, tensorflowTrialConfig.ps.replicas, tensorflowTrialConfig.ps.image, 'run_ps.sh', nonWorkerPodResources);
            }
            replicaSpecsObjMap.set(this.kubernetesCRDClient.jobKind, { 'tfReplicaSpecs': replicaSpecsObj });
        }
        else if (this.kubeflowTrialConfig.operatorType === 'pytorch-operator') {
            let pytorchTrialConfig = this.kubeflowTrialConfig;
            if (pytorchTrialConfig.worker) {
                replicaSpecsObj.Worker = this.generateReplicaConfig(trialWorkingFolder, pytorchTrialConfig.worker.replicas, pytorchTrialConfig.worker.image, 'run_worker.sh', workerPodResources);
            }
            replicaSpecsObj.Master = this.generateReplicaConfig(trialWorkingFolder, pytorchTrialConfig.master.replicas, pytorchTrialConfig.master.image, 'run_master.sh', nonWorkerPodResources);
            replicaSpecsObjMap.set(this.kubernetesCRDClient.jobKind, { 'pytorchReplicaSpecs': replicaSpecsObj });
        }
        return {
            apiVersion: `kubeflow.org/${this.kubernetesCRDClient.apiVersion}`,
            kind: this.kubernetesCRDClient.jobKind,
            metadata: {
                name: kubeflowJobName,
                namespace: 'default',
                labels: {
                    app: this.NNI_KUBERNETES_TRIAL_LABEL,
                    expId: experimentStartupInfo_1.getExperimentId(),
                    trialId: trialJobId
                }
            },
            spec: replicaSpecsObjMap.get(this.kubernetesCRDClient.jobKind)
        };
    }
    generateReplicaConfig(trialWorkingFolder, replicaNumber, replicaImage, runScriptFile, podResources) {
        if (!this.kubeflowClusterConfig) {
            throw new Error('Kubeflow Cluster config is not initialized');
        }
        if (!this.kubeflowTrialConfig) {
            throw new Error('Kubeflow trial config is not initialized');
        }
        if (!this.kubernetesCRDClient) {
            throw new Error('Kubeflow operator client is not initialized');
        }
        let volumeSpecMap = new Map();
        if (this.kubeflowClusterConfig.storageType === 'azureStorage') {
            volumeSpecMap.set('nniVolumes', [
                {
                    name: 'nni-vol',
                    azureFile: {
                        secretName: `${this.azureStorageSecretName}`,
                        shareName: `${this.azureStorageShare}`,
                        readonly: false
                    }
                }
            ]);
        }
        else {
            let nfsKubeflowClusterConfig = this.kubeflowClusterConfig;
            volumeSpecMap.set('nniVolumes', [
                {
                    name: 'nni-vol',
                    nfs: {
                        server: `${nfsKubeflowClusterConfig.nfs.server}`,
                        path: `${nfsKubeflowClusterConfig.nfs.path}`
                    }
                }
            ]);
        }
        return {
            replicas: replicaNumber,
            template: {
                metadata: {
                    creationTimestamp: null
                },
                spec: {
                    containers: [
                        {
                            name: this.kubernetesCRDClient.containerName,
                            image: replicaImage,
                            args: ["sh", `${path.join(trialWorkingFolder, runScriptFile)}`],
                            volumeMounts: [
                                {
                                    name: 'nni-vol',
                                    mountPath: this.CONTAINER_MOUNT_PATH
                                }
                            ],
                            resources: podResources
                        }
                    ],
                    restartPolicy: 'ExitCode',
                    volumes: volumeSpecMap.get('nniVolumes')
                }
            }
        };
    }
};
KubeflowTrainingService = __decorate([
    component.Singleton,
    __metadata("design:paramtypes", [])
], KubeflowTrainingService);
exports.KubeflowTrainingService = KubeflowTrainingService;
