class TargetManager:
    def __init__(self, container_manager, key_manager):
        self.container_manager = container_manager
        self.key_manager = key_manager

    def start(self, target_image):
        return self.container_manager.start(image = target_image, publish_ports = True)

