class KeyGenerator:
    keygen_version = "0.1.1"

    def __init__(self, container_manager):
        self.container_manager = container_manager

    def generate_keypair(self, filename):
        self.container_manager.start(
            'lindeboomio/openssh-keygen-alpine:{}'.format(self.keygen_version),
            volumes = dict([('keys', '/keys')]),
            command = "-t rsa -b 2048 -P '' -f ansible")

