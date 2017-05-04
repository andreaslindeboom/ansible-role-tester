class RoleTester:
    def __init__(self, key_generator, ansible_manager, target_manager):
        self.key_generator = key_generator
        self.ansible_manager = ansible_manager
        self.target_manager = target_manager

    def _bundle_config(self, testconfig):
        return list(map(
            lambda x: { 'target_image': x, 'test_playbook': testconfig['test_playbook'] },
            testconfig['targets']))

    def test_roles(self, testconfig):
        self.key_generator.generate_keypair('foo')
        bundled_config = self._bundle_config(testconfig)

        for scenario in bundled_config:
            print("Preparing test target {}".format(scenario['target_image']))
            target = self.target_manager.start(scenario['target_image'])

            self.ansible_manager.run(target, scenario['test_playbook'])

            # self.target_manager.cleanup()
