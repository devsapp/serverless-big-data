# -*- coding: utf-8 -*-
import json
import os
import logging
import requests

from aliyun.log import LogClient
from aliyun.log import PullLogResponse

logger = logging.getLogger()

class Sink(object):
    def __init__(self):
        self.connected = False

    def connect(self):
        try:
            self.sink_config = {
                "dataway": os.environ.get('GUANCE_DATAWAY', ''),
                "token": os.environ.get('GUANCE_TOKEN', ''),
                "measurement": os.environ.get('GUANCE_MEASUREMENT', ''), 
                "timeout": int(os.environ.get('GUANCE_HTTP_TIMEOUT_IN_SECOND', '600')), # 可选
            }

            if self.sink_config["timeout"] > 600:
                self.sink_config["timeout"] = 600
 
            self.client = requests.session()
            self.client.headers = {
                'Content-Type': 'application/json',
            }
            self.client.max_redirects = 1
            self.url = "https://{0}/v1/write/logging?token={1}".format(self.sink_config['dataway'], self.sink_config['token'])

            self.default_fields = {}
            if self.sink_config.get("measurement"):
                self.default_fields['measurement'] = self.sink_config.get("measurement")
        except Exception as e:
            logger.error(e)
            raise Exception(str(e))
        self.connected = True

    def is_connected(self):
        return self.connected

    def deliver(self, shard_id, log_groups):
        logs = PullLogResponse.loggroups_to_flattern_list(log_groups, time_as_str=True, decode_bytes=True)
        logger.info("Get data from shard {0}, log count: {1}".format(shard_id, len(logs)))
        try:
            post_data_list = []
            for log in logs:
                event = {}
                event.update(self.default_fields)
                event['time'] = int(log[u'__time__'])*1000*1000*1000
                del log['__time__']
                
                event['tags'] = {}
                event['fields'] = {}

                for key, value in log.items():
                    event['fields'][key] = value

                post_data_list.append(event)
                
            if len(post_data_list) != 0:
                data = json.dumps(post_data_list)
                req = self.client.post(self.url, data=data, timeout=self.sink_config["timeout"])
                req.raise_for_status()
        except Exception as err:
            logger.error("Failed to deliver logs to remote guance server. Exception: {0}".format(err))
            raise err
        logger.info("Complete send data to remote")
    
sink = Sink()

def initialize(context):
    logger.info('initializing sink connect')
    sink.connect()

def handler(event, context):
    if not sink.is_connected():
        try:
            sink.connect()
        except Exception as e:
            raise Exception("unconnected sink target")

    request_body = json.loads(event.decode())
    logger.info(request_body)

    if request_body['source'] == "test":
        # only for test
        return 'success'

    # Get the name of log project, the name of log store, the endpoint of sls, begin cursor, end cursor and shardId from event.source
    source = request_body['source']
    log_project = source['projectName']
    log_store = source['logstoreName']
    endpoint = source['endpoint']
    begin_cursor = source['beginCursor']
    end_cursor = source['endCursor']
    shard_id = source['shardId']

    creds = context.credentials
    client = LogClient(endpoint=endpoint,
                       accessKeyId=creds.access_key_id,
                       accessKey=creds.access_key_secret,
                       securityToken=creds.security_token)


    # Read data from source logstore within cursor: [begin_cursor, end_cursor) in the example, which contains all the logs trigger the invocation
    while True:
        response = client.pull_logs(project_name=log_project,
                                    logstore_name=log_store,
                                    shard_id=shard_id,
                                    cursor=begin_cursor,
                                    count=100,
                                    end_cursor=end_cursor,
                                    compress=False)
        log_group_cnt = response.get_loggroup_count()
        if log_group_cnt == 0:
            break
        logger.info("get %d log group from %s" % (log_group_cnt, log_store))
        sink.deliver(shard_id, response.get_loggroup_list())
        begin_cursor = response.get_next_cursor()

    return 'success'