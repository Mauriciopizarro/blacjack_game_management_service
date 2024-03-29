import json
import pika
import uuid
from logging.config import dictConfig
import logging
from config import settings
from domain.interfaces.publisher import Publisher
from infrastructure.logging import LogConfig
from urllib.parse import urlparse

dictConfig(LogConfig().dict())
logger = logging.getLogger("blackjack")


class RabbitConnection:

    instance = None

    def __init__(self):
        credentials = pika.PlainCredentials(settings.RABBIT_USERNAME, settings.RABBIT_PASSWORD)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=settings.RABBIT_HOST,
                                      heartbeat=9999,
                                      blocked_connection_timeout=300,
                                      credentials=credentials,
                                      virtual_host=settings.RABBIT_VHOST)
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue="game_started")
        logger.warning('Rabbit connection initialized')

    @classmethod
    def get_channel(cls):
        instance = cls.init_connection()
        return instance.channel

    @classmethod
    def get_connection(cls):
        instance = cls.init_connection()
        return instance.connection

    @classmethod
    def init_connection(cls):
        if not cls.instance:
            cls.instance = cls()
        return cls.instance


class RabbitPublisher(Publisher):

    def send_message(self, message: dict, topic: str):
        """Method to publish message to RabbitMQ"""
        publish_queue_name = topic
        channel = RabbitConnection.get_channel()
        channel.basic_publish(
            exchange='',
            routing_key=publish_queue_name,
            properties=pika.BasicProperties(
                correlation_id=str(uuid.uuid4())
            ),
            body=json.dumps(message)
        )
        logger.info(f'Message published in topic {topic}')
