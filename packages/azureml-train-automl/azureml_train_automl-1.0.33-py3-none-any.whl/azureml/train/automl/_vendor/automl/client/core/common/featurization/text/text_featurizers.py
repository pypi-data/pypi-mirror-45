# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Container for Text featurizers."""
import numpy as np
from typing import Any

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder
from sklearn.naive_bayes import MultinomialNB

from automl.client.core.common import constants, logging_utilities
from automl.client.core.common.featurization.text.nimbus_ml_text_target_encoder import NimbusMLTextTargetEncoder
from automl.client.core.common.featurization.data.word_embeddings_info import EmbeddingInfo
from automl.client.core.common.featurization.text.stats_transformer import StatsTransformer
from automl.client.core.common.featurization.text.bagofwords_transformer import BagOfWordsTransformer
from automl.client.core.common.featurization.text.wordembedding_transformer import WordEmbeddingTransformer
from automl.client.core.common.featurization.text.stringcast_transformer import StringCastTransformer
from automl.client.core.common.featurization.generic.modelbased_target_encoder import ModelBasedTargetEncoder
from automl.client.core.common.featurization.data import DataProviders
from automl.client.core.common.featurization.featurization_utilities import if_package_exists

from .constants import NIMBUS_ML_PARAMS


class TextFeaturizers:
    """Container for Text featurizers."""

    @classmethod
    def bow_transformer(cls, *args: Any, **kwargs: Any) -> BagOfWordsTransformer:
        """Create bag of words transformer."""
        return BagOfWordsTransformer(*args, **kwargs)

    @classmethod
    def count_vectorizer(cls, *args: Any, **kwargs: Any) -> CountVectorizer:
        """Create count vectorizer featurizer."""
        if constants.FeatureSweeping.LOGGER_KEY in kwargs:
            kwargs.pop(constants.FeatureSweeping.LOGGER_KEY)
        if 'dtype' not in kwargs:
            kwargs['dtype'] = np.uint8
        return CountVectorizer(*args, **kwargs)

    @classmethod
    def naive_bayes(cls, *args: Any, **kwargs: Any) -> ModelBasedTargetEncoder:
        """Create naive bayes featurizer."""
        if not kwargs:
            kwargs = {}

        kwargs["model_class"] = MultinomialNB
        return ModelBasedTargetEncoder(*args, **kwargs)

    @classmethod
    def string_cast(cls, *args: Any, **kwargs: Any) -> StringCastTransformer:
        """Create string cast featurizer."""
        return StringCastTransformer(*args, **kwargs)

    @classmethod
    def text_stats(cls, *args: Any, **kwargs: Any) -> StatsTransformer:
        """Create text stats transformer."""
        return StatsTransformer(*args, **kwargs)

    @classmethod
    def text_target_encoder(cls, *args: Any, **kwargs: Any) -> ModelBasedTargetEncoder:
        """Create text target encoder."""
        return ModelBasedTargetEncoder(*args, **kwargs)

    @classmethod
    @if_package_exists(type(NimbusMLTextTargetEncoder).__name__, ["nimbusml"])
    def averaged_perceptron_text_target_encoder(cls, *args: Any, **kwargs: Any) -> NimbusMLTextTargetEncoder:
        """Create text target encoder using NimbusML AveragedPerceptron classifier."""
        from nimbusml.feature_extraction.text import NGramFeaturizer
        from nimbusml.feature_extraction.text.extractor import Ngram
        from nimbusml.linear_model import AveragedPerceptronBinaryClassifier
        featurizer = NGramFeaturizer(char_feature_extractor=Ngram(weighting=NIMBUS_ML_PARAMS.NGRAM_CHAR_WEIGHTING,
                                                                  ngram_length=NIMBUS_ML_PARAMS.NGRAM_CHAR_LENGTH,
                                                                  all_lengths=NIMBUS_ML_PARAMS.NGRAM_CHAR_ALL_LENGTHS),
                                     word_feature_extractor=Ngram(weighting=NIMBUS_ML_PARAMS.NGRAM_WORD_WEIGHTING,
                                                                  ngram_length=NIMBUS_ML_PARAMS.NGRAM_WORD_LENGTH,
                                                                  all_lengths=NIMBUS_ML_PARAMS.NGRAM_WORD_ALL_LENGTHS),
                                     vector_normalizer="L2")
        avg_perceptron = AveragedPerceptronBinaryClassifier(
            num_iterations=NIMBUS_ML_PARAMS.AVG_PERCEPTRON_ITERATIONS)
        return NimbusMLTextTargetEncoder(featurizer=featurizer, learner=avg_perceptron)

    @classmethod
    def tfidf_vectorizer(cls, *args: Any, **kwargs: Any) -> TfidfVectorizer:
        """Create tfidf featurizer."""
        if constants.FeatureSweeping.LOGGER_KEY in kwargs:
            kwargs.pop(constants.FeatureSweeping.LOGGER_KEY)
        if 'dtype' not in kwargs:
            kwargs['dtype'] = np.float32
        return TfidfVectorizer(*args, **kwargs)

    @classmethod
    def word_embeddings(cls, embeddings_name: str = EmbeddingInfo.ENGLISH_FASTTEXT_WIKI_NEWS_SUBWORDS_300,
                        *args: Any, **kwargs: Any) -> WordEmbeddingTransformer:
        """
        Create word embedding based transformer.

        :param embeddings_name: Name of the embeddings of interest.
        """
        logger_key = "logger"
        kwargs[logger_key] = kwargs.get(logger_key, logging_utilities.get_logger())
        assert embeddings_name is not None and embeddings_name in EmbeddingInfo._all_

        if WordEmbeddingTransformer.EMBEDDING_PROVIDER_KEY not in kwargs:
            kwargs[WordEmbeddingTransformer.EMBEDDING_PROVIDER_KEY] = DataProviders.get(embeddings_name)

        return WordEmbeddingTransformer(*args, **kwargs)

    @classmethod
    def get(cls, sweeper_name: str, *args: Any, **kwargs: Any) -> Any:
        """
        Create and return the request sweeper.

        :param sweeper_name: Name of the requested sweeper.
        """
        if hasattr(cls, sweeper_name):
            member = getattr(cls, sweeper_name)
            if hasattr(member, "__call__"):  # Check that the member is a callable
                return member(*args, **kwargs)
        return None
