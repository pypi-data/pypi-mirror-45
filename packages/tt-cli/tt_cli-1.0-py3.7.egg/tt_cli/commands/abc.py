class ABCCommand:
    def add_arguments(self, parser):
        pass

    def handle(self, **kwargs):
        raise NotImplementedError
