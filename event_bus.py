from functools import partial, wraps
from event import EventBase, Cancelled
from inspect import signature

__eventbus__ = {}


def post(event: EventBase):
    triggered = [event.__class__]

    def recursive(clazz, trigger: list):
        for base in clazz.__bases__:
            if issubclass(base, EventBase) and \
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

    sig = signature(func)

    if len(sig.parameters) != 1 or len(anno_dict) != 1:
        raise TypeError(
            "Hook requires and only requires 1 annotated parameter!")

    event = anno_dict[0][1]

    if not issubclass(event, EventBase):
        raise TypeError("Event listening is not derived from EventBase!")

    if event not in __eventbus__:
        __eventbus__[event] = []

    __eventbus__[event].append((func, priority))
    __eventbus__[event].sort(key=lambda x: x[1], reverse=True)

    return func
