from qgate_sln_mlrun.ts.tsbase import TSBase
from qgate_sln_mlrun.ts.tshelper import TSHelper
from qgate_sln_mlrun.setup import Setup
from qgate_sln_mlrun.helper.basehelper import BaseHelper
import glob
import os
import pandas as pd
import json


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
        from kafka import KafkaProducer

        producer = KafkaProducer(bootstrap_servers=self.setup.kafka)
        topic_name = self.create_helper_name(project_name, featureset_name)

        # create possible file for load
        source_file = os.path.join(os.getcwd(),
                                   self.setup.model_definition,
                                   "02-data",
                                   self.setup.dataset_name,
                                   f"*-{featureset_name}.csv.gz")

        for file in glob.glob(source_file):
            # ingest data with bundl/chunk
            for data_frm in pd.read_csv(file,
                                        sep=self.setup.csv_separator,  # ";",
                                        header="infer",
                                        decimal=self.setup.csv_decimal,  # ",",
                                        compression="gzip",
                                        encoding="utf-8",
                                        chunksize=Setup.MAX_BUNDLE):
                for row in data_frm.to_numpy().tolist():
                    producer.send(topic_name, json.dumps(row))
            producer.flush()

    def _delete_topics(self, topic_names):
        from kafka.admin import KafkaAdminClient, NewTopic

        admin_client = KafkaAdminClient(bootstrap_servers=self.setup.kafka)
        try:
            admin_client.delete_topics(topics=topic_names)
        except  Exception as e:
            print(e)



    def helper_exist(self, project_name, featureset_name):
        from kafka import KafkaConsumer

        consumer = KafkaConsumer(bootstrap_servers=self.setup.kafka)
        topic_name = self.create_helper_name(project_name, featureset_name)
        existing_topic_list = consumer.topics()
        if topic_name in existing_topic_list:
            return True
        return False
