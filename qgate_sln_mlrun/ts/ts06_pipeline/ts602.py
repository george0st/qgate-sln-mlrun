"""
  TS602: Complex pipeline(s)
"""

from qgate_sln_mlrun.ts.tsbase import TSBase
from qgate_sln_mlrun.setup import Setup
import mlrun.feature_store as fstore
import mlrun
import pandas as pd
import glob
import os


class TS602(TSBase):

    def __init__(self, solution):
        super().__init__(solution, self.__class__.__name__)

    @property
    def desc(self) -> str:
        return "Complex pipeline(s)"

    @property
    def long_desc(self):
        return "Complex pipeline(s)"

    def exec(self):
        """Simple pipeline during ingest"""
        self._complex_pipeline(f"*/complex (event)")


    @TSBase.handler_testcase
    def _complex_pipeline(self, testcase_name):

        # definition complex graph
        #

        # transaction ingest from parquet to the featureset


        ## Define and add value mapping
        # transaction_set = fs.FeatureSet("transactions",
        #                                  entities=[fs.Entity("source")],
        #                                  timestamp_key='timestamp',
        #                                  description="transactions feature set")
        # main_categories = ["es_transportation", "es_health", "es_otherservices",
        #        "es_food", "es_hotelservices", "es_barsandrestaurants",
        #        "es_tech", "es_sportsandtoys", "es_wellnessandbeauty",
        #        "es_hyper", "es_fashion", "es_home", "es_contents",
        #        "es_travel", "es_leisure"]
        #
        # # One Hot Encode the newly defined mappings
        # one_hot_encoder_mapping = {'category': main_categories,
        #                            'gender': list(transactions_data.gender.unique())}
        #
        # # Define the graph steps
        # transaction_set.graph\
        #     .to(DateExtractor(parts = ['hour', 'day_of_week'], timestamp_col = 'timestamp'))\
        #     .to(MapValues(mapping={'age': {'U': '0'}}, with_original_features=True))\
        #     .to(OneHotEncoder(mapping=one_hot_encoder_mapping)).respond()
        #
        #
        # # Add aggregations for 2, 12, and 24 hour time windows
        # transaction_set.add_aggregation(name='amount',
        #                                 column='amount',
        #                                 operations=['avg','sum', 'count','max'],
        #                                 windows=['2h', '12h', '24h'],
        #                                 period='1h')
        pass
