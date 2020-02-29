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
    def bar():
        print(1)
    event.set_callback(bar)

inst = SomeEvent(1)
post(inst)
inst.callback()
