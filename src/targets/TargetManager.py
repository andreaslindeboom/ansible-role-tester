class TargetManager:
    def __init__(self, docker_client, target_config):
        self.docker_client = docker_client

    def foo(self):
        return 'foo'

    #todo:
    # this class should take the following things:
    # - docker client
    # - target config
    # and do the following things:
    # - start a target by name (or a list of names)
    # - clean up everything it creates (network, containers)
