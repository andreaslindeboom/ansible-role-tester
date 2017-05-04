import docker
import support

def main():
    config_path = "testconfig.yml"
    container_network_id = 'role_tester_network'

    container_manager = support.ContainerManager(
        docker_client = docker.from_env(),
        container_network_id = container_network_id)

    role_tester = support.RoleTester(
        support.KeyGenerator(container_manager),
        support.AnsibleManager(container_manager),
        support.TargetManager(container_manager))

    test_config = support.YamlFileLoader.load_yaml(config_path)

    role_tester.test_roles(test_config)

if __name__ == "__main__": main()

