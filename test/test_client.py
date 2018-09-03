from srqueue import SimpleQueue


def test_client():
    que = SimpleQueue()
    print(que.client.instance_keys)
    while 1:
        msg = input('event: ')
        if msg == '/quit':
            exit(0)
        que.client.publish('test_print', {'name': 'me', 'info': msg})


if __name__ == "__main__":
    test_client()
