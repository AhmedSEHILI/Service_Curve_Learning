from .common import *


class Parameters(dict):

    def __init__(self, path):

        with open(path, 'r') as txt:
            for param in txt:
                name, val = param.strip().split(',')
                try:
                    self[name] = int(val)
                except ValueError:
                    self[name] = float(val)

    def modules_by_priorities(self):
        priorities = (self.get_module_priority(mod) for mod in MODULES)
        z = zip(MODULES, priorities)
        return (x[0] for x in reversed(sorted(z, key=lambda x: x[1])))

    def get_module_priority(self, module):
        return self['RT_' + module.upper() + '_PRIO']

    def get_module_period(self, module):
        return self['RT_' + module.upper() + '_INTV']
