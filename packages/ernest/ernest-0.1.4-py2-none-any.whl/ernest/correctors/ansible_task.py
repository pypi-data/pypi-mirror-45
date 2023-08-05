import re

from ._base import Corrector


def _textify(k, v, indent=0, list_item=False):
    d = []
    prefix = '  ' * (indent - 1) + '- ' if list_item else '  ' * indent
    if (isinstance(v, list) or isinstance(v, dict)) and k is not None:
        d.append(prefix + k + ':')
    # actual processing
    if isinstance(v, list):
        for lv in v:
            d += _textify(None, lv, indent + 1, True)
    elif isinstance(v, dict):
        for i, (dk, dv) in enumerate(v.items()):
            d += _textify(dk, dv, indent + 1, list_item if i == 0 else False)
    elif isinstance(v, str):
        blocks = re.split('(?<!{{)\s(?!}})', v)
        if all(['=' in b and re.fullmatch('\w+', b.split('=')[0]) for b in
                blocks]):
            v = {bk: bv for bk, bv in [b.split('=', 1) for b in blocks]}
            d += _textify(k, v, indent + 1)
        else:
            if k is not None and 'regexp' in k:
                v = "'{}'".format(str(v))
            else:
                quote = ['{{' in str(v),
                         '/' in str(v),
                         ' ' in str(v),
                         '-' in str(v)]
                rm_quote = re.findall('([\"\'])?([^\"\']+)([\"\'])?', str(v))[0][1]
                v = '"{}"'.format(rm_quote) if any(quote) else str(v)
            if k is not None:
                k = prefix + str(k) + ':'
                d.append('{0} {1}'.format(k, v))
            else:
                d.append(prefix + v)
    elif isinstance(v, bool):
        v = 'yes' if v else 'no'
        if k is not None:
            k = prefix + str(k) + ':'
            d.append('{0} {1}'.format(k, v))
        else:
            d.append(prefix + v)
    else:
        if k is not None:
            k = prefix + str(k) + ':'
            d.append('{0} {1}'.format(k, v))
        else:
            d.append(prefix + str(v))
    return d


class AnsibleTaskCorrector(Corrector):
    def __init__(self, config):
        super(AnsibleTaskCorrector, self).__init__(config)
        self.funcmap.update({
            'inline': self.remove_inline
            })

    def remove_inline(self, f):
        tasks = f.tasks
        if isinstance(tasks, dict):
            tasks = tasks.items()
            list_item = False
        elif isinstance(tasks, list):
            list_item = True
        else:
            raise Exception
        for k, (v, txt) in tasks:
            text_lines = _textify(k, v, 0, list_item)
            col = k._column_number if hasattr(k, '_column_number') else 3
            text_lines = [(' ' * (col - 3)) + l for l in text_lines]
            text = '\n'.join(text_lines)
            f.content = f.content.replace(txt, text)
