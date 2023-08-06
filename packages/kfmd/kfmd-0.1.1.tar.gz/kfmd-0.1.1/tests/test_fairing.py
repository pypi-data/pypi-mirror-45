from kfmd import executable, default_config
import unittest
import fairing

def hello_world():
    print('Hello world!')
    print('Hello world!')

class FairingTest(unittest.TestCase):
    def test_build(self):
        preprocessor = fairing.preprocessors.function.FunctionPreProcessor(hello_world)
        builder = fairing.builders.docker.docker.DockerBuilder(
            registry = 'gcr.io/hongyes-ml/fairing-job',
            preprocessor = preprocessor
        )
        builder.build()
        pod_spec = builder.generate_pod_spec()
        deployer = fairing.deployers.job.job.Job()
        deployer.deploy(pod_spec)