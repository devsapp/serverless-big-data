#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from schema import Schema

# message_schema is used to validate messages.
MESSAGE_SCHEMA = {
    'id': str,
    'source': str,
    'specversion': str,
    'type': str,
    'datacontenttype': str,
    'time': str,
    'subject': str,
    'aliyunaccountid': str,
    #'data': data is user define,
}

# SINK_CONFIG_SCHEMA is used to validate sink target config.
SINK_CONFIG_SCHEMA = {
    'eventSchema': str,
    'batchOrNot': str,
    'bootstrapServers': str,
    'topicName': str,
}


def validate_message_schema(message):
    """validate input message according to Message_SCHEMA.

    Args:
        message: Origin message in cloud events schema from event bridge.

    Returns:
        bool:Whether the config is validated.

    Raises:
        None.
    """
    return Schema(MESSAGE_SCHEMA, ignore_extra_keys=True).is_valid(message)

def validate_sink_config_schema(sink_config):
    """validate sink target config according to SINK_CONFIG_SCHEMA.

    Args:
        sink_config: Origin message in cloud events schema from event bridge.

    Returns:
        bool: Whether the config is validated.

    Raises:
        None.
    """
    return Schema(SINK_CONFIG_SCHEMA, ignore_extra_keys=True).is_valid(sink_config)