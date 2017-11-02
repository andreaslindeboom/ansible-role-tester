import docker
import mock
import pytest

from targets import TargetManager

@pytest.fixture
def docker_client():
    return mock.create_autospec(docker.DockerClient)

@pytest.fixture
def target_config():
    return {
        'foo': 'bar' }

@pytest.fixture
def invalid_target_configs():
    return [
        {'foo': 'bar' },
        { 'baz': 'baa' }]

@pytest.fixture
def target_manager(docker_client, target_config):
    return TargetManager(docker_client, target_config)

def test_rejects_invalid_config(docker_client, invalid_target_configs):
    for config in invalid_target_configs:
        TargetManager(docker_client, invalid_target_configs)

def test_foo(target_manager, docker_client):
    assert target_manager.foo() == 'foo'

