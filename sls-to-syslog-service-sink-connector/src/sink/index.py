# -*- coding: utf-8 -*-
import json
import os
import logging
import six
from datetime import datetime

from aliyun.log import LogClient
from aliyun.log import PullLogResponse
from aliyun.log.ext import syslogclient
from pysyslogclient import SyslogClientRFC5424 as SyslogClient

logger = logging.getLogger()


class Sink(object):
    """Sink Class.

    The main class deal with the incoming message and put to sink target.
    """

    def __init__(self):
        """Class Initializer. Initialization should realized in connect method.

        Args:
            None

        Returns:
            None

        Raises:
            None
        """
        self.connected = False

    def connect(self):
        """Sink connector construct method.
        Args:
            sink_config: config of this sink connector

        Returns:
            None

        Raises:
            None
        """
        try:
            self.sink_config = {
                'host': os.environ.get('SYSLOG_HOST', ''),
                'port': int(os.environ.get('SYSLOG_PORT', '514')),
                'protocol': os.environ.get('SYSLOG_PROTOCOL', 'tcp'),
                "facility": syslogclient.FAC_USER,  # 可选，可以参考其他syslogclient.FAC_*的值。
                "severity": syslogclient.SEV_INFO,  # 可选，可以参考其他syslogclient.SEV_*的值。
                "hostname": "aliyun.example.com",  # 可选，机器名，默认选择本机机器名。
                "tag": "tag"  # 可选，标签，默认是短划线（-）。
            }
            self.client = SyslogClient(self.sink_config.get('host'), self.sink_config.get('port'), self.sink_config.get('protocol'))
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
                # suppose we only care about audit log
                timestamp = datetime.fromtimestamp(int(log[u'__time__']))
                del log['__time__']

                io = six.StringIO()
                # 可以根据需要修改格式化内容，这里使用Key=Value传输，并使用默认的双竖线（||）进行分割。
                for k, v in six.iteritems(log):
                    io.write("{0}{1}={2}".format('||', k, v))

                data = io.getvalue()

                # 可以根据需要修改facility或者severity。
                self.client.log(data,
                           facility=self.sink_config.get("facility", None),
                           severity=self.sink_config.get("severity", None),
                           timestamp=timestamp,
                           program=self.sink_config.get("tag", None),
                           hostname=self.sink_config.get("hostname", None))
        except Exception as err:
            logger.debug("Failed to connect to remote syslog server ({0}). Exception: {1}".format(self.sink_config, err))
            # 需要添加一些错误处理的代码，例如重试或者通知等。
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