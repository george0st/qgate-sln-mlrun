from qgate_sln_mlrun.ts.tsbase import TSBase
from qgate_sln_mlrun.ts.tshelper import TSHelper
from qgate_sln_mlrun.setup import Setup
from qgate_sln_mlrun.helper.basehelper import BaseHelper

class KafkaHelper(BaseHelper):

    # Prefix of TOPIC with sources
    TOPIC_SOURCE_PREFIX = "tmp_"

    def __init__(self,setup: Setup):
        self._setup = setup

    @property
    def setup(self) -> Setup:
        return self._setup

    @property
    def configured(self):
        """Return None if not configured or connection string (based on setting QGATE_KAFKA in *.env file)."""
        return self.setup.kafka

    @property
    def prefix(self):
        return KafkaHelper.TOPIC_SOURCE_PREFIX

    def create_insert_data(self, featureset_name, drop_if_exist = False):
        """Create topic and insert data"""
        from kafka import KafkaProducer

        producer = KafkaProducer(bootstrap_servers=self.setup.kafka)
        for _ in range(5):
            producer.send('ax', b'some_message_bytes')