# -*- coding: utf-8 -*-
import json
import logging
import os

import jinja2
from schema import Schema
from tablestore import BatchWriteRowRequest
from tablestore import Condition
from tablestore import OTSClient
from tablestore import PutRowItem
from tablestore import Row
from tablestore import RowExistenceExpectation
from tablestore import TableInBatchWriteRowItem

from env import OTS_SINK_CONFIG_SCHEMA

logger = logging.getLogger()


class OTSSink(object):

    def __init__(self, endpoint, access_key_id, access_key_secret, sts_token, instance_name, table_name,
                 primary_key_name, rows_name):
        self.endpoint = endpoint
        self.instance_name = instance_name
        self.table_name = table_name
        self.primary_key_name = primary_key_name
        self.rows_name = rows_name
        try:
            logger.info("ak: %s, secret: %s, token: %s", access_key_id, access_key_secret, sts_token)
            self.ots_client = OTSClient(endpoint, access_key_id, access_key_secret, instance_name, sts_token=sts_token)
        except Exception as e:
            logger.error(e)
            logger.error(
                "ERROR: Unexpected error: Could not create a ots_client from %s/%s", self.endpoint, self.instance_name)
            raise Exception(str(e))

    # get put row
    def get_row(self, evt):
        put_row_items = []
        pk = []
        cols = []
        print(type(self.primary_key_name))
        for key in self.primary_key_name:
            logger.info("get key: %s, list: %s, evt: %s", key, self.primary_key_name, evt)
            pk.append((key, evt[key]))
        for value in self.rows_name:
            logger.info("get value: %s, evt: %s", value, evt)
            cols.append((value, evt[value]))
        logger.info("pk: %s, col: %s", pk, cols)
        row = Row(pk, cols)
        condition = Condition(RowExistenceExpectation.IGNORE)
        item = PutRowItem(row, condition)
        put_row_items.append(item)
        return put_row_items

    def produce_to_ots(self, data):
        try:
            request = BatchWriteRowRequest()
            request.add(TableInBatchWriteRowItem(self.table_name, data))
            resp = self.ots_client.batch_write_row(request)
            logger.info('Result all succeed: %s' % (resp.is_all_succeed()))
            succ, fail = resp.get_put()
            for item in succ:
                logger.info('Put succeed, consume %s write cu.' % item.consumed.write)
            for item in fail:
                logger.error('Put failed, error code: %s, error message: %s' % (item.error_code, item.error_message))
            if resp.is_all_succeed() is False:
                return False
        except Exception as e:
            logger.error(e)
            logger.error("ERROR: Unexpect error while produce message to tablestore")
            return False
        return True


def initializer(context):
    endpoint = os.environ.get('endpoint')
    instance_name = os.environ.get('instance_name')
    table_name = os.environ.get('table_name')
    primary_keys_name = os.environ.get('primary_keys_name')
    rows_name = os.environ.get('rows_name')
    creds = context.credentials

    sink_config = {
        'endpoint': endpoint,
        'instance_name': instance_name,
        'table_name': table_name,
        'primary_keys_name': primary_keys_name.split(','),
        'rows_name': rows_name.split(','),
        'access_key_id': creds.access_key_id,
        'access_key_secret': creds.access_key_secret,
        'security_token': creds.security_token
    }

    if not Schema(OTS_SINK_CONFIG_SCHEMA, ignore_extra_keys=True).is_valid(sink_config):
        logger.error("validate failed error: %s", Schema(OTS_SINK_CONFIG_SCHEMA, ignore_extra_keys=True).validate(sink_config))
        raise Exception("SINK_CONFIG validate failed")

    global ots_sink
    ots_sink = OTSSink(sink_config['endpoint'],
                       creds.access_key_id,
                       creds.access_key_secret,
                       creds.security_token,
                       sink_config['instance_name'],
                       sink_config['table_name'],
                       sink_config['primary_keys_name'],
                       sink_config['rows_name'])


# deal message and return it
def deal_message(record):
    return record


def handler(event, context):

    # processing data
    evt = json.loads(event)
    logger.info("incoming event: %s", evt)
    # FIXME batch insert
    rows = ots_sink.get_row(evt['data'])
    success = ots_sink.produce_to_ots(rows)
    if success is False:
        logger.error("insert ots failed.")
        return "failed"
    return {"success": success}