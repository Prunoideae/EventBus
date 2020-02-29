from event_bus import subscribe, post
from event import EventBase, EventExplicit, EventCommon


class SomeEvent(EventCommon):
    def __init__(self, foo: int):
        super().__init__()
        self.foo = foo
        self.callback = None

    def set_callback(self, func):
        self.callback = func


@subscribe
def cancel_hook(event: SomeEvent.Cancelled):
    print("Event was cancelled!")


@subscribe
def cancelled_hook(event: SomeEvent):
    print("I'm not being called!")


@subscribe(priority=2)
def survivor(event: SomeEvent):
    print("I'm printed before cancelled!")


@subscribe(priority=1)
def killer(event: SomeEvent):
    event.cancel()
    pass


inst = SomeEvent(1)
post(inst)
