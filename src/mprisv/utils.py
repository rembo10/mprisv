import os
import pathlib
from functools import reduce

from dbus_next.aio import MessageBus

introspection_dir=pathlib.Path(pathlib.Path(__file__).parent.absolute(), 'introspection')

def get_introspection(name: str) -> str:
    with open(pathlib.Path(introspection_dir, f'{name}.xml'), 'r') as f:
        return f.read()

def get_ifaces(bus: MessageBus, name: str, kind: str, path: str, ifaces: list[str]):
    introspection = get_introspection(kind)
    obj = bus.get_proxy_object(name, path, introspection)
    return map(lambda x: obj.get_interface(x), ifaces)

def is_mpris(name: str) -> bool:
    return name.startswith('org.mpris.MediaPlayer2.')

def is_headphones(xs):
    return reduce(lambda acc, x: acc or 'MediaTransport' in x, xs, False)
