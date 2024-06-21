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
                'host': os.environ.get('SPLUNK_HTTP_HOST', ''),
                'port': int(os.environ.get('SPLUNK_HTTP_PORT', '80')),
                'token': os.environ.get('SPLUNK_HTTP_TOKEN', ''),
                'https': bool(os.environ.get('SPLUNK_ENABLE_HTTPS', 'False').lower() == "true"),  # 可选, bool
                'timeout': int(os.environ.get('SPLUNK_HTTP_TIMEOUT', '120')),  # 可选, int
                'ssl_verify': bool(os.environ.get('SPLUNK_ENABLE_SSL_VERIFY', 'False').lower() == "true"), # 可选, bool
                "sourcetype": os.environ.get('SPLUNK_SOURCETYPE', ''), # 可选, sourcetype
                "index": os.environ.get('SPLUNK_INDEX', ''),           # 可选, index
                "source": os.environ.get('SPLUNK_SOURCE', ''),         # 可选, source
            }
            
            self.client = requests.session()
            self.client.max_redirects = 1
            self.client.verify = self.sink_config["ssl_verify"]
            self.client.headers['Authorization'] = "Splunk {}".format(self.sink_config['token'])
            self.url = "{0}://{1}:{2}/services/collector/event".format("http" if not self.sink_config['https'] else "https", self.sink_config['host'], self.sink_config['port'])

            self.default_fields = {}
            if self.sink_config.get("sourcetype"):
                self.default_fields['sourcetype'] = self.sink_config.get("sourcetype")
            if self.sink_config.get("source"):
                self.default_fields['source'] = self.sink_config.get("source")
            if self.sink_config.get("index"):
                self.default_fields['index'] = self.sink_config.get("index")
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
            for log in logs:
                # 发送数据到 Splunk
                event = {}
                event.update(self.default_fields)
                event['time'] = log[u'__time__']
                del log['__time__']

                json_topic = {"actiontrail_audit_event": ["event"]}
                topic = log.get("__topic__", "")
                if topic in json_topic:
                    try:
                        for field in json_topic[topic]:
                            log[field] = json.loads(log[field])
                    except Exception as ex:
                        pass
                event['event'] = json.dumps(log)
                data = json.dumps(event, sort_keys=True)

                req = self.client.post(self.url, data=data, timeout=self.sink_config["timeout"])
                req.raise_for_status()
        except Exception as err:
            logger.error("Failed to deliver logs to remote Splunk server ({0}). Exception: {1}".format(self.sink_config, err))
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