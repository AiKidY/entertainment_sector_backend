#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rabbitpy

from src.config import RABBITMQ_CONF


class RabbitMqFactory:
    def __init__(self):
        print(RABBITMQ_CONF)
        username = RABBITMQ_CONF.get('username')
        password = RABBITMQ_CONF.get('password')
        host = RABBITMQ_CONF.get('host')
        port = RABBITMQ_CONF.get('port')
        virtual_host = RABBITMQ_CONF.get('virtual_host')
        heartbeat = RABBITMQ_CONF.get('heartbeat')

        rabbit_url = f'amqp://{username}:{password}@{host}:{port}/{virtual_host}'
        self.rabbit_client = rabbitpy.Connection(rabbit_url)

    def get_rabbit_cleint(self):
        return self.rabbit_client

    def creat_a_channel(self) -> rabbitpy.AMQP:
        return rabbitpy.AMQP(self.rabbit_client.channel())  # 使用适配器，使rabbitpy包的公有方法几乎接近pika包的channel的方法。
