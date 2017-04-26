#!/usr/bin/env python3

import yaml
import sys
import subprocess

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

class ShellHelper:
    docker_network = "role_tester_net"

    @classmethod
    def ensure_network_exists(self, network):
        network_list = subprocess.run([ "docker" , "network", "list", "|" , "awk", "'{ print $2 }'" ], stdout=subprocess.PIPE)
        if (network not in network_list.stdout):
            print("Network {} does not exist, creating").format(network)
            subprocess.run([ "docker" , "network", "create", network ], stdout=subprocess.PIPE)
        else:
            print("Network {} exists, not creating").format(network)


    @classmethod
    def start_target_container(self, target_container):
        ShellHelper.ensure_network_exists(ShellHelper.docker_network)

        subprocess.run([ "docker" , "run", "-itd", "-P", "--net", ShellHelper.docker_network, target_container ])

class RoleTester:
    def __init__(self, ansible_version, ansible_image, test_location):
        self.ansible_version = ansible_version
        self.ansible_image = ansible_image
        self.test_location = test_location

    def bundle_config(self, testconfig):
        return list(map(
            lambda x: { 'target': x, 'ansible_image': self.ansible_image, 'test_location': self.test_location },
            testconfig['targets']))

    def test_roles(self, testconfig):
        bundled_config = self.bundle_config(testconfig)

        for test_case in bundled_config:
            print("Preparing test target")
            ShellHelper.start_target_container(test_case['target'])


def main():
    config_path = "testconfig.yml"
    ansible_version = "2.3.0.0"
    ansible_image = "lindeboomio/ansible-alpine:{}".format(ansible_version)
    test_location = "test/test.yml"

    test_config = YamlFileLoader.load_yaml(config_path)
    role_tester = RoleTester(ansible_version, ansible_image, test_location)

    role_tester.test_roles(test_config)

if __name__ == "__main__": main()
