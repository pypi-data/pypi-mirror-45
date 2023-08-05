# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Convenience names for long types."""
from typing import List, Tuple

from automl.client.core.common.stats_computation import RawFeatureStats

# Stats and column purposes type
StatsAndColumnPurposeType = Tuple[RawFeatureStats, str, str]
