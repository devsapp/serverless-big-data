#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from schema import Schema

# SINK_CONFIG_SCHEMA is used to validate sink target config.
SINK_CONFIG_SCHEMA = {
    'bootstrapServers': str,
    'topicName': str,
}

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