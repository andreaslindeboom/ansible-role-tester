import os
import sys

class KeyManager:
    keygen_version = "0.1.1"

    def __init__(self, container_manager, key_name, cleanup = True):
        self.container_manager = container_manager
        self.key_name = key_name
        self.cleanup = cleanup
        self._generate_keypair()

    def __del__(self):
        if self.cleanup:
            print("\n--- Key cleanup ---")
            self._cleanup()

    def _generate_keypair(self):
        print("Generating keypair to enable Ansible to access target over SSH")
        self.container_manager.start(
            'lindeboomio/openssh-keygen-alpine:{}'.format(self.keygen_version),
            volumes = dict([('keys', '/keys')]),
            command = "-t rsa -b 2048 -P '' -f {}".format(self.key_name))

        try:
            with open('/keys/{}'.format(self.key_name), 'r') as key_file:
                self.key = key_file.read().strip('\n\r')

            with open('/keys/{}.pub'.format(self.key_name), 'r') as pubkey_file:
                self.pubkey = pubkey_file.read().strip('\n\r')
        except IOError:
            print("Could not read key file")
            sys.exit(1)

    def _cleanup(self):
        key_files = os.listdir("/keys")
        for key in key_files:
            file_path = "/keys/{}".format(key)
            if os.path.isfile(file_path):
                print("Cleaning up {}".format(file_path))
                os.unlink(file_path)

    def get_pubkey(self):
        return self.pubkey
