# coding: utf-8
# Date      : 2019/4/29
# Author    : kylin
# PROJECT   : aiocrawler
# File      : redis_exporter
import aioredis
import asyncio
import pickle
from typing import Iterable, List
from aiocrawler import Item
from aiocrawler import BaseSettings
from aiocrawler.extensions.exporters.exporter import BaseExporter


class RedisExporter(BaseExporter):
    def __init__(self, settings: BaseSettings, item_class: Item, loop: asyncio.AbstractEventLoop = None):
        BaseExporter.__init__(self, settings, item_class)
        self.loop = loop if loop else asyncio.get_event_loop()
        self.redis_pool: aioredis.ConnectionsPool = None
        self.redis_items_key = self.settings.REDIS_PROJECT_NAME + ':items'

    async def initialize_redis(self):
        if not self.settings.REDIS_URL:
            raise ValueError('REDIS_URL is not configured in {setting_name}'.format(
                setting_name=self.settings.__class__.__name__))
        else:
            self.logger.debug('Connecting to The Redis Server...')
            self.redis_pool = await aioredis.create_pool(self.settings.REDIS_URL, loop=self.loop)

    async def get_redis_items(self, start: int, end: int):
        items = await self.redis_pool.execute('lrange', self.redis_items_key, start, end)
        count = len(items)
        self.logger.debug(f'Got {count} items <{start}, {end}> from '
                          f'The Redis Server <redis key: {self.redis_items_key}>')
        items = map(lambda x: pickle.loads(x), items)
        items = self.__filter_items(items)
        return items

    def __filter_items(self, items: Iterable[Item]):
        for item in items:
            if item.__class__.__name__ == self.item_class_name:
                yield item

    async def get_total_count(self):
        count = await self.redis_pool.execute('llen', self.redis_items_key)
        return count
