import datetime

from storey import MapClass

from typing import Any, Dict, List, Optional, Union

import mlrun.errors
from mlrun.serving.utils import StepToDict
from mlrun.feature_store.steps import MLRunStep
import uuid

class GenerateId(StepToDict, MLRunStep):
    def __init__(self, namespace: str, features: List[str], **kwargs):
        super().__init__(**kwargs)
        self.namespace = namespace
        self.features = features

    def _get_id(self):
        return uuid.uuid5(self.namespace, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))

    def _do_storey(self, event):
        for feature in self.features:
            try:
                event[feature]=self._get_id()
            except KeyError:
                raise mlrun.errors.MLRunInvalidArgumentError(
                    f"The error in '{feature}'"
                )
        return event

    def _do_pandas(self, event):
        for feature in self.features:
            try:
                event[feature]=self._get_id()
            except KeyError:
                raise mlrun.errors.MLRunInvalidArgumentError(
                    f"The error in '{feature}'"
                )
        return event

    def _do_spark(self, event):
        for feature in self.features:
            try:
                event[feature]=self._get_id()
            except KeyError:
                raise mlrun.errors.MLRunInvalidArgumentError(
                    f"The error in '{feature}'"
                )
        return event

    @classmethod
    def validate_args(cls, feature_set, **kwargs):
        features = kwargs.get("features", [])
        namespace = kwargs.get("namespace", [])

        entity_names = list(feature_set.spec.entities.keys())
        dropped_entities = set(features).intersection(entity_names)
        if dropped_entities:
            raise mlrun.errors.MLRunInvalidArgumentError(
                f"GenerateID can not apply to these entities: {dropped_entities}"
            )

        if not namespace:
            raise mlrun.errors.MLRunInvalidArgumentError("GenerateID can use not None value for namespace")

