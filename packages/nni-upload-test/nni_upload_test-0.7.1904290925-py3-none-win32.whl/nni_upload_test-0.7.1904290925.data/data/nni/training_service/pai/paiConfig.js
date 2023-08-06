'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const trialConfig_1 = require("../common/trialConfig");
class PAITaskRole {
    constructor(name, taskNumber, cpuNumber, memoryMB, gpuNumber, command, shmMB) {
        this.name = name;
        this.taskNumber = taskNumber;
        this.cpuNumber = cpuNumber;
        this.memoryMB = memoryMB;
        this.gpuNumber = gpuNumber;
        this.command = command;
        this.shmMB = shmMB;
    }
}
exports.PAITaskRole = PAITaskRole;
class PAIJobConfig {
    constructor(jobName, image, dataDir, outputDir, codeDir, taskRoles, virtualCluster) {
        this.jobName = jobName;
        this.image = image;
        this.dataDir = dataDir;
        this.outputDir = outputDir;
        this.codeDir = codeDir;
        this.taskRoles = taskRoles;
        this.virtualCluster = virtualCluster;
    }
}
exports.PAIJobConfig = PAIJobConfig;
class PAIClusterConfig {
    constructor(userName, passWord, host) {
        this.userName = userName;
        this.passWord = passWord;
        this.host = host;
    }
}
exports.PAIClusterConfig = PAIClusterConfig;
class NNIPAITrialConfig extends trialConfig_1.TrialConfig {
    constructor(command, codeDir, gpuNum, cpuNum, memoryMB, image, dataDir, outputDir, virtualCluster, shmMB) {
        super(command, codeDir, gpuNum);
        this.cpuNum = cpuNum;
        this.memoryMB = memoryMB;
        this.image = image;
        this.dataDir = dataDir;
        this.outputDir = outputDir;
        this.virtualCluster = virtualCluster;
        this.shmMB = shmMB;
    }
}
exports.NNIPAITrialConfig = NNIPAITrialConfig;
