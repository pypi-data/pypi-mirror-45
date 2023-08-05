from ansible.parsing.yaml.loader import AnsibleLoader
from ansible.parsing.yaml.objects import AnsibleSequence, AnsibleMapping

from ernest.correctors.ansible_task import AnsibleTaskCorrector
from ernest.models.filetypes._base import FileItem


class AnsibleTask(FileItem):
    '''
    A YAML file used with Ansible.
    '''

    ext_ = 'yml'
    name = 'ansible-task'
    correctors = [AnsibleTaskCorrector]

    @classmethod
    def match(cls, meta):
        ext = meta.ext == cls.ext_
        #in_task_folder = '/tasks/' in meta.path
        return ext

    @property
    def tasks(self):
        with open(self.meta.path, 'r') as f:
            reader = AnsibleLoader(f)
            data = reader.get_data()
        content = self.content.splitlines(keepends=False)

        def _ln(current, item):
            if isinstance(item, list):
                return max([_ln(current, i) for i in item])
            elif isinstance(item, dict):
                return max([_ln(current, v) for k, v in item.items()])
            else:
                if hasattr(item, '_line_number'):
                    return item._line_number
                else:
                    return current + 1

        if isinstance(data, dict):
            tasklist = {}
            for tk, tv in data.items():
                ln = tk._line_number - 1
                txt = content[ln:_ln(ln, tk)]
                tasklist[tk] = (tv, '\n'.join(txt))
        elif isinstance(data, list):
            tasklist = []
            for t in data:
                ln = t._line_number - 1
                txt = content[ln:_ln(ln, t)]
                tasklist.append((None, (t, '\n'.join(txt))))
        else:
            tasklist = None
        return tasklist

    @property
    def stats(self):
        return {
            'tasks': len(self.tasks)
            }
