from .filetypes import *
from .meta import Metadata


class FileFactory(object):
    '''
    Assigns file types.
    '''

    classes = [FileItem, Pyfile, AnsibleTask]

    def __init__(self, config):
        self.config = config

    def __call__(self, *args, **kwargs):
        path = args[0]
        mdata = Metadata(path, self.config)
        try:
            castto = next(c for c in self.classes if c.match(mdata))
            item = castto(mdata)
        except StopIteration:
            item = FileItem(mdata)
        return item
