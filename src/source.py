#!/usr/bin/env python
# coding: utf-8
import sys
import traceback
import asyncio
from redis import StrictRedis
from json import loads, dumps


__author__ = "Jiao <cyber65535@gmail.com>"


class QueueServer(object):

    HANDLERS_MAP = {}

    def __init__(self, host='localhost', port=6379, db=0, password=None):
        self.db = db
        self.redis = StrictRedis(
            host=host, port=port, db=db, password=password,
            decode_responses=True
        )
        status = self.redis.config_set('notify-keyspace-events', 'AKE')
        print("SET notify-keyspace-events AKE is", status)

    def execute_handler(self, event_key, **kwargs):
        handler = self.HANDLERS_MAP.get(event_key, None)
        if handler:
            print(f'exec: {event_key}')
            handler(**kwargs)
        else:
            print(f'No handler for {event_key}')

    def listen(self, key, error_key):
        pubsub = self.redis.pubsub()
        pubsub.psubscribe(f'__keyspace@{self.db}__:{key}')
        for msg in pubsub.listen():
            if msg.get('data') != 'lpush':
                continue
            event = self.redis.rpoplpush(key, error_key)
            while event:
                try:
                    event_data = loads(event)
                    event_key = event_data.pop('event_handler_key')
                    self.execute_handler(event_key, **event_data)
                    self.redis.lrem(error_key, 0, event)  # rem safe bak
                except Exception as err:
                    print(err)
                    print(''.join(traceback.format_exception(*sys.exc_info())))
                event = self.redis.rpoplpush(key, error_key)
            self.redis.lrem(error_key, 0, event)  # rem safe bak

    async def async_execute_handler(self, event_key, **kwargs):
        handler = self.HANDLERS_MAP.get(event_key, None)
        if handler:
            print(f'exec: {event_key}')
            await handler(**kwargs)
        else:
            print(f'No handler for {event_key}')

    async def async_listen(self, key, error_key):
        pubsub = self.redis.pubsub()
        pubsub.psubscribe(f'__keyspace@{self.db}__:{key}')
        for msg in pubsub.listen():
            if msg.get('data') != 'lpush':
                continue
            event = self.redis.rpoplpush(key, error_key)
            while event:
                try:
                    event_data = loads(event)
                    event_key = event_data.pop('event_handler_key')
                    await self.async_execute_handler(event_key, **event_data)
                    self.redis.lrem(error_key, 0, event)  # rem safe bak
                except Exception as err:
                    logging.error(err)
                    print(''.join(traceback.format_exception(*sys.exc_info())))
                event = self.redis.rpoplpush(key, error_key)
            self.redis.lrem(error_key, 0, event)  # rem safe bak

    def add_handlers(self, handler_map):
        self.HANDLERS_MAP.update(handler_map)

    def async_run(self, key='/eventbus', error_key='/error/event'):
        io_loop = asyncio.get_event_loop()
        io_loop.run_until_complete(self.async_listen(key, error_key))

    def run(self, key='/eventbus', error_key='/error/event'):
        self.listen(key, error_key)


class QueueClient(object):

    def __init__(self, host='localhost', port=6379, db=0, password=None,
                 key='/eventbus', error_key='/error/event'):
        """key and error_key is redis-list"""
        self.key = key
        self.error_key = error_key
        self.redis = StrictRedis(
            host=host, port=port, db=db, password=password,
            decode_responses=True
        )

    def publish(self, event_handler_key, data):
        data['event_handler_key'] = event_handler_key
        self.redis.lpush(self.key, dumps(data))

    def push_error(self, data):
        self.redis.lpush(self.error_key, data)
