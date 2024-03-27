# -*- coding: utf-8 -*-
import json
import logging
import os
import time

import jinja2
import oss2
from oss2 import exceptions
from schema import Schema

from env import OSS_SINK_CONFIG_SCHEMA

logger = logging.getLogger()


class OSSSink(object):

    def __init__(self, endpoint, bucket, object_prefix, access_key_id,
                 access_key_secret, security_token):
        self.endpoint = endpoint
        self.bucket = bucket
        self.object_prefix = object_prefix

        auth = oss2.StsAuth(access_key_id, access_key_secret, security_token)
        self.bucket_client = oss2.Bucket(auth, endpoint, bucket)

    # generate oss key name for kafka record
    def generate_oss_key_name(self):
        return self.object_prefix + "_" + str(int(time.time()))

    # get content from message
    def get_content(self, record):
        return json.dumps(record)

    # check if oss key is exist
    def oss_file_exist(self, key):
        try:
            self.bucket_client.get_object_meta(key)
        except exceptions.NoSuchKey as err1:
            return False, None
        except Exception as err2:
            logger.error("get oss key {%s} failed, err: %s", key, err2)
            return False, err2
        logger.info("file already exist, oss key: %s", key)
        return True, None

    # upload content to oss
    def upload_oss(self, content, filename):
        exist, e = self.oss_file_exist(filename)

        if e is not None:
            logger.error("upload oss abort, check file failed: %s", e)
            return False
        if exist:
            logger.error("upload oss abort, %s is exist in %s", filename, self.bucket)
            return False
        response = self.bucket_client.put_object(filename, content)
        if response.status != 200:
            logger.error("upload oss failed, response: %s", response)
            return False
        return True


def initializer(context):
    endpoint = os.environ.get('endpoint')
    bucket = os.environ.get('bucket')
    object_prefix = os.environ.get('object_prefix')
    creds = context.credentials

    sink_config = {
        'endpoint': endpoint,
        'bucket': bucket,
        'object_prefix': object_prefix,
        'access_key_id': creds.access_key_id,
        'access_key_secret': creds.access_key_secret,
        'security_token': creds.security_token
    }

    if not Schema(OSS_SINK_CONFIG_SCHEMA, ignore_extra_keys=True).is_valid(sink_config):
        logger.error("validate failed error: %s", Schema(OSS_SINK_CONFIG_SCHEMA, ignore_extra_keys=True).validate(sink_config))
        raise Exception("SINK_CONFIG validate failed")


    global oss_sink
    oss_sink = OSSSink(endpoint,
                       bucket,
                       object_prefix,
                       creds.access_key_id,
                       creds.access_key_secret,
                       creds.security_token)


def handler(event, context):
    # processing data 数据处理
    evt = json.loads(event)
    logger.info("incoming event: %s", evt)

    filename = oss_sink.generate_oss_key_name()
    data = oss_sink.get_content(evt)
    success = oss_sink.upload_oss(data, filename)

    return {"success": success}
