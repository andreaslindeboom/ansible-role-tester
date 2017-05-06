import docker
import sys
import uuid

class ContainerManager:
    def __init__(self, docker_client, container_network_id):
        self.docker_client = docker_client
        self.managed_containers = []

        self._ensure_network_exists(container_network_id)

    def __del__(self):
        print("")
        self.cleanup()
        self._cleanup_networks()

    def _ensure_network_exists(self, docker_network_id):
        try:
            existing_networks = list(map(lambda x: x.name, self.docker_client.networks.list()))
            if (docker_network_id) not in existing_networks:
                self.docker_network = self.docker_client.networks.create(docker_network_id)
            else:
                self.docker_network = self.docker_client.networks.get(docker_network_id)
        except docker.errors.APIError as err:
            print("Docker API Error:\n {}".format(err))
            sys.exit(1)

    def _cleanup_networks(self):
        try:
            if (self.docker_network):
                print("Cleaning up network {}".format(self.docker_network.name))
                self.docker_network.remove()
        except docker.errors.APIError as err:
            print("Docker API Error:\n {}".format(err))
            sys.exit(1)

    def _generateContainerName(self):
        return "{}-{}".format(self.docker_network.name, uuid.uuid4())

    def start(self, image, publish_ports=False, volumes={}, command=None):
        try:
            print("Starting container with image {} on network {}".format(image, self.docker_network.name))
            container = self.docker_client.containers.run(
                image,
                name=self._generateContainerName(),
                detach=True,
                publish_all_ports=publish_ports,
                networks=[self.docker_network.name],
                volumes = dict(map(lambda paths: (paths[0], {'bind': paths[1], 'ro': False}), volumes.items())),
                command = command
            )

            self.managed_containers.append(container)

            # explicitly connect container to network to get around this bug: https://github.com/docker/docker-py/issues/1562
            self.docker_network.connect(container)
            default_network = self.docker_client.networks.get('bridge')
            default_network.disconnect(container)

            # reload container to get port metadata
            container.reload()

            return container
        except docker.errors.APIError as err:
            print("Docker API Error:\n {}".format(err))
            sys.exit(1)
        except docker.errors.ContainerError as err:
            print("Docker Container Error:\n {}".format(err))
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

