# -*- coding: utf-8 -*-
import json
import logging
import os
import traceback
from retrying import retry

from confluent_kafka import Producer

from schema import Schema

import sink_schema
import transform

logger = logging.getLogger()
default_retry_times = 3


def retry_on_exception(exception):
    """if the result needes to be retried.

    Args:
        exception: function call exception

    Returns:
        Bool, if retrable, return True otherwise return False

    Raises:
        None
    """
    logger.error("got exception")
    traceback.print_exc()
    return isinstance(exception, BufferError)


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

    def connect(self, sink_config):
        """Sink connector construct method.
            todo: User should realize this method

        Args:
            sink_config: config of this sink connector

        Returns:
            None

        Raises:
            None
        """
        self.sink_config = sink_config

        try:
            conf = {
                'bootstrap.servers': sink_config["bootstrapServers"], "acks": 1}
            self.producer = Producer(**conf)

        except Exception as e:
            logger.error(e)
            logger.error(
                "ERROR: Unexpected error: Could not connect to Kafka instance.")
            raise Exception(str(e))

        logger.info("sink target: kafka instance connected")
        self.connected = True

    def close(self):
        """Sink connector deconstruct method.

        Args:
            None

        Returns:
            None

        Raises:
            None
        """
        self.connected = False

    def is_connected(self):
        """Sink connector connect check.

        Args:
            None

        Returns:
            None

        Raises:
            None
        """
        return self.connected

    @retry(stop_max_attempt_number=default_retry_times, wait_exponential_multiplier=1000, retry_on_exception=retry_on_exception)
    def _write_data(self, single_data):
        """ Inner method to write data to kafka instance.

        Args:
            single_data: input data

        Returns:
                Null

        Raises:
            kafka exception
        """
        self.producer.produce(self.sink_config["topicName"], single_data)
        self.producer.poll(0)

    def deliver(self, payload):
        """Sink operator.

        Args:
            payload: input payload

        Returns:
            Failed data list

        Raises:
            KafkaException
        """
        for single_data in payload:
            self._write_data(single_data)

        self.producer.flush()

        return


sink = Sink()


def initialize(context):
    """Sink function initializer.
        This method is called before the function invocation,
        and will be only called once in a specified container.
        todo: User should realize this method

    Args:
        context: fc function invocation context

    Returns:
        None

    Raises:
        Exception
    """
    logger.info('initializing sink connect')
    sink_config_env = os.environ.get('SINK_CONFIG')
    sink_config = json.loads(sink_config_env)
    if not sink_schema.validate_sink_config_schema(sink_config):
        logger.error("validate failed error: %s",
                     Schema(sink_schema.SINK_CONFIG_SCHEMA, ignore_extra_keys=True).validate(sink_config))
        raise Exception("SINK_CONFIG_SCHEMA validate failed")

    sink.connect(sink_config)


def destroy(context):
    """Sink function deconstructor.
        This method is called as pre-stop, which will be executed before the function container releasement.

    Args:
        context: fc function invocation context

    Returns:
        None

    Raises:
        None
    """
    sink.close()


def handler(event, context):
    """FC Function handler.

    Args:
        event: FC function invocation payload.
        context:  FC function invocation context. Valid params see: https://help.aliyun.com/document_detail/422182.html.

    Returns:
        {"success": True}

    Raises:
        Exception.
    """

    try:
        if not sink.is_connected():
            sink.connect(sink.sink_config)
            logger.error("unconnected sink target. Now reconnected")
        sink.deliver(transform.transform(event, context))

    except Exception as e:
        logger.error(e)
        traceback.print_exc()
        raise e

    return json.dumps({"success": True, "error_message": ""})
