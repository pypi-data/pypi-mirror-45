class Corrector(object):
    def __init__(self, config):
        self.config = config
        self.funcmap = {}

    def get(self, methods):
        if methods == [0]:
            return self.funcmap.values()
        else:
            return [self.funcmap.get(m, None) for m in methods]
