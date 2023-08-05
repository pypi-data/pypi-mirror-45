#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@file: RedisUtils.py
@time: 2019/04/17
"""

# -*- coding: utf-8 -*-
# @Time    : 2019/4/16 下午8:52
# @File    : RedisUtils.py
# @Software: PyCharm


import traceback
from conf.log_handlers import log
from rediscluster import StrictRedisCluster
import sys

class RedisCluster(object):
    def __init__(self,redis_nodes):

        try:
            self.conn = StrictRedisCluster(startup_nodes=redis_nodes)
        except Exception as e:
            log.error("Connect Error:%s"%traceback.format_exc())
            self.conn =  False

    def redis_set(self,key,value,extime=""):
        '''
        set 类型
        :param key:
        :param value:
        :param extime:  失效时间
        :return: bool
        '''
        if not self.conn:
            return False
        if extime:
            return self.conn.set(key,value,extime)
        return self.conn.set(key,value)

    def redis_get(self,key):
        '''
        set 类型
        :param key:
        :return:   str
        '''
        if not self.conn:
            return False
        res = self.conn.get(key)
        if res:
            return res.decode("utf-8")
        else:
            return None

    def redis_del(self,key):
        '''
        除hash类型外多可以使用
        :param key:
        :return:  ==1 删除成功  ==0不存在或没删除成功
        '''
        if not self.conn:
            return False
        return self.conn.delete(key)

    def redis_hset(self,name,key,value):
        '''
        hash 类型
        :param key:
        :param value:
        :return: ==1  成功
        '''
        if not self.conn:
            return False
        return self.conn.hset(name,key,value)

    def redis_hget(self,name,key):
        '''
        hash 类型
        :param key:
        :param value:
        :return: None 未查到数据
        '''
        if not self.conn:
            return False
        res = self.conn.hget(name,key)
        if res:
            return res.decode("utf-8")
        return None

    def redis_hdel(self,name,keys):
        '''
        hash 类型
        :param key:
        :param value:
        :return: ==1 删除成功
        '''
        if not self.conn:
            return False
        return self.conn.hdel(name,keys)

    def redis_saddSet(self,name,*values):
        '''
        sadd 集合
        :param name:
        :param values:  可以一次添加多个
        :return:  ==1 添加成功
        '''
        if not self.conn:
            return False
        return self.conn.sadd(name,*values)

    def redis_smembers(self,name):
        '''
        集合查询使用
        :param name:
        :return:   返回一个列表
        '''
        if not self.conn:
            return False
        res = self.conn.smembers(name)
        if res:
            res_list = []
            for response in res:
                res_list.append(response.decode("utf-8"))
            return res_list
        return None

    def redis_zaddSet(self,name, *args):
        '''
        写入zadd集合
        :param name:
        :param args:   长度等于2
        :return:  ==1  成功
        '''
        if not self.conn:
            return False
        return self.conn.zadd(name, *args)

    def redis_zrangebyscore(self,name, min, max):
        '''
        查询zadd集合元素
        :param name:
        :param min:   开始
        :param max:   结束
        :return:  列表
        '''
        if not self.conn:
            return False
        res = self.conn.zrangebyscore(name,min,max)
        if res:
            res_list = []
            for response in res:
                res_list.append(response.decode("utf-8"))
            return res_list
        return None


    def redis_listSet(self,name, *values):
        '''
        list
        :param name:
        :param values:   可以一次添加多个
        :return:
        '''
        if not self.conn:
            return False
        return self.conn.lpush(name, *values)

    def redis_listGet(self,name, start, end):
        '''
        List
        :param name:
        :param start:   开始
        :param end:     结束
        :return:
        '''
        if not self.conn:
            return False
        res = self.conn.lrange(name, start, end)
        if res:
            res_list = []
            for response in res:
                res_list.append(response.decode("utf-8"))
            return res_list
        else:
            return None



if __name__ == '__main__':
    redis_obj = RedisCluster(redis_nodes)
    # log.info(redis_obj.redis_hset("hasss","111111","admin1"))
    # log.info(redis_obj.redis_hdel("hasss","111111"))
    log.info(redis_obj.redis_listSet("hasss",["111111","222"],"test3"))
    # log.info(redis_obj.redis_smembers("hasss"))
    # log.info(redis_obj.redis_zaddSet("hasssz","0",["test3","test4"]))
    print(redis_obj.redis_del("hasss"))

    log.info(redis_obj.redis_listGet("hasss",0,100))


    # print(redis_obj.redis_del("111111"))
    # log.info(redis_obj.redis_get("111111"))