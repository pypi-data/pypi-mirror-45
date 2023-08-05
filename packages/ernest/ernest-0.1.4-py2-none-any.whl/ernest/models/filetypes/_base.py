from ernest.helpers.common import pretty


class FileItem(object):
    '''
    A generic file type.
    '''
    ext_ = None
    name = 'file'
    correctors = []

    def __init__(self, meta):
        self.meta = meta
        try:
            self.content = self.read()
        except UnicodeDecodeError:
            self.content = ''
        self._correctors = [c(meta.config) for c in self.correctors]

    @classmethod
    def match(cls, meta):
        return False

    def read(self):
        with open(self.meta.path, 'r') as f:
            return f.read()

    def correct(self, *methods):
        if 0 or 'all' in methods:
            methods = [0]
        funcs = [m for c in self._correctors for m in c.get(methods) if m is not None]
        for m in funcs:
            m(self)
        self.save()

    def save(self):
        with open(self.meta.path, 'w') as f:
            f.write(self.content)

    @property
    def stats(self):
        return {}

    def __repr__(self):
        content = [item for sublist in [pretty(k, v, 0) for k, v in self.stats.items()]
                   for item in sublist]
        return '\n'.join([self.meta.path] + content) + '\n'