from event_bus import subscribe, post
from event import EventBase, EventExplicit


class SomeEvent(EventBase):
    def __init__(self, foo: int):
        super().__init__()
        self.foo = foo
        self.callback = None

    def set_callback(self, func):
        self.callback = func


@subscribe(event=SomeEvent)
def hook(event: SomeEvent):
    print(1)


@subscribe(event=EventBase)
def base(event: EventBase):
    print(2)


@subscribe(event=SomeEvent, priority=1)
def hook2(event: SomeEvent):
    #event.cancel()
    pass


inst = SomeEvent(1)
post(inst)
