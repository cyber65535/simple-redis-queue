import sys
sys.path.append("..")


from src import QueueClient


def test_client():
    while 1:
        client = QueueClient(
            key='/test/simple/event', error_key='/error/simple/event')
        r = input('event: ')
        if r == '/quit':
            exit(0)
        client.publish('test_print', {'info': r})


if __name__ == "__main__":
    test_client()
