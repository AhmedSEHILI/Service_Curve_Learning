from .common import *
import vcd


def dump_vcd(trace):

    init = trace[0].ts

    with open("dump.vcd", 'w') as dumpfile, \
         vcd.VCDWriter(dumpfile, timescale='1 us', init_timestamp=init) as writer:

        if Run in trace:
            jobs = tuple(writer.register_var('jobs', m, 'wire', size=1) for m in MODULES)
        if Activate in trace:
            activations = tuple(writer.register_var('activations', m, 'event') for m in MODULES)
        if Miss in trace:
            violations = tuple(writer.register_var('violations', m, 'event') for m in MODULES)

        # Initialize all at wires at 0
        for i in range(len(MODULES)):
            writer.change(jobs[i], init, 0)

        for entry in trace:
            match entry:
                case Activate(ts, id):
                    writer.change(activations[id], ts, 1)
                case Run(ts, id):
                    writer.change(jobs[id], ts, 1)
                case End(ts, id):
                    writer.change(jobs[id], ts, 0)
                case Preempt(ts, id):
                    writer.change(jobs[id], ts, 'X')
                case Suspend(ts, id):
                    writer.change(jobs[id], ts, 'Z')
                case Miss(ts, id):
                    writer.change(violations[id], ts, 1)
                case _: pass


def make_gtkw(modules, markers=None):

    with open("diagram.gtkw", 'w') as gtkwfile:
        save = vcd.gtkw.GTKWSave(gtkwfile)

        save.dumpfile("dump.vcd", False)
        save.sst_expanded(False)

        for module in modules:
            save.trace('jobs.' + module)
            save.trace('activations.' + module)
            save.trace('violations.' + module, color='red')

        if markers:
            markers = {chr(97 + i): val for (i, val) in enumerate(markers)}
            save.zoom_markers(-13, markers['a'], **markers)
