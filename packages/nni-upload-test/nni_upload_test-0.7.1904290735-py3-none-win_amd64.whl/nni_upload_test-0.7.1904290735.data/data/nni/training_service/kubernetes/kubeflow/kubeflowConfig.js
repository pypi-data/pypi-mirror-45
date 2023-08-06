'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const assert = require("assert");
const kubernetesConfig_1 = require("../kubernetesConfig");
const errors_1 = require("../../../common/errors");
class KubeflowClusterConfig extends kubernetesConfig_1.KubernetesClusterConfig {
    constructor(apiVersion, operator) {
        super(apiVersion);
        this.operator = operator;
    }
}
exports.KubeflowClusterConfig = KubeflowClusterConfig;
class KubeflowClusterConfigNFS extends kubernetesConfig_1.KubernetesClusterConfigNFS {
    constructor(operator, apiVersion, nfs, storage) {
        super(apiVersion, nfs, storage);
        this.operator = operator;
    }
    get storageType() {
        return 'nfs';
    }
    static getInstance(jsonObject) {
        let kubeflowClusterConfigObjectNFS = jsonObject;
        assert(kubeflowClusterConfigObjectNFS !== undefined);
        return new KubeflowClusterConfigNFS(kubeflowClusterConfigObjectNFS.operator, kubeflowClusterConfigObjectNFS.apiVersion, kubeflowClusterConfigObjectNFS.nfs, kubeflowClusterConfigObjectNFS.storage);
    }
}
exports.KubeflowClusterConfigNFS = KubeflowClusterConfigNFS;
class KubeflowClusterConfigAzure extends kubernetesConfig_1.KubernetesClusterConfigAzure {
    constructor(operator, apiVersion, keyVault, azureStorage, storage) {
        super(apiVersion, keyVault, azureStorage, storage);
        this.operator = operator;
    }
    get storageType() {
        return 'azureStorage';
    }
    static getInstance(jsonObject) {
        let kubeflowClusterConfigObjectAzure = jsonObject;
        return new KubeflowClusterConfigAzure(kubeflowClusterConfigObjectAzure.operator, kubeflowClusterConfigObjectAzure.apiVersion, kubeflowClusterConfigObjectAzure.keyVault, kubeflowClusterConfigObjectAzure.azureStorage, kubeflowClusterConfigObjectAzure.storage);
    }
}
exports.KubeflowClusterConfigAzure = KubeflowClusterConfigAzure;
class KubeflowClusterConfigFactory {
    static generateKubeflowClusterConfig(jsonObject) {
        let storageConfig = jsonObject;
        if (!storageConfig) {
            throw new Error("Invalid json object as a StorageConfig instance");
        }
        if (storageConfig.storage && storageConfig.storage === 'azureStorage') {
            return KubeflowClusterConfigAzure.getInstance(jsonObject);
        }
        else if (storageConfig.storage === undefined || storageConfig.storage === 'nfs') {
            return KubeflowClusterConfigNFS.getInstance(jsonObject);
        }
        throw new Error(`Invalid json object ${jsonObject}`);
    }
}
exports.KubeflowClusterConfigFactory = KubeflowClusterConfigFactory;
class KubeflowTrialConfig extends kubernetesConfig_1.KubernetesTrialConfig {
    constructor(codeDir) {
        super(codeDir);
    }
    get operatorType() {
        throw new errors_1.MethodNotImplementedError();
    }
}
exports.KubeflowTrialConfig = KubeflowTrialConfig;
class KubeflowTrialConfigTemplate extends kubernetesConfig_1.KubernetesTrialConfigTemplate {
    constructor(replicas, command, gpuNum, cpuNum, memoryMB, image) {
        super(command, gpuNum, cpuNum, memoryMB, image);
        this.replicas = replicas;
    }
}
exports.KubeflowTrialConfigTemplate = KubeflowTrialConfigTemplate;
class KubeflowTrialConfigTensorflow extends KubeflowTrialConfig {
    constructor(codeDir, worker, ps) {
        super(codeDir);
        this.ps = ps;
        this.worker = worker;
    }
    get operatorType() {
        return 'tf-operator';
    }
}
exports.KubeflowTrialConfigTensorflow = KubeflowTrialConfigTensorflow;
class KubeflowTrialConfigPytorch extends KubeflowTrialConfig {
    constructor(codeDir, master, worker) {
        super(codeDir);
        this.master = master;
        this.worker = worker;
    }
    get operatorType() {
        return 'pytorch-operator';
    }
}
exports.KubeflowTrialConfigPytorch = KubeflowTrialConfigPytorch;
class KubeflowTrialConfigFactory {
    static generateKubeflowTrialConfig(jsonObject, operator) {
        if (operator === 'tf-operator') {
            let kubeflowTrialConfigObject = jsonObject;
            return new KubeflowTrialConfigTensorflow(kubeflowTrialConfigObject.codeDir, kubeflowTrialConfigObject.worker, kubeflowTrialConfigObject.ps);
        }
        else if (operator === 'pytorch-operator') {
            let kubeflowTrialConfigObject = jsonObject;
            return new KubeflowTrialConfigPytorch(kubeflowTrialConfigObject.codeDir, kubeflowTrialConfigObject.master, kubeflowTrialConfigObject.worker);
        }
        throw new Error(`Invalid json object ${jsonObject}`);
    }
}
exports.KubeflowTrialConfigFactory = KubeflowTrialConfigFactory;
