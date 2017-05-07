class TargetManager:
    def __init__(self, container_manager):
        self.container_manager = container_manager

    def start(self, target_image, authorized_key = None):
        container = self.container_manager.start(
            image = target_image,
            publish_ports = True,
            environment = { "AUTHORIZED_KEY": authorized_key })
        return container.name

