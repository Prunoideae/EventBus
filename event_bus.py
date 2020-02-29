from functools import partial, wraps
from event import EventBase, Cancelled

__eventbus__ = {}


def post(event: EventBase):
    triggered = [event.__class__]

    def recursive(clazz, trigger: list):
        for base in clazz.__bases__:
            if isinstance(base, EventBase.__class__) and \
                base not in trigger and \
                    base != object:
                trigger.append(base)
                recursive(base, trigger)

    recursive(event.__class__, triggered)

    triggered = [x for x in triggered if x in __eventbus__]

    try:
        for t in triggered:
            for hook in __eventbus__[t]:
                hook[0](event)
    except Cancelled:
        pass


def subscribe(func=None, *, priority=0):
    if func is None:
        return partial(subscribe, priority=priority)

    anno_dict = list(func.__annotations__.items())

    if len(anno_dict) != 1:
        raise TypeError("Hook requires only 1 parameter!")

    event = anno_dict[0][1]

    if not issubclass(event, EventBase):
        raise TypeError("Event listening is not derived from EventBase!")
    if not isinstance(event, EventBase.__class__):
        raise TypeError("Event type must be an instance of EventBase!")

    if event not in __eventbus__:
        __eventbus__[event] = []

    __eventbus__[event].append((func, priority))
    __eventbus__[event].sort(key=lambda x: x[1], reverse=True)

    return func
