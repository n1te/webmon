from services.kafka_producer import KafkaProducerConfig

from common.config import YAMLConfig
from common.services.postgres import PostgresConfig


class SchedulerConfig(YAMLConfig):
    kafka: KafkaProducerConfig
    postgres: PostgresConfig
