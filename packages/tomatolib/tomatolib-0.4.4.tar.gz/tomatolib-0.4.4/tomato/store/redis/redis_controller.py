#!/usr/bin/python
# -*- coding:utf-8 -*-

"""
    @file:      redis_controller.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @auther:    steven(love.as.string@gmail.com)
    @date:      March 15, 2019
    @desc:      RedisController
"""

import logging
import datetime
from tomato.util.application import Application


class RedisController(object):

    def __init__(self):
        self.__redis_client = Application()['redis']

    def __getattr__(self, attr):
        return getattr(self.__redis_client, attr)

    async def zcard(self, key):
        return await self.__redis_client.execute('zcard', key)

    async def zrank(self, key, member):
        return await self.__redis_client.execute('zrank', key, member)

    async def zadd(self, key, score, member):
        return await self.__redis_client.execute('zadd', key, score, member)

    async def zrangebyscore(self, key, min, max, withscores=None):
        return await self.__redis_client.execute('zrangebyscore', key,
            min, max, withscores)

    async def zrevrangebyscore(self, key, max, min, withscores=None):
        return await self.__redis_client.execute('zrevrangebyscore', key,
            max, min, withscores)

    async def lpush(self, key, *values):
        await self.__redis_client.execute('LPUSH', key, *values)

    async def hset(self, name, field, value):
        await self.__redis_client.execute('HSET', name, field, value)

    async def hset(self, name, field, value):
        await self.__redis_client.execute('HSET', name, field, value)

    async def hset(self, name, field, value):
        await self.__redis_client.execute('HSET', name, field, value)
