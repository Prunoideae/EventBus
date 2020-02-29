class Cancelled(Exception):
    pass


class EventBase():
    def __init__(self):
        pass

    def cancel(self):
        raise Cancelled()


class EventExplicit(EventBase):
    def __init__(self):
        super().__init__()

    def cancel(self):
        raise RuntimeError("This event is not cancellable!")
