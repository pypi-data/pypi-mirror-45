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
const component = require("../../../common/component");
const cpp = require("child-process-promise");
const fs = require("fs");
const path = require("path");
const containerJobData_1 = require("../../common/containerJobData");
const experimentStartupInfo_1 = require("../../../common/experimentStartupInfo");
const trialConfigMetadataKey_1 = require("../../common/trialConfigMetadataKey");
const utils_1 = require("../../../common/utils");
const kubernetesData_1 = require("../kubernetesData");
const util_1 = require("../../common/util");
const azureStorageClientUtils_1 = require("../azureStorageClientUtils");
const kubernetesTrainingService_1 = require("../kubernetesTrainingService");
const frameworkcontrollerConfig_1 = require("./frameworkcontrollerConfig");
const frameworkcontrollerJobRestServer_1 = require("./frameworkcontrollerJobRestServer");
const frameworkcontrollerApiClient_1 = require("./frameworkcontrollerApiClient");
const frameworkcontrollerJobInfoCollector_1 = require("./frameworkcontrollerJobInfoCollector");
let FrameworkControllerTrainingService = class FrameworkControllerTrainingService extends kubernetesTrainingService_1.KubernetesTrainingService {
    constructor() {
        super();
        this.fcContainerPortMap = new Map();
        this.fcJobInfoCollector = new frameworkcontrollerJobInfoCollector_1.FrameworkControllerJobInfoCollector(this.trialJobsMap);
        this.experimentId = experimentStartupInfo_1.getExperimentId();
        this.nextTrialSequenceId = -1;
    }
    async run() {
        this.kubernetesJobRestServer = component.get(frameworkcontrollerJobRestServer_1.FrameworkControllerJobRestServer);
        if (!this.kubernetesJobRestServer) {
            throw new Error('kubernetesJobRestServer not initialized!');
        }
        await this.kubernetesJobRestServer.start();
        this.kubernetesJobRestServer.setEnableVersionCheck = this.versionCheck;
        this.log.info(`frameworkcontroller Training service rest server listening on: ${this.kubernetesJobRestServer.endPoint}`);
        while (!this.stopping) {
            await utils_1.delay(3000);
            await this.fcJobInfoCollector.retrieveTrialStatus(this.kubernetesCRDClient);
            if (this.kubernetesJobRestServer.getErrorMessage) {
                throw new Error(this.kubernetesJobRestServer.getErrorMessage);
                this.stopping = true;
            }
        }
    }
    async submitTrialJob(form) {
        if (!this.fcClusterConfig) {
            throw new Error('frameworkcontrollerClusterConfig is not initialized');
        }
        if (!this.kubernetesCRDClient) {
            throw new Error('kubernetesCRDClient is undefined');
        }
        if (!this.kubernetesRestServerPort) {
            const restServer = component.get(frameworkcontrollerJobRestServer_1.FrameworkControllerJobRestServer);
            this.kubernetesRestServerPort = restServer.clusterRestServerPort;
        }
        const trialJobId = utils_1.uniqueString(5);
        const curTrialSequenceId = this.generateSequenceId();
        const trialWorkingFolder = path.join(this.CONTAINER_MOUNT_PATH, 'nni', experimentStartupInfo_1.getExperimentId(), trialJobId);
        const trialLocalTempFolder = path.join(utils_1.getExperimentRootDir(), 'trials-local', trialJobId);
        const frameworkcontrollerJobName = `nniexp${this.experimentId}trial${trialJobId}`.toLowerCase();
        this.generateContainerPort();
        await this.prepareRunScript(trialLocalTempFolder, curTrialSequenceId, trialJobId, trialWorkingFolder, form);
        let trialJobOutputUrl = await this.uploadCodeFiles(trialJobId, trialLocalTempFolder);
        const trialJobDetail = new kubernetesData_1.KubernetesTrialJobDetail(trialJobId, 'WAITING', Date.now(), trialWorkingFolder, form, frameworkcontrollerJobName, curTrialSequenceId, trialJobOutputUrl);
        this.trialJobsMap.set(trialJobId, trialJobDetail);
        const frameworkcontrollerJobConfig = await this.prepareFrameworkControllerConfig(trialJobId, trialWorkingFolder, frameworkcontrollerJobName);
        await this.kubernetesCRDClient.createKubernetesJob(frameworkcontrollerJobConfig);
        this.trialJobsMap.set(trialJobId, trialJobDetail);
        return Promise.resolve(trialJobDetail);
    }
    async uploadCodeFiles(trialJobId, trialLocalTempFolder) {
        if (!this.fcClusterConfig) {
            throw new Error('Kubeflow Cluster config is not initialized');
        }
        let trialJobOutputUrl = '';
        if (this.fcClusterConfig.storageType === 'azureStorage') {
            try {
                await azureStorageClientUtils_1.AzureStorageClientUtility.uploadDirectory(this.azureStorageClient, `nni/${experimentStartupInfo_1.getExperimentId()}/${trialJobId}`, this.azureStorageShare, `${trialLocalTempFolder}`);
                trialJobOutputUrl = `https://${this.azureStorageAccountName}.file.core.windows.net/${this.azureStorageShare}/${path.join('nni', experimentStartupInfo_1.getExperimentId(), trialJobId, 'output')}`;
            }
            catch (error) {
                this.log.error(error);
                return Promise.reject(error);
            }
        }
        else if (this.fcClusterConfig.storageType === 'nfs') {
            let nfsFrameworkControllerClusterConfig = this.fcClusterConfig;
            await cpp.exec(`mkdir -p ${this.trialLocalNFSTempFolder}/nni/${experimentStartupInfo_1.getExperimentId()}/${trialJobId}`);
            await cpp.exec(`cp -r ${trialLocalTempFolder}/* ${this.trialLocalNFSTempFolder}/nni/${experimentStartupInfo_1.getExperimentId()}/${trialJobId}/.`);
            const nfsConfig = nfsFrameworkControllerClusterConfig.nfs;
            trialJobOutputUrl = `nfs://${nfsConfig.server}:${path.join(nfsConfig.path, 'nni', experimentStartupInfo_1.getExperimentId(), trialJobId, 'output')}`;
        }
        return Promise.resolve(trialJobOutputUrl);
    }
    generateCommandScript(command) {
        let portScript = '';
        if (!this.fcTrialConfig) {
            throw new Error('frameworkcontroller trial config is not initialized');
        }
        for (let taskRole of this.fcTrialConfig.taskRoles) {
            portScript += `FB_${taskRole.name.toUpperCase()}_PORT=${this.fcContainerPortMap.get(taskRole.name)} `;
        }
        return `${portScript} . /mnt/frameworkbarrier/injector.sh && ${command}`;
    }
    async prepareRunScript(trialLocalTempFolder, curTrialSequenceId, trialJobId, trialWorkingFolder, form) {
        if (!this.fcTrialConfig) {
            throw new Error('frameworkcontroller trial config is not initialized');
        }
        await cpp.exec(`mkdir -p ${path.dirname(trialLocalTempFolder)}`);
        await cpp.exec(`cp -r ${this.fcTrialConfig.codeDir} ${trialLocalTempFolder}`);
        const runScriptContent = containerJobData_1.CONTAINER_INSTALL_NNI_SHELL_FORMAT;
        await fs.promises.writeFile(path.join(trialLocalTempFolder, 'install_nni.sh'), runScriptContent, { encoding: 'utf8' });
        await cpp.exec(`mkdir -p ${trialLocalTempFolder}`);
        for (let taskRole of this.fcTrialConfig.taskRoles) {
            const runScriptContent = await this.generateRunScript('frameworkcontroller', trialJobId, trialWorkingFolder, this.generateCommandScript(taskRole.command), curTrialSequenceId.toString(), taskRole.name, taskRole.gpuNum);
            await fs.promises.writeFile(path.join(trialLocalTempFolder, `run_${taskRole.name}.sh`), runScriptContent, { encoding: 'utf8' });
        }
        const trialForm = form;
        if (trialForm && trialForm.hyperParameters) {
            await fs.promises.writeFile(path.join(trialLocalTempFolder, utils_1.generateParamFileName(trialForm.hyperParameters)), trialForm.hyperParameters.value, { encoding: 'utf8' });
        }
    }
    async prepareFrameworkControllerConfig(trialJobId, trialWorkingFolder, frameworkcontrollerJobName) {
        if (!this.fcTrialConfig) {
            throw new Error('frameworkcontroller trial config is not initialized');
        }
        const podResources = [];
        for (let taskRole of this.fcTrialConfig.taskRoles) {
            let resource = {};
            resource.requests = this.generatePodResource(taskRole.memoryMB, taskRole.cpuNum, taskRole.gpuNum);
            resource.limits = Object.assign({}, resource.requests);
            podResources.push(resource);
        }
        const frameworkcontrollerJobConfig = this.generateFrameworkControllerJobConfig(trialJobId, trialWorkingFolder, frameworkcontrollerJobName, podResources);
        return Promise.resolve(frameworkcontrollerJobConfig);
    }
    async setClusterMetadata(key, value) {
        switch (key) {
            case trialConfigMetadataKey_1.TrialConfigMetadataKey.NNI_MANAGER_IP:
                this.nniManagerIpConfig = JSON.parse(value);
                break;
            case trialConfigMetadataKey_1.TrialConfigMetadataKey.FRAMEWORKCONTROLLER_CLUSTER_CONFIG:
                let frameworkcontrollerClusterJsonObject = JSON.parse(value);
                this.fcClusterConfig = frameworkcontrollerConfig_1.FrameworkControllerClusterConfigFactory.generateFrameworkControllerClusterConfig(frameworkcontrollerClusterJsonObject);
                if (this.fcClusterConfig.storageType === 'azureStorage') {
                    let azureFrameworkControllerClusterConfig = this.fcClusterConfig;
                    this.azureStorageAccountName = azureFrameworkControllerClusterConfig.azureStorage.accountName;
                    this.azureStorageShare = azureFrameworkControllerClusterConfig.azureStorage.azureShare;
                    await this.createAzureStorage(azureFrameworkControllerClusterConfig.keyVault.vaultName, azureFrameworkControllerClusterConfig.keyVault.name, azureFrameworkControllerClusterConfig.azureStorage.accountName, azureFrameworkControllerClusterConfig.azureStorage.azureShare);
                }
                else if (this.fcClusterConfig.storageType === 'nfs') {
                    let nfsFrameworkControllerClusterConfig = this.fcClusterConfig;
                    await this.createNFSStorage(nfsFrameworkControllerClusterConfig.nfs.server, nfsFrameworkControllerClusterConfig.nfs.path);
                }
                this.kubernetesCRDClient = frameworkcontrollerApiClient_1.FrameworkControllerClient.generateFrameworkControllerClient();
                break;
            case trialConfigMetadataKey_1.TrialConfigMetadataKey.TRIAL_CONFIG:
                let frameworkcontrollerTrialJsonObjsect = JSON.parse(value);
                this.fcTrialConfig = new frameworkcontrollerConfig_1.FrameworkControllerTrialConfig(frameworkcontrollerTrialJsonObjsect.codeDir, frameworkcontrollerTrialJsonObjsect.taskRoles);
                try {
                    await util_1.validateCodeDir(this.fcTrialConfig.codeDir);
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
    generateContainerPort() {
        if (!this.fcTrialConfig) {
            throw new Error('frameworkcontroller trial config is not initialized');
        }
        let port = 4000;
        for (let index in this.fcTrialConfig.taskRoles) {
            this.fcContainerPortMap.set(this.fcTrialConfig.taskRoles[index].name, port);
            port += 1;
        }
    }
    generateFrameworkControllerJobConfig(trialJobId, trialWorkingFolder, frameworkcontrollerJobName, podResources) {
        if (!this.fcClusterConfig) {
            throw new Error('frameworkcontroller Cluster config is not initialized');
        }
        if (!this.fcTrialConfig) {
            throw new Error('frameworkcontroller trial config is not initialized');
        }
        let taskRoles = [];
        for (let index in this.fcTrialConfig.taskRoles) {
            let containerPort = this.fcContainerPortMap.get(this.fcTrialConfig.taskRoles[index].name);
            if (!containerPort) {
                throw new Error('Container port is not initialized');
            }
            let taskRole = this.generateTaskRoleConfig(trialWorkingFolder, this.fcTrialConfig.taskRoles[index].image, `run_${this.fcTrialConfig.taskRoles[index].name}.sh`, podResources[index], containerPort);
            taskRoles.push({
                name: this.fcTrialConfig.taskRoles[index].name,
                taskNumber: this.fcTrialConfig.taskRoles[index].taskNum,
                frameworkAttemptCompletionPolicy: {
                    minFailedTaskCount: this.fcTrialConfig.taskRoles[index].frameworkAttemptCompletionPolicy.minFailedTaskCount,
                    minSucceededTaskCount: this.fcTrialConfig.taskRoles[index].frameworkAttemptCompletionPolicy.minSucceededTaskCount
                },
                task: taskRole
            });
        }
        return {
            apiVersion: `frameworkcontroller.microsoft.com/v1`,
            kind: 'Framework',
            metadata: {
                name: frameworkcontrollerJobName,
                namespace: 'default',
                labels: {
                    app: this.NNI_KUBERNETES_TRIAL_LABEL,
                    expId: experimentStartupInfo_1.getExperimentId(),
                    trialId: trialJobId
                }
            },
            spec: {
                executionType: 'Start',
                taskRoles: taskRoles
            }
        };
    }
    generateTaskRoleConfig(trialWorkingFolder, replicaImage, runScriptFile, podResources, containerPort) {
        if (!this.fcClusterConfig) {
            throw new Error('frameworkcontroller Cluster config is not initialized');
        }
        if (!this.fcTrialConfig) {
            throw new Error('frameworkcontroller trial config is not initialized');
        }
        let volumeSpecMap = new Map();
        if (this.fcClusterConfig.storageType === 'azureStorage') {
            volumeSpecMap.set('nniVolumes', [
                {
                    name: 'nni-vol',
                    azureFile: {
                        secretName: `${this.azureStorageSecretName}`,
                        shareName: `${this.azureStorageShare}`,
                        readonly: false
                    }
                }, {
                    name: 'frameworkbarrier-volume',
                    emptyDir: {}
                }
            ]);
        }
        else {
            let frameworkcontrollerClusterConfigNFS = this.fcClusterConfig;
            volumeSpecMap.set('nniVolumes', [
                {
                    name: 'nni-vol',
                    nfs: {
                        server: `${frameworkcontrollerClusterConfigNFS.nfs.server}`,
                        path: `${frameworkcontrollerClusterConfigNFS.nfs.path}`
                    }
                }, {
                    name: 'frameworkbarrier-volume',
                    emptyDir: {}
                }
            ]);
        }
        let containers = [
            {
                name: 'framework',
                image: replicaImage,
                command: ["sh", `${path.join(trialWorkingFolder, runScriptFile)}`],
                volumeMounts: [
                    {
                        name: 'nni-vol',
                        mountPath: this.CONTAINER_MOUNT_PATH
                    }, {
                        name: 'frameworkbarrier-volume',
                        mountPath: '/mnt/frameworkbarrier'
                    }
                ],
                resources: podResources,
                ports: [{
                        containerPort: containerPort
                    }]
            }
        ];
        let initContainers = [
            {
                name: 'frameworkbarrier',
                image: 'frameworkcontroller/frameworkbarrier',
                volumeMounts: [
                    {
                        name: 'frameworkbarrier-volume',
                        mountPath: '/mnt/frameworkbarrier'
                    }
                ]
            }
        ];
        let spec = {
            containers: containers,
            initContainers: initContainers,
            restartPolicy: 'OnFailure',
            volumes: volumeSpecMap.get('nniVolumes'),
            hostNetwork: false
        };
        if (this.fcClusterConfig.serviceAccountName) {
            spec.serviceAccountName = this.fcClusterConfig.serviceAccountName;
        }
        let taskRole = {
            pod: {
                spec: spec
            }
        };
        return taskRole;
    }
};
FrameworkControllerTrainingService = __decorate([
    component.Singleton,
    __metadata("design:paramtypes", [])
], FrameworkControllerTrainingService);
exports.FrameworkControllerTrainingService = FrameworkControllerTrainingService;
