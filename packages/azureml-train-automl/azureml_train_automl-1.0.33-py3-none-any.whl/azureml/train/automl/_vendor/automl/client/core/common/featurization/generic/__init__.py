# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Init for generic transformers module."""
from automl.client.core.common.featurization.generic.imputation_marker import ImputationMarker
from automl.client.core.common.featurization.generic.lambda_transformer import LambdaTransformer
from automl.client.core.common.featurization.generic.generic_transformer import GenericTransformer
from automl.client.core.common.featurization.generic.generic_featurizers import GenericFeaturizers
from automl.client.core.common.featurization.generic.countbased_target_encoder import CountBasedTargetEncoder
from automl.client.core.common.featurization.generic.modelbased_target_encoder import ModelBasedTargetEncoder
from automl.client.core.common.featurization.generic.crossvalidation_target_encoder import CrossValidationTargetEncoder
from automl.client.core.common.featurization.generic.woe_target_encoder import WoEBasedTargetEncoder
from automl.client.core.common.featurization.generic.abstract_multiclass_target_encoder \
    import AbstractMultiClassTargetEncoder
