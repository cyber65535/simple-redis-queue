# simple-redis-queue
A simple redis queue


# Guide

Install Package

```
$git clone https://github.com/cyber65535/simple-redis-queue

$cd simple-redis-queue

$python setup.py install
```

Import Package

```
import srqueue
```

Use

```
# init config  : File A
srque = srqueue.SimpleQueue(host, port, db, password, key, error_key)

# server       : File B
def some_func(name, words):
    print("{}: {}".format(name, words))

srque.add_handler({"echo": some_func})
srque.listen()

# client       : File C
words = "println some word"
data = {
    "words": "Hello Queue!",
    "name": "Joy"
}
srque.client.publish("echo", data)
```

If async

```
srque = srqueue.SimpleQueue(host, port, db, password, key, error_key)

# server
async def some_func(words):            # async func
    print(words)

srque.add_handler({"echo": some_func})
srque.alisten()                        # alisten

# client (other file)
words = "println some word"
srque.client.publish("echo", words)
```

Another way to initialize the Class

```
# server
from srqueue import QueueServer

srque_server = QueueServer(host, port, db, password, key, error_key)

srque.add_handler({event_handler_key: some_func})
srque.listen()


# client
from srqueue import ClientClient

srque_client = QueueClient(host, port, db, password, key, error_key)
srque_client.pushlish(event_handler_key, data)
```
