import docker
from support import *

from roletester import RoleTester

def main():
    config_path = "testconfig.yml"
    container_network_id = 'role_tester_network'
    key_name = 'ansible'

    print("--- General preparation ---")

    container_manager = ContainerManager(
        docker_client = docker.from_env(),
        container_network_id = container_network_id)

    key_manager = KeyManager(container_manager, key_name)

    role_tester = RoleTester(
        key_manager,
        AnsibleManager(container_manager, key_manager),
        TargetManager(container_manager, key_manager))

    test_config = YamlFileLoader.load_yaml(config_path)

    role_tester.test_roles(test_config)

if __name__ == "__main__": main()

