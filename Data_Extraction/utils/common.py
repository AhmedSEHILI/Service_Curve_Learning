from collections import namedtuple

MissionItem = namedtuple('MissionItem', 'ts it')

# Named tuples for trace restructuring
for ty in ('Activate', 'Run', 'Preempt', 'Suspend', 'End', 'Miss'):
    globals()[ty] = namedtuple(ty, 'ts id')

# List of modules ordered as they appear in "snoop.cpp"
MODULES = ('snsr', 'rctl', 'ekf2', 'actl', 'pctl', 'hte', 'fmgr', 'cmdr', 'navr')
