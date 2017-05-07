class AnsibleManager:
    ansible_version = "2.3.0.0"

    def __init__(self, container_manager, key_manager):
        self.container_manager = container_manager
        self.key_manager = key_manager

    def _get_ansible(ansible_version):
        "lindeboomio/ansible-alpine:{}".format(ansible_version)

    def run(self, target, test_playbook):
        print("Should run the playbook {} now on target {}".format(test_playbook, target.id))

