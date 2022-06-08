# -*- coding: utf-8 -*-
import logging
import json
import time
import os

import fc2

from kafka import KafkaClient
from multiprocessing import Process
from kafka.errors import KafkaError

logger = logging.getLogger()
logger.setLevel(level=logging.INFO)


def kafka_consumer_api_handler(context, trigger_consumer_params):
    try:
        creds = context.credentials
        # 实例化要请求产品的client对象，以及函数所在的地域
        client = fc2.Client(
            endpoint='https://%s.%s.fc.aliyuncs.com' % (context.account_id, context.region),
            accessKeyID=creds.access_key_id,
            accessKeySecret=creds.access_key_secret,
            securityToken=creds.security_token or '')

        response = client.invoke_function(trigger_consumer_params["consumer_service_name"],
                                          trigger_consumer_params["consumer_function_name"], json.dumps(trigger_consumer_params),
                                          headers={'x-fc-invocation-type': 'Async'})
        logger.info(response.data)
    except Exception as err:
        logger.error(err)


def handler(event, context):
    partitions = []
    try:
        start_time = int(time.time())
        logger.info("schedule start time: %s", str(start_time))
        ivk = json.loads(event)
        evt = json.loads(ivk["payload"])

        consumer_service_name = os.environ.get('consumer_service_name')
        topic_name = os.environ.get('topic_name')
        consumer_group_id = os.environ.get('consumer_group_id')
        kafka_instance_id = os.environ.get('kafka_instance_id')
        bucket_name = os.environ.get('bucket_name')
        kafka_endpoint = os.environ.get('kafka_endpoint')

        hosts = kafka_endpoint.split(',')

        client = KafkaClient(hosts)
        partitions = client.get_partition_ids_for_topic(topic_name)

        # 输出json格式的字符串回包
        logger.info("get topic attributes: %s", partitions)
        process_list = list()
        for partition_id in partitions:
            trigger_consumer_params = {
                "consumer_service_name": consumer_service_name,
                "consumer_function_name": evt["consumer_function_name"],
                "topic_name": topic_name,
                "consumer_group_id": consumer_group_id,
                "kafka_instance_id": kafka_instance_id,
                "bucket_name": bucket_name,
                "partition_id": partition_id,
                "kafka_endpoint": kafka_endpoint
            }
            logger.info("job-------:" + json.dumps(trigger_consumer_params))
            p = Process(target=kafka_consumer_api_handler, name='kafka_consumer_api_handler(%s)' % "",
                        args=(context, trigger_consumer_params))
            process_list.append(p)

        for p in process_list:
            p.start()

        for p in process_list:
            p.join()
        logger.info("schedule success end time: %s", str(int(time.time())))
    except KafkaError as err:
        logger.error(err)
        logger.info("schedule failed end time: %s", str(int(time.time())))

    return json.dumps(partitions)
