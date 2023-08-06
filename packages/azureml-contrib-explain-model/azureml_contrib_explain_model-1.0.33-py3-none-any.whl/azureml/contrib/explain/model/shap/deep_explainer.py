# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Defines an explainer for DNN models."""

from azureml.explain.model.shap import deep_explainer
from azureml.explain.model.dataset.decorator import tabular_decorator
from azureml.explain.model._internal.constants import ExplainType
from ..scoring.scoring_model import KNNScoringModel
from ..explanation.explanation import _create_local_explanation
from .kwargs_utils import _get_explain_global_kwargs
from ..common.aggregate import contrib_aggregator


@contrib_aggregator
class DeepExplainer(deep_explainer.DeepExplainer):
    """An explainer for DNN models, implemented using shap's DeepExplainer, supports tensorflow and pytorch."""

    @tabular_decorator
    def explain_global(self, evaluation_examples, sampling_policy=None,
                       include_local=True):
        """Explain the model globally by aggregating local explanations to global.

        :param evaluation_examples: A matrix of feature vector examples (# examples x # features) on which
            to explain the model's output.
        :type evaluation_examples: numpy.array or pandas.DataFrame or scipy.sparse.csr_matrix
        :param sampling_policy: Optional policy for sampling the evaluation examples.  See documentation on
            SamplingPolicy for more information.
        :type sampling_policy: SamplingPolicy
        :param include_local: Include the local explanations in the returned global explanation.
            If include_local is False, will stream the local explanations to aggregate to global.
        :type include_local: bool
        :return: A model explanation object. It is guaranteed to be a GlobalExplanation which also has the properties
            of LocalExplanation and ExpectedValuesMixin. If the model is a classifier, it will have the properties of
            PerClassMixin.
        :rtype: DynamicGlobalExplanation
        """
        kwargs = _get_explain_global_kwargs(sampling_policy, ExplainType.SHAP_DEEP, include_local)
        return self._explain_global(evaluation_examples, **kwargs)

    @tabular_decorator
    def explain_local(self, evaluation_examples):
        """Explain the model by using shap's deep explainer.

        :param evaluation_examples: A matrix of feature vector examples (# examples x # features) on which
            to explain the model's output.
        :type evaluation_examples: numpy.array or pandas.DataFrame or scipy.sparse.csr_matrix
        :return: A model explanation object. It is guaranteed to be a LocalExplanation which also has the properties
            of ExpectedValuesMixin. If the model is a classfier, it will have the properties of the ClassesMixin.
        :rtype: DynamicLocalExplanation
        """
        kwargs = super(DeepExplainer, self)._get_explain_local_kwargs(evaluation_examples)
        return _create_local_explanation(**kwargs)

    def create_scoring_model(self, evaluation_examples):
        """Create the scoring model for the deep explainer.

        This will run explain_global in the background.

        :param evaluation_examples: The evaluation samples that have been used to generate
            the local importance values.
        :type evaluation_examples: numpy.array or iml.datatypes.DenseData or scipy.sparse.csr_matrix
        :return: The scoring model based on the model being explained.
        :rtype: KNNScoringModel
        """
        explanation = self.explain_global(evaluation_examples)
        return KNNScoringModel(evaluation_examples, explanation.local_importance_values)
