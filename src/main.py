#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
from collections.abc import Callable

from src.tools.rabbitmq import RabbitMqFactory

logger = logging.getLogger(__name__)


# 消费回调函数
def callback_handler(body):
    print(f'callback_handler, body: {body}')


class RabbitmqConsumer():
    def __init__(self, queue_name, threads_num=100, max_retry_times=3):
        self.amqp_factory = RabbitMqFactory()
        self.queue_name = queue_name
        self.threads_num = threads_num
        self.max_retry_times = max_retry_times

    def init(self):
        channel = self.amqp_factory.creat_a_channel()
        channel.queue_declare(queue=self.queue_name, durable=True)
        channel.basic_qos(prefetch_count=self.threads_num)

        for message in channel.basic_consume(self.queue_name):
            body = message.body.decode()
            print(f'接收到消息, body: {body}')
            self.consume_rabbitpy(message)

    def consume_rabbitpy(self, message, current_retry_times=0):
        if current_retry_times < self.max_retry_times:
            try:
                callback_handler(message.body.decode())
                message.ack()  # 确认消费
            except Exception as e:
                print(f'consume_rabbitpy, 第{current_retry_times + 1}次异常, error: {e}')
                self.consume_rabbitpy(message, current_retry_times + 1)
        else:
            print(f'consume_rabbitpy, 达到最大重试次数: {self.max_retry_times}, 消息自动确认消费')  # 错得超过指定的次数了，就确认消费了。
            message.ack()  # 超过重试次数, 则自动确认消费


if __name__ == '__main__':
    rabbitmq_consumer = RabbitmqConsumer('queue_test', threads_num=200)
    rabbitmq_consumer.init()
