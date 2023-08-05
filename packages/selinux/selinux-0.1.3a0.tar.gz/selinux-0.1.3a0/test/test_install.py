import fnmatch
import os
import subprocess
import sys
from seaworthy.definitions import ContainerDefinition
from seaworthy.utils import output_lines
from seaworthy.helpers import DockerHelper


dh = DockerHelper()

class CakeContainer(ContainerDefinition):
    IMAGE = 'centos:8'

    def __init__(self, name):
        super().__init__(name, self.IMAGE)

    # Utility methods can be added to the class to extend functionality
    # def exec_cake(self, *params):
    #     return output_lines(self.inner().exec_run(params))


#RELEASE_CONFIG_DIR = 'config/release'


def pytest_generate_tests(metafunc):
    # matches = []
    # if 'testdata' in metafunc.fixturenames:
    #     for root, dirnames, filenames in os.walk(RELEASE_CONFIG_DIR):
    #         for filename in fnmatch.filter(filenames, '*.yml'):
    #             matches.append(os.path.join(root, filename))

    # container = ContainerDefinition(
    # 'echo', 'jmalloc/echo-server',
    # wait_patterns=[r'Echo server listening on port 8080'],
    # create_kwargs={'ports': {'8080': None}})

    # fixture = container.pytest_fixture('echo_container')

    matches = [CakeContainer('centos7')]
    metafunc.parametrize('cnt', matches)


def test_install(cnt):

    # r = subprocess.run(['ansible-playbook',
    #                     '-e@%s' % testdata,
    #                     # workaround for ansible bug which may fail to detect
    #                     # python interpreter, so we force it to use the same
    #                     # interpreter
    #                     '-eansible_python_interpreter=%s' % sys.executable,
    #                     'test/validate-release-config.yml'])
    # output = testdata.exec_cake(['whoami'])
    cnt.setup(helper=dh)
    cnt.start()
    assert cnt.created
    # x = testdata.get_logs()
    # assert x == 0
