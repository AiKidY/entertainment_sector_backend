#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
import yaml
import logging

DEBUG = 1

logger = logging.getLogger(__name__)


def loadYamlConfig():
    yaml_config = dict()
    try:
        yamfile = os.getcwd() + "/etc/config.yaml"
        print(f'loadYamlConfig, yamfile_path: {yamfile}')
        f = open(yamfile, 'r', encoding='utf-8')
        yaml_config = yaml.load(f.read(), Loader=yaml.SafeLoader)
        f.close()
    except Exception as e:
        logger.error(f'loadYamlConfig, error: {e}')
    return yaml_config


CONF = loadYamlConfig()
logger.info(f'loadYamlConfig finish: {CONF}')

# ------------------------------------------------------------ 配置 ------------------------------------------------------
rabbitmq = CONF.get('rabbitmq', {})

RABBITMQ_CONF = {
    'host': rabbitmq.get("host"),
    'port': rabbitmq.get("port"),
    'virtual_host': rabbitmq.get("virtual_host"),
    'username': rabbitmq.get("username"),
    'password': rabbitmq.get("password"),
    'socket_timeout': rabbitmq.get("timeout"),
    'hb_interval': rabbitmq.get("heartbeat")
}

all_config_var = locals()


# ------------------------------------------------------------ 配置 ------------------------------------------------------


def loadJsonConfig():
    curr_path = os.getcwd()
    with open(curr_path + "/etc/config_ex.json", 'r', encoding='utf-8') as load_f:
        try:
            load_config = json.load(load_f)
        except Exception as e:
            logger.error('load config_ex fail: %s' % e)
            return

    for key in load_config:
        if not all_config_var.get(key, None) is None:
            if isinstance(all_config_var[key], dict):
                all_config_var[key].update(load_config[key])
            else:
                all_config_var[key] = load_config[key]

    logger.info('load config_ex succ')


# # 如果是kube 环境加载配置
if DEBUG == 2 or DEBUG == 3:
    loadJsonConfig()
