from ._executor import Executor, Execution
from ._in_proc import InProcExecutor
import cloudpickle
import base64

class DockerExecutor(Executor):
    def __init__(self, base_image = 'python:3.6'):
        self.base_image = base_image

    def execute(self, execution):
        def entry_point():
            InProcExecutor().execute(execution)
        entry_point_fn = base64.b64encode(cloudpickle.dumps(entry_point))
        python_shim = "import cloudpickle;import base64;cloudpickle.loads(base64.b64decode({}))()".format(
            entry_point_fn)
        python_shim = 'python -c "{}"'.format(python_shim)
        bash_shim = 'pip install kfmd;{}'.format(python_shim)
        bash_shim = '/bin/bash -c "{}"'.format(bash_shim.replace('"', '\\"'))

        import docker
        client = docker.from_env()
        # print(client.containers.run('alpine', 'echo hello world'))
        print(client.containers.run(self.base_image, bash_shim, remove = True).decode('utf-8'))
