import logging

from aiokafka.helpers import create_ssl_context
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class KafkaSSLConfig(BaseModel):
    cafile: str
    certfile: str
    keyfile: str


class KafkaConfig(BaseModel):
    bootstrap_servers: str
    topic: str
    ssl: KafkaSSLConfig | None = None


class KafkaServiceBase:
    @staticmethod
    def _get_ssl_params(ssl_config: KafkaSSLConfig) -> dict:
        if ssl_config is not None:
            return {
                'security_protocol': 'SSL',
                'ssl_context': create_ssl_context(
                    cafile=ssl_config.cafile,
                    certfile=ssl_config.certfile,
                    keyfile=ssl_config.keyfile,
                ),
            }
        else:
            return {}
