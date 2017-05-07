class RoleTester:
    def __init__(self, key_generator, ansible_manager, target_manager):
        self.key_generator = key_generator
        self.ansible_manager = ansible_manager
        self.target_manager = target_manager

    def _bundle_config(self, testconfig):
        return list(map(
            lambda x: { 'target': x, 'playbook': testconfig['playbook'] },
            testconfig['targets']))

    def test_roles(self, testconfig):
        print("--- General preparation ---")
        self.key_generator.generate_keypair('ansible')
        bundled_config = self._bundle_config(testconfig)

        print("\n--- Target preparation ---")
        for scenario in bundled_config:
            print("Preparing test target {}".format(scenario['target']))
            # self.ansible_manager.run(target, scenario['playbook'])

            target = self.target_manager.start(scenario['target'])
