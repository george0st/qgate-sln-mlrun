from qgate_sln_mlrun.ts.tsbase import TSBase
from qgate_sln_mlrun.ts.tshelper import TSHelper
from qgate_sln_mlrun.setup import Setup
from qgate_sln_mlrun.helper.basehelper import BaseHelper
import glob
import os
import pandas as pd
import json
from kafka.admin import KafkaAdminClient, NewTopic
from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import (UnknownError, KafkaConnectionError, FailedPayloadsError,
                          KafkaTimeoutError, KafkaUnavailableError,
                          LeaderNotAvailableError, UnknownTopicOrPartitionError,
                          NotLeaderForPartitionError, ReplicaNotAvailableError)


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

    def create_insert_data(self, project_name, featureset_name, drop_if_exist = False):
        """Create topic and insert data"""

        producer = KafkaProducer(bootstrap_servers=self.setup.kafka)
        topic_name = self.create_helper_name(project_name, featureset_name)

        if drop_if_exist:
            self._delete_topics([topic_name])

        # create possible file for load
        source_file = os.path.join(os.getcwd(),
                                   self.setup.model_definition,
                                   "02-data",
                                   self.setup.dataset_name,
                                   f"*-{featureset_name}.csv.gz")

        for file in glob.glob(source_file):
            # ingest data with bundl/chunk
            for data_frm in pd.read_csv(file,
                                        sep=self.setup.csv_separator,
                                        header="infer",
                                        decimal=self.setup.csv_decimal,
                                        compression="gzip",
                                        encoding="utf-8",
                                        chunksize=Setup.MAX_BUNDLE):
                for row in data_frm.to_numpy().tolist():
                    producer.send(topic_name, json.dumps(row).encode("utf-8"))
                producer.flush()
        producer.close()

    def _delete_topics(self, topic_names):

        admin_client = None
        try:
            admin_client = KafkaAdminClient(bootstrap_servers=self.setup.kafka)
            admin_client.delete_topics(topics=topic_names, timeout_ms=2000)
        except UnknownTopicOrPartitionError:
            pass
        except Exception as e:
            pass
        finally:
            if admin_client:
                admin_client.close()
    def _create_topic(self, topic_name, num_partitions=1, replication_factor=1, retention_min=60):

        admin_client=None
        try:
            admin_client = KafkaAdminClient(bootstrap_servers=self.setup.kafka)

            # https://docs.confluent.io/platform/current/installation/configuration/topic-configs.html#retention-ms
            topic_list = [
                NewTopic(
                    name=topic_name,
                    num_partitions=num_partitions,
                    replication_factor=replication_factor,
                    topic_configs={'retention.ms': str(retention_min*60*1000)}
                )
            ]
            admin_client.create_topics(new_topics=topic_list, validate_only=False)
        finally:
            if admin_client:
                admin_client.close()

    def helper_exist(self, project_name, featureset_name) -> bool:

        consumer = existing_topic_list = None
        try:
            consumer=KafkaConsumer(bootstrap_servers=self.setup.kafka)
            existing_topic_list = consumer.topics()
        except:
            pass
        finally:
            if consumer:
                consumer.close()

        topic_name = self.create_helper_name(project_name, featureset_name)
        if existing_topic_list:
            if topic_name in existing_topic_list:
                return True
        return False
