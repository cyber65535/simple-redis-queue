import sys
sys.path.append("..")


from src import QueueClient


def test_client():
    client = QueueClient()
    print(client.instance_keys)
    while 1:
        msg = input('event: ')
        if msg == '/quit':
            exit(0)
        client.publish('test_print', {'name': 'me', 'info': msg})


if __name__ == "__main__":
    test_client()
