# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Dataset purpose."""

from enum import Enum


class DatasetPurpose(Enum):
    """Represents a dataset purpose type that is used to retrieve a dataset from a model."""

    TRAINING = "training"
    MODEL_SERVING = "model_serving"
