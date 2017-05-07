class RoleTester:
    active_targets = []

    def __init__(self, key_manager, ansible_manager, target_manager):
        self.key_manager = key_manager
        self.ansible_manager = ansible_manager
        self.target_manager = target_manager

    def _bundle_config(self, testconfig):
        return list(map(
            lambda x: { 'target': x, 'playbook': testconfig['playbook'] },
            testconfig['targets']))

    def test_roles(self, testconfig):
        bundled_config = self._bundle_config(testconfig)
        authorized_key = self.key_manager.get_pubkey()

        print("\n--- Target preparation ---")
        for scenario in bundled_config:
            print("Preparing test target {}".format(scenario['target']))
            target = self.target_manager.start(scenario['target'], authorized_key)
            self.active_targets.append(target)

        print("\n--- Test execution ---")
        for scenario in bundled_config:
            self.ansible_manager.run(target, scenario['playbook'])
