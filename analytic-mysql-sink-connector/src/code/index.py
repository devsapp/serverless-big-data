#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ast
import logging
import os
import json
from schema import Schema
import pymysql
import cloudevents

from env import ADB_MYSQL_SINK_CONFIG_SCHEMA

logger = logging.getLogger()
logger.setLevel(logging.INFO)

message_schema = {
    'id': str,
}


class VerifyException(Exception): pass


class Sink(object):
    """
    将数据发送到ADB
    """
    # Initialize the specific sink with the SINK_CONFIG
    def __init__(self):
        try:
            host = os.environ.get('host')
            port = os.environ.get('port')
            user = os.environ.get('user')
            password = os.environ.get('password')
            database = os.environ.get('database')
            sink_config = json.dumps({'host': host,'port':int(port),'user':user,'password':password,'database':database}) # os.environ["SINK_CONFIG"]
            env = json.loads(sink_config)
            if not Schema(ADB_MYSQL_SINK_CONFIG_SCHEMA, ignore_extra_keys=True).is_valid(env):
                Schema(ADB_MYSQL_SINK_CONFIG_SCHEMA, ignore_extra_keys=True).validate(env)
                raise VerifyException("env validate failed")
            self.config = ast.literal_eval(sink_config)
            self.conn = None
            print(self.config)
        except Exception as e:
            logger.error(e)
            logger.error(
                "ERROR: Unexpected error: Could not get the mandatory sink config.")
            raise Exception(str(e))

    # Connect the sink target with with sink config, we coud place this logic in __init__ phase also
    def connect(self):
        try:
            self.conn = pymysql.connect(
                host=self.config["host"],
                port=self.config["port"],
                user=self.config["user"],
                passwd=self.config["password"],
                db=self.config["database"],
                connect_timeout=5
            )
        except Exception as e:
            logger.error(e)
            logger.error(
                "ERROR: Unexpected error: Could not connect to MySql instance.")
            raise Exception(str(e))

    # deal the message, 这里可以对消息进行处理后返回
    def deal_message(self, ori_message):
        validate_message_schema(ori_message)
        return ori_message["data"];  

    # Write a entity to db table
    def write(self, ori_message):
        """
        发送消息
        CREATE Table Data (
            id BIGINT primary key NOT NULL AUTO_INCREMENT,
            data TEXT(256)
        )
        """
        sql = "INSERT INTO Data(data) VALUES ('%s') " % (json.dumps(ori_message))
        print(sql)
        with self.conn.cursor() as cursor:
            cursor.execute(sql)
            self.conn.commit()
            result = cursor.fetchall()
            print(result)
            return result

    def close(self):
        pass

    def is_connected(self):
        return True


def validate_message_schema(message):
    return Schema(message_schema, ignore_extra_keys=True).validate(message)


sink = Sink()


def initializer(context):
    logger.info('initializing sink connect')
    # how to resume connection when resumed from snapshot?
    sink.connect()


# 函数入口
def handler(event, context):
    if not sink.is_connected():
        sink.connect()

    # event 要求为 cloud event，校验
    evt = json.loads(event)
    # todo: check the cloud event 需要确定 event 格式，是 binary 还是 json

    print("handler event: ", evt)
    body = sink.deal_message(evt)
    sink.write(body)
    return {"result": "success"}


def destroy(context):
    logger.info('stop sink connection')
    sink.close()
