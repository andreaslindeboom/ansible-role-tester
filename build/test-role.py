#!/usr/bin/env python3

import docker
import sys
import yaml

class YamlFileLoader:
    @classmethod
    def load_yaml(self, filepath):
        try:
            config = open(filepath, 'r')
        except OSError:
            print("File {} not found".format(filepath))
            sys.exit(1)

        try:
            parsed_yaml = yaml.load(config)
        except yaml.YAMLError as err:
            print("Yaml file could not be loaded:\n {}".format(err))
            sys.exit(1)

        return parsed_yaml

class ContainerManager:
    def __init__(self, docker_client, docker_network_id):
        self.docker_client = docker_client
        self.managed_containers = []

        self.ensure_network_exists(docker_network_id)

    def __del__(self):
        self.cleanup_networks()

    def ensure_network_exists(self, docker_network_id):
        try:
            existing_networks = self.docker_client.networks.list()
            if (docker_network_id) not in existing_networks:
                self.docker_network = self.docker_client.networks.create(docker_network_id)
        except docker.errors.APIError as err:
            print("Docker API Error:\n {}".format(err))
            sys.exit(1)

    def cleanup_networks(self):
        try:
            if (self.docker_network):
                self.docker_network.remove()
        except docker.errors.APIError as err:
            print("Docker API Error:\n {}".format(err))
            sys.exit(1)

    def start(self, image):
        try:
            container = self.docker_client.containers.run(image, detach=True, publish_all_ports=True, networks=[self.docker_network.name])
            self.managed_containers.append(container)

            return container
        except docker.errors.APIError as err:
            print("Docker API Error:\n {}".format(err))
            sys.exit(1)

    def cleanup(self):
        try:
            while self.managed_containers:
                container = self.managed_containers.pop()

                print("Cleaning up container {}".format(container.id))
                container.remove(force=True)
        except docker.errors.APIError as err:
            print("Docker API Error:\n {}".format(err))
            sys.exit(1)

class TargetManager:
    def __init__(self, container_manager):
        self.container_manager = container_manager

    def start(self, target_image):
        return self.container_manager.start(target_image)

    def cleanup(self):
        self.container_manager.cleanup()

class AnsibleManager:

    def __init__(self, container_manager):
        self.container_manager = container_manager

    def get_ansible(ansible_version):
        "lindeboomio/ansible-alpine:{}".format(ansible_version)

class RoleTester:
    ansible_version = "2.3.0.0"
    test_location = "test/test.yml"

    def __init__(self, ansible_manager, target_manager):
        self.ansible_manager = ansible_manager
        self.target_manager = target_manager

    def bundle_config(self, testconfig):
        return list(map(
            lambda x: { 'target_image': x, 'test_location': self.test_location },
            testconfig['targets']))

    def test_roles(self, testconfig):
        bundled_config = self.bundle_config(testconfig)

        for scenario in bundled_config:
            print("Preparing test target {}".format(scenario['target_image']))
            self.target_manager.start(scenario['target_image'])

            # self.ansible_manager.run( ansible_version)

            # self.target_manager.cleanup()

def main():
    config_path = "testconfig.yml"

    container_manager = ContainerManager(docker_client = docker.from_env(), docker_network_id = 'role_tester_network')
    ansible_manager = AnsibleManager(container_manager)
    target_manager = TargetManager(container_manager)

    role_tester = RoleTester(ansible_manager, target_manager)
    test_config = YamlFileLoader.load_yaml(config_path)

    role_tester.test_roles(test_config)

if __name__ == "__main__": main()
