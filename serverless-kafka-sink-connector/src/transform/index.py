# -*- coding: utf-8 -*-
import logging
import json
import os

import fc2
from schema import Schema

import transform_schema

logger = logging.getLogger()
logger.setLevel(level=logging.INFO)


def sink_api_handler(context, destination_config, payload):
    """Send Data to FC Sink Function.

    Using FC SDK, call sink function with dealt data and transform configuration.

    Args:
        destination_config: destination config.
        payload: dealt data, following cloud event schema, or customized data.

    Returns:
        None

    Raises:
        Exception: All Exceptions happened when call fc.
    """
    try:
        creds = context.credentials
        # 实例化要请求产品的client对象，以及函数所在的地域
        client = fc2.Client(
            endpoint='https://%s.%s.fc.aliyuncs.com' % (context.account_id, context.region),
            accessKeyID=creds.access_key_id,
            accessKeySecret=creds.access_key_secret,
            securityToken=creds.security_token or '')

        response = client.invoke_function(destination_config["serviceName"],
                                          destination_config["functionName"], json.dumps(payload),
                                          headers={'x-fc-invocation-type': 'Async'})
        logger.info(response.data)
    except Exception as e:
        logger.error(e)
        raise e


def transform(transform_config, message):
    """Filter method.

    User should edit this method to make sure the message is transformed properly.

    Args:
        transform_config: transform config.
        message: Origin message in cloud events schema from event bridge.

    Returns:
        message: Message after filtered.

    Raises:
        None.
    """
    if transform_config["eventSchema"] == "cloudEvent":
        logger.info("check single data with schema: cloudEvent")
        if transform_config['batchOrNot'] == "True":
            # validate batch data schema
            for single_message in message:
                if not transform_schema.validate_message_schema(single_message):
                    logger.error("validate failed error: %s",
                                 Schema(transform_schema.MESSAGE_SCHEMA, ignore_extra_keys=True).validate(single_message))
                    raise Exception("MESSAGE_SCHEMA validate failed")
        else:
            # validate single data schema
            if not transform_schema.validate_message_schema(message):
                logger.error("validate failed error: %s",
                             Schema(transform_schema.MESSAGE_SCHEMA, ignore_extra_keys=True).validate(message))
                raise Exception("MESSAGE_SCHEMA validate failed")

    return message


def handler(event, context):
    """FC Function handler.

    Args:
        event: FC function invocation payload.

    Returns:
        context:  FC function invocation context. Valid params see: https://help.aliyun.com/document_detail/422182.html.

    Raises:
        None.
    """
    try:
        transform_config_env = os.environ.get('TRANSFORM_CONFIG')
        transform_config = json.loads(transform_config_env)
        if not transform_schema.validate_transform_config_schema(transform_config):
            logger.error("validate failed error: %s",
                         Schema(transform_schema.TRANSFORM_CONFIG_SCHEMA, ignore_extra_keys=True).validate(transform_config))
            raise Exception("TRANSFORM_CONFIG_SCHEMA validate failed")

        destination_config_env = os.environ.get('DESTINATION_CONFIG')
        destination_config = json.loads(destination_config_env)
        if not transform_schema.validate_destination_config_schema(destination_config):
            logger.error("validate failed error: %s",
                         Schema(transform_schema.DESTINATION_CONFIG_SCHEMA, ignore_extra_keys=True).validate(destination_config))
            raise Exception("DESTINATION_CONFIG_SCHEMA validate failed")

        payload = json.loads(event)

        sink_api_handler(context, destination_config, transform(transform_config, payload))

    except Exception as e:
        logger.error(e)
        return json.dumps({"success": False, "error_message": str(e)})

    return json.dumps({"success": True, "error_message": ""})
