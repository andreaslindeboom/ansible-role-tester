class TargetManager:
    def __init__(self, container_manager):
        self.container_manager = container_manager

    def start(self, target_image):
        return self.container_manager.start_detached(target_image)

    def cleanup(self):
        self.container_manager.cleanup()


