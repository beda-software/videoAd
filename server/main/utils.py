from __future__ import unicode_literals

__author__ = 'lkot'


class Generator(object):
    def __init__(self, array):
        self.array = array
        self.index = 0

    def __getitem__(self, item):
        if isinstance(item, slice):
            if not self.array:
                return []
            start = item.start if item.start else 0
            self.index = (self.index + start) % len(self.array)
            return [self[0] for i in range(item.stop - start)]
        else:
            self.index = (self.index + item) % len(self.array)
            item = self.array[self.index]
            self.index = (self.index + 1) % len(self.array)
            return item