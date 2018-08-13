import sys
sys.path.append("..")

from src import QueueServer


async def aecho(info):
    print(info)


def echo(info):
    print(info)

HANDLERS_MAP = {
    'test_print': aecho
}


def test_server():
    server = QueueServer()
    server.add_handlers(HANDLERS_MAP)
    server.async_run(
        key='/test/simple/event', error_key='/error/simple/event')


if __name__ == "__main__":
    test_server()
