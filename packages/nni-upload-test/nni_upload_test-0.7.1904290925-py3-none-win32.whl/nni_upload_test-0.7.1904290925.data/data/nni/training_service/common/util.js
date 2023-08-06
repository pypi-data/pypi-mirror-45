'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const utils_1 = require("../../common/utils");
const cpp = require("child-process-promise");
const cp = require("child_process");
const gpuData_1 = require("./gpuData");
const path = require("path");
const typescript_string_operations_1 = require("typescript-string-operations");
async function validateCodeDir(codeDir) {
    let fileCount;
    try {
        fileCount = await utils_1.countFilesRecursively(codeDir);
    }
    catch (error) {
        throw new Error(`Call count file error: ${error}`);
    }
    if (fileCount && fileCount > 1000) {
        const errMessage = `Too many files(${fileCount} found}) in ${codeDir},`
            + ` please check if it's a valid code dir`;
        throw new Error(errMessage);
    }
    return fileCount;
}
exports.validateCodeDir = validateCodeDir;
async function execMkdir(directory) {
    if (process.platform === 'win32') {
        await cpp.exec(`powershell.exe New-Item -Path ${directory} -ItemType "directory" -Force`);
    }
    else {
        await cpp.exec(`mkdir -p ${directory}`);
    }
    return Promise.resolve();
}
exports.execMkdir = execMkdir;
async function execNewFile(filename) {
    if (process.platform === 'win32') {
        await cpp.exec(`powershell.exe New-Item -Path ${filename} -ItemType "file" -Force`);
    }
    else {
        await cpp.exec(`touch ${filename}`);
    }
    return Promise.resolve();
}
exports.execNewFile = execNewFile;
function execScript(filePath) {
    if (process.platform === 'win32') {
        return cp.exec(`powershell.exe -file ${filePath}`);
    }
    else {
        return cp.exec(`bash ${filePath}`);
    }
}
exports.execScript = execScript;
async function execTail(filePath) {
    let cmdresult;
    if (process.platform === 'win32') {
        cmdresult = await cpp.exec(`powershell.exe Get-Content ${filePath} -Tail 1`);
    }
    else {
        cmdresult = await cpp.exec(`tail -n 1 ${filePath}`);
    }
    return Promise.resolve(cmdresult);
}
exports.execTail = execTail;
async function execRemove(directory) {
    if (process.platform === 'win32') {
        await cpp.exec(`powershell.exe Remove-Item ${directory}`);
    }
    else {
        await cpp.exec(`rm -rf ${directory}`);
    }
    return Promise.resolve();
}
exports.execRemove = execRemove;
async function execKill(pid) {
    if (process.platform === 'win32') {
        await cpp.exec(`cmd /c taskkill /PID ${pid} /T /F`);
    }
    else {
        await cpp.exec(`pkill -P ${pid}`);
    }
    return Promise.resolve();
}
exports.execKill = execKill;
function setEnvironmentVariable(variable) {
    if (process.platform === 'win32') {
        return `$env:${variable.key}="${variable.value}"`;
    }
    else {
        return `export ${variable.key}=${variable.value}`;
    }
}
exports.setEnvironmentVariable = setEnvironmentVariable;
function getScriptName(fileNamePrefix) {
    if (process.platform === 'win32') {
        return fileNamePrefix + '.ps1';
    }
    else {
        return fileNamePrefix + '.sh';
    }
}
exports.getScriptName = getScriptName;
function getgpuMetricsCollectorScriptContent(gpuMetricCollectorScriptFolder) {
    if (process.platform === 'win32') {
        return typescript_string_operations_1.String.Format(gpuData_1.GPU_INFO_COLLECTOR_FORMAT_WINDOWS, gpuMetricCollectorScriptFolder, path.join(gpuMetricCollectorScriptFolder, 'pid'));
    }
    else {
        return typescript_string_operations_1.String.Format(gpuData_1.GPU_INFO_COLLECTOR_FORMAT_LINUX, gpuMetricCollectorScriptFolder, path.join(gpuMetricCollectorScriptFolder, 'pid'));
    }
}
exports.getgpuMetricsCollectorScriptContent = getgpuMetricsCollectorScriptContent;
