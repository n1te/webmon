from services.http import HttpServiceConfig
from services.kafka_consumer import KafkaConsumerConfig

from common.config import YAMLConfig
from common.services.postgres import PostgresConfig


class CheckerConfig(YAMLConfig):
    kafka: KafkaConsumerConfig
    postgres: PostgresConfig
    http: HttpServiceConfig
