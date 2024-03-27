#!/usr/bin/env python
# -*- coding: utf-8 -*-

OTS_SINK_CONFIG_SCHEMA = {
    'endpoint': str,
    'access_key_id': str,
    'access_key_secret': str,
    'security_token': str,
    'instance_name': str,
    'table_name': str,
    'primary_keys_name': list,
    'rows_name': list,
}
