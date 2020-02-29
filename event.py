class Cancelled(Exception):
    pass


class EventBase():
    def __init__(self):
        pass

    def cancel(self):
        raise Cancelled()


class EventCommon(EventBase):
    def __init__(self):
        super().__init__()

    class Cancelled(EventBase):
        def __init__(self, event):
            super().__init__()
            self.event = event

        def cancel(self):
            raise RuntimeError("This event is not cancellable!")


class EventExplicit(EventCommon):
    def __init__(self):
        super().__init__()

    def cancel(self):
        raise RuntimeError("This event is not cancellable!")
