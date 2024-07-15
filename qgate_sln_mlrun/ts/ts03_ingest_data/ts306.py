"""
  TS306: Ingest data to feature set(s) from Kafka source
"""
from qgate_sln_mlrun.ts.tsbase import TSBase
import mlrun
import mlrun.feature_store as fstore
from mlrun.datastore.sources import KafkaSource
import json
from qgate_sln_mlrun.helper.kafkahelper import KafkaHelper
import os
import glob


class TS306(TSBase):

    def __init__(self, solution):
        super().__init__(solution, self.__class__.__name__)
        self._kafka = KafkaHelper(self.setup)

    @property
    def desc(self) -> str:
        return "Ingest data to feature set(s) from Kafka source"

    @property
    def long_desc(self):
        return ("Ingest data to feature set(s) from Kafka source")

    def prj_exec(self, project_name):
        """ Data ingest"""

        # It can be executed only in case that configuration is fine
        if not self._kafka.configured:
            return

        for featureset_name in self.get_featuresets(self.project_specs.get(project_name)):
            # Create shared topic as data source
            self._kafka.create_insert_data(self._kafka.create_helper(featureset_name), featureset_name,True)
            self._create_featureset(f'{project_name}/{featureset_name}', project_name, featureset_name)

    @TSBase.handler_testcase
    def _create_featureset(self, testcase_name, project_name, featureset_name):
        # get existing feature set (feature set have to be created in previous test scenario)
        featureset = fstore.get_feature_set(f"{project_name}/{featureset_name}")

        # samples
        #  https://github.com/mlrun/test-notebooks/tree/main/kafka_redis_fs
        #  https://docs.mlrun.org/en/latest/feature-store/sources-targets.html#id1

        # fstore.ingest(featureset,
        #               KafkaSource(brokers=self.setup.kafka,
        #                         topics=[self._kafka.create_helper(featureset_name)]),
        #               # overwrite=False,
        #               return_df=False,
        #               # infer_options=mlrun.data_types.data_types.InferOptions.Null)
        #               infer_options=mlrun.data_types.data_types.InferOptions.default())
