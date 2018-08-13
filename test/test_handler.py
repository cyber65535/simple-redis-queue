from enum import IntEnum
import sys
sys.path.append("..")


async def aecho(name, info):
    print(name + ':' + info)


def echo(info):
    print(info)


class EventEnum(IntEnum):
    test = 1


HANDLERS_MAP = {
    'test_print': aecho
}
