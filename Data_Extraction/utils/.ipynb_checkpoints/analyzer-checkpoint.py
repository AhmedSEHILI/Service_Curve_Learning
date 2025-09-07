from .common import *
from .trace import *
from functools import lru_cache


class Job(tuple):

    def __new__ (cls, events):
        return super().__new__(cls, tuple(events))

    def __getattr__(self, name):
        # Lazy evaluation
        val = None
        match name:
            case 'activation':
                if isinstance(self[0], Activate):
                    val = self[0].ts
            case 'start':
                val = self[1].ts
                if isinstance(self[0], Run):
                    val = self[0].ts
            case 'end':
                val = self[-1].ts
            case 'jitter':
                if self.activation:
                    val = self.start - self.activation
            case 'xtime':
                val = 0
                for lhs, rhs in zip(self[:-1], self[1:]):
                    if isinstance(lhs, Run):
                        val += rhs.ts - lhs.ts
            case 'rtime':
                if self.activation:
                    val = self.end - self.activation
            case 'overdue':
                val = False
                for ev in self[1:]:
                    if isinstance(ev, Activate):
                        val = True
                        break
            case 'preemptions':
                val = []
                for lhs, rhs in zip(self[:-1], self[1:]):
                    if isinstance(lhs, Preempt):
                        val.append(rhs.ts-lhs.ts)
                if val:
                    val = tuple(val)
                else:
                    val = None
            case 'ptime':
                if self.preemptions:
                    val = sum(self.preemptions)
            case _:
                return None

        # Save result and return
        setattr(self, name, val)
        return getattr(self, name)


class JobAnalyzer(tuple):

    def __new__(cls, trace):
        return super().__new__(cls, trace)

    @lru_cache(maxsize=len(MODULES))
    def __getitem__(self, id):

        def is_type_of_interest(x):
            return any(isinstance(x, ty)
                       for ty in (Run, End, Activate, Preempt, Suspend))

        roi = (x for x in self
               if is_type_of_interest(x) and x.id == id)

        jobs = []
        for ev in roi:
            if 'segment' not in locals():
                if isinstance(ev, End):
                    segment = []
                continue

            segment.append(ev)

            if isinstance(ev, End):
                jobs.append(Job(segment))
                segment = []

        return tuple(jobs)

    @lru_cache(maxsize=len(MODULES))
    def build_overdue_trace(self):
        trace = []

        for id in range(len(MODULES)):
            for job in filter(lambda x: x.overdue, self[id]):
                trace.extend(Miss(x.ts, x.id)
                             for x in job[1:]
                             if isinstance(x, Activate))

        return Trace.from_unsorted_data(trace)
