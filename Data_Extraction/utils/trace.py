from .common import *


class Trace(tuple):

    def __new__(cls, data):
        return super().__new__(cls, tuple(data))

    @classmethod
    def from_unsorted_data(cls, data):
        data = list(data)
        data.sort(key=lambda x: x.ts)
        return cls.__new__(cls, data)

    @classmethod
    def from_scheduler(cls, path):

        def formatter(entry):

            split = list(map(int, entry.strip().split(',')))
            idx = split[2] & 0xF
            typ = split[2] >> 4
            ts = split[0]
            xt = split[1]

            yield Run(ts, idx)

            ts += xt # next timestamp is after execution time

            match typ: # run ends with...
                case 2: yield Preempt(ts, idx)
                case 4: yield Suspend(ts, idx)
                case _: yield End(ts, idx)

        return cls.from_unsorted_data(cls.gen_entries(path, formatter))

    @classmethod
    def from_activator(cls, path):

        def formatter(entry):
            yield Activate(*map(int, entry.strip().split(',')))

        return cls.__new__(cls, cls.gen_entries(path, formatter))

    @classmethod
    def from_mission_result(cls, path):

        def formatter(entry):
            split = list(map(int, entry.strip().split(',')))
            yield MissionItem(split[0], split[2])

        entries = Trace.gen_entries(path, formatter)
        roi = tuple(filter(lambda x: x.it >=0, entries))
        return cls.__new__(cls, roi)

    @staticmethod
    def gen_entries(path, formatter):
        with open(path, 'r') as csv:
            csv.readline() # pop first line
            for entry in csv:
                for formatted in formatter(entry):
                    yield formatted

    def __iter__(self):
        data = super().__iter__()

        if hasattr(self, 'lbound'):
            data = filter(lambda x: x.ts >= self.lbound, data)

        if hasattr(self, 'rbound'):
            data = filter(lambda x: x.ts <= self.rbound, data)

        return data

    def __gt__(self, lbound):
        self.lbound = lbound
        return self

    def __lt__(self, rbound):
        self.rbound = rbound
        return self

    def __add__(self, other):

        def funnel(tr_a, tr_b):
            neck = []
            silos = []

            # Prepare neck and silos
            for it in (iter(tr_a), iter(tr_b)):
                try:
                    neck.append(next(it))
                    silos.append(it)
                except StopIteration:
                    pass

            # Loop until all silos are empty
            while silos:
                ripe = neck.index(min(neck, key=lambda x: x.ts))
                yield neck[ripe]

                try:
                    neck[ripe] = next(silos[ripe])
                except StopIteration:
                    del neck[ripe]
                    del silos[ripe]

        fused = funnel(self, other)
        ret = super().__new__(Trace, tuple(fused))

        # Delete fused trace's origins
        del self, other

        return ret

    def __contains__(self, item):
        return any(isinstance(x, item) for x in self)
