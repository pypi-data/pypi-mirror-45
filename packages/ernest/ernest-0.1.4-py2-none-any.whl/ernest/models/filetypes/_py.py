import redbaron

from ernest.correctors.py import PyCorrector
from ernest.helpers.common import nodes_stats
from ernest.helpers.py import PyBools, PyConstants, get_dotproxy_names
from ernest.models.filetypes._base import FileItem


class Pyfile(FileItem):
    '''
    A python file.
    '''
    ext_ = 'py'
    name = 'py'
    correctors = [PyCorrector]

    def __init__(self, meta):
        super(Pyfile, self).__init__(meta)
        self.tree = redbaron.RedBaron(self.read())
        self._isequal = self.read().strip() == self.tree.dumps().strip()

    @classmethod
    def match(cls, meta):
        return meta.ext == cls.ext_

    @property
    def documentable(self):
        return self.tree.find_all(PyBools.isdocumentable)

    @property
    def docstrings(self):
        return self.tree.find_all(PyConstants.typenames.strings,
                                  lambda x: PyBools.isdocumentable(x.parent))

    @property
    def header(self):
        return self.tree.find_all(
            PyConstants.typenames.strings + PyConstants.typenames.comment,
            lambda x: PyBools.isroot(x.parent))

    @property
    def string_literals(self):
        return self.tree.find_all(PyConstants.typenames.strings,
                                  lambda x: not PyBools.isdocumentable(x.parent))

    @property
    def ascii_literals(self):
        return self.tree.find_all(PyConstants.typenames.ascii,
                                  lambda x: not PyBools.isdocumentable(x.parent))

    @property
    def imports(self):
        return list(set(['.'.join(get_dotproxy_names(n)[:3]) for n in
                         self.tree.find_all(PyConstants.typenames.imports)]))

    @property
    def forbidden_imports(self):
        return [i for i in self.imports if PyBools.isforbidden(i, self.meta.config)]

    def save(self):
        if not self._isequal:
            print(self.meta.path + ' was not equal')
            return
        else:
            with open(self.meta.path, 'w') as pyfile:
                pyfile.write(self.tree.dumps())

    @property
    def stats(self):
        return {
            'docs': {
                'documentable items': len(self.documentable),
                'strings': len(self.docstrings)
                },
            'literals': nodes_stats(self.string_literals),
            'imports': sorted(self.imports),
            'forbidden imports': sorted(self.forbidden_imports)
            }
