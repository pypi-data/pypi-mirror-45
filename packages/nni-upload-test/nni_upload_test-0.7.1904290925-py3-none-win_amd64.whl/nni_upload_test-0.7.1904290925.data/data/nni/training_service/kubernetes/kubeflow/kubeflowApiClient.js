'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const fs = require("fs");
const kubernetesApiClient_1 = require("../kubernetesApiClient");
exports.GeneralK8sClient = kubernetesApiClient_1.GeneralK8sClient;
class KubeflowOperatorClient extends kubernetesApiClient_1.KubernetesCRDClient {
    static generateOperatorClient(kubeflowOperator, operatorApiVersion) {
        if (kubeflowOperator === 'tf-operator') {
            if (operatorApiVersion == 'v1alpha2') {
                return new TFOperatorClientV1Alpha2();
            }
            else if (operatorApiVersion == 'v1beta1') {
                return new TFOperatorClientV1Beta1();
            }
        }
        else if (kubeflowOperator === 'pytorch-operator') {
            if (operatorApiVersion == 'v1alpha2') {
                return new PytorchOperatorClientV1Alpha2();
            }
            else if (operatorApiVersion == 'v1beta1') {
                return new PytorchOperatorClientV1Beta1();
            }
        }
        throw new Error(`Invalid operator ${kubeflowOperator} or apiVersion ${operatorApiVersion}`);
    }
}
exports.KubeflowOperatorClient = KubeflowOperatorClient;
class TFOperatorClientV1Alpha2 extends KubeflowOperatorClient {
    constructor() {
        super();
        this.crdSchema = JSON.parse(fs.readFileSync('./config/kubeflow/tfjob-crd-v1alpha2.json', 'utf8'));
        this.client.addCustomResourceDefinition(this.crdSchema);
    }
    get operator() {
        return this.client.apis["kubeflow.org"].v1alpha2.namespaces('default').tfjobs;
    }
    get containerName() {
        return 'tensorflow';
    }
}
class TFOperatorClientV1Beta1 extends kubernetesApiClient_1.KubernetesCRDClient {
    constructor() {
        super();
        this.crdSchema = JSON.parse(fs.readFileSync('./config/kubeflow/tfjob-crd-v1beta1.json', 'utf8'));
        this.client.addCustomResourceDefinition(this.crdSchema);
    }
    get operator() {
        return this.client.apis["kubeflow.org"].v1beta1.namespaces('default').tfjobs;
    }
    get containerName() {
        return 'tensorflow';
    }
}
class PytorchOperatorClientV1Alpha2 extends KubeflowOperatorClient {
    constructor() {
        super();
        this.crdSchema = JSON.parse(fs.readFileSync('./config/kubeflow/pytorchjob-crd-v1alpha2.json', 'utf8'));
        this.client.addCustomResourceDefinition(this.crdSchema);
    }
    get operator() {
        return this.client.apis["kubeflow.org"].v1alpha2.namespaces('default').pytorchjobs;
    }
    get containerName() {
        return 'pytorch';
    }
}
class PytorchOperatorClientV1Beta1 extends kubernetesApiClient_1.KubernetesCRDClient {
    constructor() {
        super();
        this.crdSchema = JSON.parse(fs.readFileSync('./config/kubeflow/pytorchjob-crd-v1beta1.json', 'utf8'));
        this.client.addCustomResourceDefinition(this.crdSchema);
    }
    get operator() {
        return this.client.apis["kubeflow.org"].v1beta1.namespaces('default').pytorchjobs;
    }
    get containerName() {
        return 'pytorch';
    }
}
