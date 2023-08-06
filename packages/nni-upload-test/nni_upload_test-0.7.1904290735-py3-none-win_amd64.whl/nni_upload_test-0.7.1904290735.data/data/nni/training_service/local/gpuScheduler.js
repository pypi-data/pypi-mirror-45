'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const fs = require("fs");
const os = require("os");
const path = require("path");
const util_1 = require("../common/util");
const log_1 = require("../../common/log");
const utils_1 = require("../../common/utils");
class GPUScheduler {
    constructor() {
        this.stopping = false;
        this.log = log_1.getLogger();
        this.gpuMetricCollectorScriptFolder = `${os.tmpdir()}/nni/script`;
    }
    async run() {
        await this.runGpuMetricsCollectorScript();
        while (!this.stopping) {
            try {
                await this.updateGPUSummary();
            }
            catch (error) {
                this.log.error('Read GPU summary failed with error: ', error);
            }
            await utils_1.delay(5000);
        }
    }
    async runGpuMetricsCollectorScript() {
        await util_1.execMkdir(this.gpuMetricCollectorScriptFolder);
        let gpuMetricsCollectorScriptPath = path.join(this.gpuMetricCollectorScriptFolder, util_1.getScriptName('gpu_metrics_collector'));
        const gpuMetricsCollectorScriptContent = util_1.getgpuMetricsCollectorScriptContent(this.gpuMetricCollectorScriptFolder);
        await fs.promises.writeFile(gpuMetricsCollectorScriptPath, gpuMetricsCollectorScriptContent, { encoding: 'utf8' });
        util_1.execScript(gpuMetricsCollectorScriptPath);
    }
    getAvailableGPUIndices() {
        if (this.gpuSummary !== undefined) {
            return this.gpuSummary.gpuInfos.filter((info) => info.activeProcessNum === 0)
                .map((info) => info.index);
        }
        return [];
    }
    getSystemGpuCount() {
        if (this.gpuSummary !== undefined) {
            return this.gpuSummary.gpuCount;
        }
        return 0;
    }
    async stop() {
        this.stopping = true;
        try {
            const pid = await fs.promises.readFile(path.join(this.gpuMetricCollectorScriptFolder, 'pid'), 'utf8');
            await util_1.execKill(pid);
            await util_1.execRemove(this.gpuMetricCollectorScriptFolder);
        }
        catch (error) {
            this.log.error(`GPU scheduler error: ${error}`);
        }
    }
    async updateGPUSummary() {
        const cmdresult = await util_1.execTail(path.join(this.gpuMetricCollectorScriptFolder, 'gpu_metrics'));
        if (cmdresult && cmdresult.stdout) {
            this.gpuSummary = JSON.parse(cmdresult.stdout);
        }
        else {
            this.log.error('Could not get gpu metrics information!');
        }
    }
}
exports.GPUScheduler = GPUScheduler;
