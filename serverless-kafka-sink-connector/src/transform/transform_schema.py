#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from schema import Schema

# MESSAGE_SCHEMA is used to validate messages.
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

# TRANSFORM_CONFIG_SCHEMA is used to validate transform config.
TRANSFORM_CONFIG_SCHEMA = {
    'eventSchema': str,
    'batchOrNot': str,
}

# DESTINATION_CONFIG_SCHEMA is used to validate destination config.
DESTINATION_CONFIG_SCHEMA = {
    'serviceName': str,
    'functionName': str,
}


def validate_message_schema(message):
    """validate input message according to Message_SCHEMA.

    Args:
        message: Origin message in cloud events schema from event bridge.

    Returns:
        message: Whether message is validated.

    Raises:
        None.
    """
    return Schema(MESSAGE_SCHEMA, ignore_extra_keys=True).is_valid(message)


def validate_transform_config_schema(config):
    """validate transform config according to ENV.

    Args:
        message: Origin message in cloud events schema from event bridge.

    Returns:
        config: Origin config.

    Raises:
        None.
    """
    return Schema(TRANSFORM_CONFIG_SCHEMA, ignore_extra_keys=True).is_valid(config)


def validate_destination_config_schema(config):
    """validate destination config according to ENV.

    Args:
        config: Origin config.

    Returns:
        bool: Whether the config is validated.

    Raises:
        None.
    """
    return Schema(DESTINATION_CONFIG_SCHEMA, ignore_extra_keys=True).is_valid(config)
