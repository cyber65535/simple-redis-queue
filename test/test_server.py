from srqueue import SimpleQueue

async def aecho(name, info):
    print(name + ':' + info)


def echo(info):
    print(info)


HANDLERS_MAP = {
    'test_print': aecho
}


def test_server():
    que = SimpleQueue()
    print(que.server.instance_keys)
    que.server.add_handlers(HANDLERS_MAP)
    que.server.alisten()


if __name__ == "__main__":
    test_server()
