
import collections
import os

import sublime, sublime_plugin


def deep_update(d, u):
    for k, v in u.items():
        if isinstance(v, collections.Mapping):
            d[k] = deep_update(d.get(k, {}), v)
        else:
            d[k] = u[k]
    return d


class Virtualenv:

    def __init__(self, root):
        self.root = root

    def __str__(self):
        return self.root

    @property
    def name(self):
        return os.path.basename(self.root)

    @property
    def path(self):
        return os.path.join(self.root, "bin")

    def get_build_kwargs(self):
        return {
            'path': os.pathsep.join((self.path, os.environ.get('PATH', ""))),  # PATH=venv/path:$PATH
            'env': {'VIRTUAL_ENV': str(self)}
        }


class RunOnVirtualenvCommand(sublime_plugin.WindowCommand):
    def run(self, **kwargs):
        virtualenv = Virtualenv("/home/adrian/.virtualenvs/sublime_virtualenv")
        deep_update(kwargs, virtualenv.get_build_kwargs())
        self.window.run_command('exec', kwargs)
