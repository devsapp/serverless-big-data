# -*- coding: utf-8 -*-
import json
import logging
import time
import os
import datetime

import oss2
from pykafka.exceptions import ConsumerStoppedException
from pykafka.client import KafkaClient
from pykafka.common import OffsetType
from kafka import KafkaConsumer
from kafka import TopicPartition


logger = logging.getLogger()
logger.setLevel(level=logging.INFO)


to_oss_bytes_up_limit = 1024 * 1024 * 500  # 每次最大投递oss包大小 500M
to_oss_bytes_down_limit = 1  # 每次最小投递oss包大小 1B
partition_max_timeout_ms_up_limit = 15 * 60 * 1000  # 最大timeout时间
partition_max_timeout_ms_down_limit = 5 * 60 * 1000  # 最小timeout时间
max_to_oss_time_s = 5  # 最小timeout时间
consumer_timeout_ms = 3000  # 默认partition多久时间没消息就退出
partition_max_to_oss_bytes = 6 * 1024 * 1024 # 6M
partition_max_timeout_ms = 10000 # 10s
offset_type = 'earliest'


class KafkaToOSS(object):
    '''
    消费kafka 投递oss
    '''

    def __init__(self, kafka_instance_id, topic_name, kafka_address, bucket_name,
                 partition_max_to_oss_bytes,
                 partition_max_timeout_ms, partition_id, consumer_timeout_ms, group_id, offset_type, context):
        self.topic_name = topic_name
        self.kafka_address = kafka_address
        self.kafka_instance_id = kafka_instance_id
        self.partition_max_to_oss_bytes = partition_max_to_oss_bytes
        self.partition_max_timeout_ms = partition_max_timeout_ms
        self.partition_id = partition_id
        self.consumer_timeout_ms = consumer_timeout_ms
        self.group_id = group_id
        self.offset_type = offset_type
        creds = context.credentials
        auth = oss2.StsAuth(
            creds.access_key_id,
            creds.access_key_secret,
            creds.security_token)

        # endpoint = 'oss-' + evt['region'] + '.aliyuncs.com'
        endpoint = 'oss-' + context.region + '-internal.aliyuncs.com'
        self.bucket = oss2.Bucket(auth, endpoint, bucket_name)

    # Generating file name. 生成写入文件名
    def object_key_generate(self):
        today = str(datetime.date.today())
        file_name = str(int(round(time.time() * 1000)))
        dir_name = "{}/{}/{}".format(str(self.kafka_instance_id), str(self.topic_name), today)
        object_key = '{}/{}'.format(dir_name, file_name)
        logger.info("generated key name: %s, dir: %s", object_key, dir_name)
        return object_key

    # Check if the file already exists. 检查文件是否已存在
    def check_oss_file(self, key):
        try:
            resp = self.bucket.head_object(key)
            logger.info("check_oss_file of resp is [%s]" % resp)
            return True
        except oss2.exceptions.NotFound as e:
            logger.info("e is [%s]" % e)
            return False
        except Exception as e:
            logger.info("unhandled exception [%s]" % e)
            logger.info(e)

    # Deleting local file. 删除本地文件
    def delete_local_file(self, src):
        try:
            logger.info("delete files and folders")
            if os.path.isfile(src):
                os.remove(src)
            elif os.path.isdir(src):
                for item in os.listdir(src):
                    item_src = os.path.join(src, item)
                    self.delete_local_file(item_src)
                os.rmdir(src)
        except Exception as err:
            logger.error("delete files and folders error: %s", err)
            pass

    # Uploading file to OSS. 上传文件到OSS
    def upload_local_file(self, local_path):
        start_time = int(time.time())
        logger.info("Start to upload time: %s", str(start_time))
        logger.info("local file sizes: %s", str(os.path.getsize(local_path)))

        if os.path.getsize(local_path) <= 0:
            logger.info("local file is empty")
            return True
        # 判断文件名是否存在
        if os.path.isfile(local_path):
            logger.info("local_filename is [%s]" % local_path)
            key = self.object_key_generate()
            while self.check_oss_file(key) is True:
                key = self.object_key_generate()
            logger.info("oss_object_name is: [%s]", key)
            response = self.bucket.put_object_from_file(key=key, filename=local_path)
            logger.debug("upload result is [%s]" % response)
            logger.info("upload osst time: %s", str(int(time.time()) - start_time))
            return True
        else:
            logger.error("Upload fail")
            return False

    # check params. 检查参数是否正确
    def param_check(self):
        if self.kafka_instance_id is None:
            return "kafka_instance_id is empty"
        if self.topic_name is None:
            return "topic_name is empty"
        if self.kafka_address is None:
            return "kafka_address is empty"
        if self.partition_max_to_oss_bytes is None:
            return "partition_max_to_oss_bytes is empty"
        if self.partition_max_timeout_ms is None:
            return "partition_max_timeout is empty"
        if self.consumer_timeout_ms is None:
            return "consumer_timeout_ms is empty"
        if self.offset_type is None:
            self.offset_type = "earliest"

        # 验证consumer_timeout_ms 取值
        self.consumer_timeout_ms = int(self.consumer_timeout_ms)
        if self.consumer_timeout_ms <= 0:
            self.consumer_timeout_ms = consumer_timeout_ms

        # 验证partition_max_to_oss_bytes 取值
        self.partition_max_to_oss_bytes = int(self.partition_max_to_oss_bytes)
        if self.partition_max_to_oss_bytes > to_oss_bytes_up_limit:
            self.partition_max_to_oss_bytes = to_oss_bytes_up_limit
        if self.partition_max_to_oss_bytes <= 0:
            self.partition_max_to_oss_bytes = to_oss_bytes_down_limit

        # 验证partition_max_timeout_ms 取值
        self.partition_max_timeout_ms = int(self.partition_max_timeout_ms)
        if self.partition_max_timeout_ms > partition_max_timeout_ms_up_limit:
            self.partition_max_timeout_ms = partition_max_timeout_ms_up_limit
        if self.partition_max_timeout_ms <= 0:
            self.partition_max_timeout_ms = partition_max_timeout_ms_down_limit

        return ""

    def calculation_max_to_oss_time(self):
        # 根据函数每次tooss的包大小（50M, 100M，150M，，500M）以及 tooss的带宽推算出对应tooss的最大预留时间
        if self.partition_max_to_oss_bytes > 50 * 1024 * 1024:
            return max_to_oss_time_s + (self.partition_max_to_oss_bytes / (50 * 1024 * 1024))
        else:
            return max_to_oss_time_s

    def worker(self):
        local_path = '/tmp/oss_file.txt'
        # local_path = os.getcwd() + '/local_file.txt'
        if os.path.exists(local_path):
            os.remove(local_path)
        os.mknod(local_path)
        f = open(local_path, 'w')
        max_to_oss_time = self.calculation_max_to_oss_time()
        start_time = int(time.time())
        logger.info("start time:%s", str(start_time))
        client = KafkaClient(hosts=self.kafka_address)
        msg_consumed_count = 0
        reset_offset_on_start_status = False
        topic = client.topics[self.topic_name.encode()]
        partitions = topic.partitions

        if self.offset_type.lower() == 'earliest':
            start_offset = OffsetType.EARLIEST
        elif self.offset_type.lower() == 'latest':
            start_offset = OffsetType.LATEST
        else:
            # 引用kafka库，解决pykafka fetch_offset_limits函数不能正确根据timestamp返回offset的问题
            start_offset = OffsetType.LATEST
            consumer = KafkaConsumer(self.topic_name, group_id=self.group_id, bootstrap_servers=[self.kafka_address])
            tp = TopicPartition(self.topic_name, self.partition_id)
            offsets = consumer.offsets_for_times({tp:int(self.offset_type)})
            if offsets[tp]:
                if offsets[tp].offset == 0:
                    start_offset = OffsetType.EARLIEST
                else:
                    committed = consumer._coordinator.fetch_committed_offsets([tp])
                    if not committed or (committed[tp] and committed[tp].offset < offsets[tp].offset):
                        start_offset = offsets[tp].offset - 1
                        reset_offset_on_start_status = True

        logger.info("consumer start offset on partition {} is {}".format(self.partition_id, start_offset))

        consumer = topic.get_simple_consumer(consumer_group=self.group_id,
                                             partitions={partitions.get(self.partition_id)},
                                             consumer_timeout_ms=self.consumer_timeout_ms,
                                             auto_commit_enable=False,
                                             auto_offset_reset=start_offset,
                                             reset_offset_on_start=reset_offset_on_start_status,
                                             )

        try:
            while True:
                msg = consumer.consume()
                if msg:
                    msg_consumed_count += 1
                    f.write(str(msg.value))
                    f.write("\n")
                if os.path.getsize(local_path) >= self.partition_max_to_oss_bytes:
                    logger.info("already reach partition_max_to_oss_bytes, file length: %s",
                                str(os.path.getsize(local_path)))
                    status = self.upload_local_file(local_path)
                    if status is False:
                        print("partition_max_to_oss_bytes failed to oss  time:" + str(int(time.time())))
                        return "partition_max_to_oss_bytes failed to oss"
                    consumer.commit_offsets()
                    f.seek(0)
                    f.truncate()
                if int(time.time()) - start_time >= self.partition_max_timeout_ms / 1000 - max_to_oss_time:
                    logger.info("already reach partition_max_timeout, osst time: %s",
                                str(int(time.time()) - start_time))
                    break
                if msg is None:
                    logger.info("already reach kafka consumer timeout, osst_time: %s",
                                str(int(time.time()) - start_time))
                    break

            f.close()
            logger.info("consumer finished, osst time: %s", str(int(time.time()) - start_time))
            logger.info("msg num: %s", str(msg_consumed_count))
            if msg_consumed_count > 0:
                status = self.upload_local_file(local_path)
                if status is False:
                    logger.error("failed to oss  time: %s", str(int(time.time())))
                    return "failed to oss"
            consumer.commit_offsets()
            consumer.stop()
            self.delete_local_file(local_path)
            logger.info("end time:%s", str(int(time.time())))
            return "success"
        except ConsumerStoppedException as err:
            logger.error("error:", str(err))
            logger.error("KafkaError failed consumer osst time: %s", str(int(time.time()) - int(start_time)))
            return "failed"


def handler(event, context):

    logger.info("invocation params: %s", event)
    evt = json.loads(event)

    topic_name = evt["topic_name"]
    group_id = evt["consumer_group_id"]
    partition_id = evt["partition_id"]
    kafka_instance_id = evt["kafka_instance_id"]
    bucket_name = evt["bucket_name"]
    hosts = evt["kafka_endpoint"]

    kafka_to_oss = KafkaToOSS(kafka_instance_id, topic_name, hosts, bucket_name,
                              partition_max_to_oss_bytes,
                              partition_max_timeout_ms,
                              partition_id,
                              consumer_timeout_ms,
                              group_id,
                              offset_type,
                              context
                              )
    err = kafka_to_oss.param_check()
    if err != "":
        logger.error("param error: %s", err)
    ret_msg = kafka_to_oss.worker()
    return ret_msg
