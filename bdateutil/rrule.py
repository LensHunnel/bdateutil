from dateutil.rrule import *
from dateutil.rrule import rrule as rrulebase
from dateutil.rrule import _rrulestr as rrulestrbase


BDAILY = 8


class rrule(rrulebase):

    def __init__(self, freq, **kwargs):
        if freq == BDAILY:
            rrulebase.__init__(self, DAILY, **kwargs)
            self._bdaily = True
            if self._count:
                self._count *= 2
        else:
            rrulebase.__init__(self, freq, **kwargs)
            self._bdaily = False

    def _iter(self):
        total = 0
        for i in rrulebase._iter(self):
            if self._bdaily:
                if i.weekday() < 5:
                    total += 1
                    if total > self._count / 2:
                        return
                    yield i
            else:
                yield i
        return


# dateutil.rrule.rrulestr returns a dateutil.rrule.rrule object
# RRuleTest.testStrType() from the original dateutil tests fails
# because dateutil.rrule.rrule is not an instance of bdateutil.rrule.rrule
# so we need to redefine rrulestr to return a bdateutil rrule object
class _rrulestr(rrulestrbase):

    def _parse_rfc_rrule(self, line, **kwargs):
        ret = rrulestrbase._parse_rfc_rrule(self, line, **kwargs)
        ret.__class__ = rrule
        ret._bdaily = False
        return ret


rrulestr = _rrulestr()
