class Cancelled(Exception):
    pass


class EventBase():
    def __init__(self):
        pass

    def cancell(self):
        self.cancelled = cancelled


class EventExplicit(EventBase):
    def __init__(self):
        super().__init__()

    def cancell(self):
        raise RuntimeError("This event is not cancellable!")
