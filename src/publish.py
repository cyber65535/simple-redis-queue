# coding: utf-8

from redis import StrictRedis


class Client(object):

    def __init__(self, host='localhost', port=6379, db=0, password=None):
        self.db = db
        self.redis = StrictRedis(host=host, port=port, db=db, password=password)
        status = self.redis.config_set('notify-keyspace-events', 'AKE')
        print("SET notify-keyspace-events AKE is", status)

    async def listen(self, key='/eventbus', error_key='/error/event'):
        pubsub = self.redis.pubsub()
        pubsub.psubscribe(f'__keyspace@{self.db}__:/{key}')
        for msg in pubsub.listen():
            if msg.get('data') != 'lpush':
                continue
            event = redis_conn.rpop(key)
            while event:
                try:
                    event_data = loads(event)
                    print(event_data)
                    event_category = event_data.pop('event_category')
                    await execute_handler(event_category, **event_data)
                except BaseException as err:
                    redis_conn.lpush(error_key, event)
                    logging.error(err)
                    print(''.join(traceback.format_exception(*sys.exc_info())))
                event = redis_conn.rpop(key)


    async def safe_listen(self):
        pubsub = self.redis.pubsub()
        pubsub.psubscribe(f'__keyspace@{self.db}__:/{key}')
        for msg in pubsub.listen():
            if msg.get('data') != 'lpush':
                continue
            event = redis_conn.rpoplpush('/eventbus', '/error/event')
            while event:
                try:
                    event_data = loads(event)
                    print(event_data)
                    event_category = event_data.pop('event_category')
                    yield execute_handler(event_category, **event_data)
                    redis_conn.lrem('/error/event', event)  # rem safe bak
                except BaseException as err:
                    logging.error(err)
                    print(''.join(traceback.format_exception(*sys.exc_info())))
                event = redis_conn.rpoplpush('/eventbus', '/error/event')
            redis_conn.lrem('/error/event', event)  # rem safe bak
