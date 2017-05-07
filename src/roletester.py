class RoleTester:
    active_targets = []

    def __init__(self, key_manager, ansible_manager, target_manager):
        self.key_manager = key_manager
        self.ansible_manager = ansible_manager
        self.target_manager = target_manager

    def test_roles(self, testconfig):
        authorized_key = self.key_manager.get_pubkey()

        print("\n--- Target preparation ---")
        for target in testconfig['targets']:
            print("Preparing test target {}".format(target))
            running_target = self.target_manager.start(target, authorized_key)
            self.active_targets.append(running_target)

        print("\n--- Test execution ---")
        self.ansible_manager.run(self.active_targets, testconfig['ansible']['playbook'], testconfig['ansible']['user'])
