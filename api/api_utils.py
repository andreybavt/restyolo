import json
import time


class Timer:
    def __init__(self, caption=None, parent=None) -> None:
        self.intervals = {}
        self.caption = caption
        self.parent = parent

    def __call__(self, *args, **kwargs):
        return Timer(args[0], self)

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.interval = (self.end - self.start) * 1000
        self.parent.intervals[self.caption] = self.parent.intervals.get(self.caption, 0) + round(self.interval)

    def __repr__(self):
        return json.dumps(self.intervals)
