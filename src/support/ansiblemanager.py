import os
import sys

class AnsibleManager:
    ansible_version = "2.3.0.0"

    def __init__(self, container_manager):
        self.container_manager = container_manager
        self.host_pwd = os.getenv('HOST_PWD')

    def _get_ansible(self, ansible_version):
        "lindeboomio/ansible-alpine:{}".format(ansible_version)

    def _write_hosts(self, targets, ansible_user, path):
        print('Generating hosts file at {}'.format(path))
        try:
            with open(path, 'w+') as hosts_file:
                hosts_file.write('[targets]\n')
                for target in targets:
                    hosts_file.write('{} ansible_user={}'.format(target, ansible_user))
        except IOError as err:
            print("Could not write hosts file: {}".format(err))
            sys.exit(1)

    def run(self, targets, ansible_playbook, ansible_user):
        self._write_hosts(targets, ansible_user, '{}/test/hosts'.format(os.getcwd()))
        print("Should run the playbook {} now on targets {}".format(ansible_playbook, targets))

