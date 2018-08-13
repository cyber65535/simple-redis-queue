import sys
sys.path.append("..")

from src import QueueServer

async def aecho(name, info):
    print(name + ':' + info)


def echo(info):
    print(info)


HANDLERS_MAP = {
    'test_print': aecho
}


def test_server():
    server = QueueServer()
    print(server.instance_keys)
    server.add_handlers(HANDLERS_MAP)
    server.async_listen()


if __name__ == "__main__":
    test_server()
