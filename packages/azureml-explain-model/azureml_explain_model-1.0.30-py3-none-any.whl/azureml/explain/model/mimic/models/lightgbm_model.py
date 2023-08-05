# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Defines an explainable lightgbm model."""

from scipy.special import expit
from .explainable_model import BaseExplainableModel, _get_initializer_args
from ...common.explanation_utils import _scale_tree_shap
from ..._internal.constants import ShapValuesOutput
import warnings

with warnings.catch_warnings():
    warnings.filterwarnings('ignore', 'Starting from version 2.2.1', UserWarning)
    import shap
    try:
        from lightgbm import LGBMRegressor, LGBMClassifier
    except ImportError:
        print("Could not import lightgbm, required if using LGBMExplainableModel")

DEFAULT_RANDOM_STATE = 123


class LGBMExplainableModel(BaseExplainableModel):
    """LightGBM (fast, high performance framework based on decision tree) explainable model.

    Please see documentation for more details: https://github.com/Microsoft/LightGBM
    """

    def __init__(self, multiclass=False, random_state=DEFAULT_RANDOM_STATE,
                 shap_values_output=ShapValuesOutput.DEFAULT, classification=True, **kwargs):
        """Initialize the LightGBM Model.

        Additional arguments to LightGBMClassifier and LightGBMRegressor can be passed through kwargs.

        :param multiclass: Set to true to generate a multiclass model.
        :type multiclass: bool
        :param random_state: Int to seed the model.
        :type random_state: int
        :param shap_values_output: The type of the output from explain_local when using TreeExplainer.
            Currently only types 'default', 'probability' and 'teacher_probability' are supported.  If
            'probability' is specified, then we approximately scale the raw log-odds values from the
            TreeExplainer to probabilities.
        :type shap_values_output: azureml.explain.model._internal.constants.ShapValuesOutput
        :param classification: Indicates if this is a classification or regression explanation.
        :type classification: bool
        """
        self.multiclass = multiclass
        if self.multiclass:
            initializer = LGBMClassifier
        else:
            initializer = LGBMRegressor
        initializer_args = _get_initializer_args(initializer, kwargs)
        self._lgbm = initializer(random_state=random_state, **initializer_args)
        super(LGBMExplainableModel, self).__init__(**kwargs)
        self._logger.debug('Initializing LGBMExplainableModel')
        self._tree_explainer = None
        self._shap_values_output = shap_values_output
        self._classification = classification

    try:
        __init__.__doc__ = (__init__.__doc__ +
                            '\nIf multiclass=True, uses the parameters for LGBMClassifier:\n' +
                            LGBMClassifier.__init__.__doc__ +
                            '\nOtherwise, if multiclass=False, uses the parameters for LGBMRegressor:\n' +
                            LGBMRegressor.__init__.__doc__)
    except Exception:
        print("Could not import lightgbm, required if using LGBMExplainableModel")

    def fit(self, dataset, labels, **kwargs):
        """Call lightgbm fit to fit the explainable model.

        :param dataset: The dataset to train the model on.
        :type dataset: numpy or scipy array
        :param labels: The labels to train the model on.
        :type labels: numpy or scipy array
        """
        self._lgbm.fit(dataset, labels, **kwargs)

    try:
        fit.__doc__ = (fit.__doc__ +
                       '\nIf multiclass=True, uses the parameters for LGBMClassifier:\n' +
                       LGBMClassifier.fit.__doc__ +
                       '\nOtherwise, if multiclass=False, uses the parameters for LGBMRegressor:\n' +
                       LGBMRegressor.fit.__doc__)
    except Exception:
        print("Could not import lightgbm, required if using LGBMExplainableModel")

    def predict(self, dataset, **kwargs):
        """Call lightgbm predict to predict labels using the explainable model.

        :param dataset: The dataset to predict on.
        :type dataset: numpy or scipy array
        :return: The predictions of the model.
        :rtype: list
        """
        return self._lgbm.predict(dataset, **kwargs)

    try:
        predict.__doc__ = (predict.__doc__ +
                           '\nIf multiclass=True, uses the parameters for LGBMClassifier:\n' +
                           LGBMClassifier.predict.__doc__ +
                           '\nOtherwise, if multiclass=False, uses the parameters for LGBMRegressor:\n' +
                           LGBMRegressor.predict.__doc__)
    except Exception:
        print("Could not import lightgbm, required if using LGBMExplainableModel")

    def predict_proba(self, dataset, **kwargs):
        """Call lightgbm predict_proba to predict probabilities using the explainable model.

        :param dataset: The dataset to predict probabilities on.
        :type dataset: numpy or scipy array
        :return: The predictions of the model.
        :rtype: list
        """
        if self.multiclass:
            return self._lgbm.predict_proba(dataset, **kwargs)
        else:
            raise Exception("predict_proba not supported for regression or binary classification dataset")

    try:
        predict_proba.__doc__ = (predict_proba.__doc__ +
                                 '\nIf multiclass=True, uses the parameters for LGBMClassifier:\n' +
                                 LGBMClassifier.predict_proba.__doc__ +
                                 '\nOtherwise predict_proba is not supported for ' +
                                 'regression or binary classification.\n')
    except Exception:
        print("Could not import lightgbm, required if using LGBMExplainableModel")

    def explain_global(self, **kwargs):
        """Call lightgbm feature importances to get the global feature importances from the explainable model.

        :return: The global explanation of feature importances.
        :rtype: numpy.ndarray
        """
        return self._lgbm.feature_importances_

    def explain_local(self, evaluation_examples, probabilities=None, **kwargs):
        """Use TreeExplainer to get the local feature importances from the trained explainable model.

        :param evaluation_examples: The evaluation examples to compute local feature importances for.
        :type evaluation_examples: numpy or scipy array
        :param probabilities: If output_type is probability, can specify the teacher model's
            probability for scaling the shap values.
        :type probabilities: numpy.ndarray
        :return: The local explanation of feature importances.
        :rtype: Union[list, numpy.ndarray]
        """
        if self._tree_explainer is None:
            self._tree_explainer = shap.TreeExplainer(self._lgbm)
        if len(evaluation_examples.shape) == 1:
            evaluation_examples = evaluation_examples.reshape(1, -1)
        # Note: For binary and multiclass case the expected values and shap values are in the units
        # of the raw predictions from the underlying model.
        # In binary case, we are using regressor on logit.  In multiclass case, shap TreeExplainer
        # outputs the margin instead of probabilities.
        shap_values = self._tree_explainer.shap_values(evaluation_examples)
        is_probability = self._shap_values_output == ShapValuesOutput.PROBABILITY
        is_teacher_probability = self._shap_values_output == ShapValuesOutput.TEACHER_PROBABILITY
        if is_probability or is_teacher_probability:
            expected_values = self._tree_explainer.expected_value
            expected_values = expit(expected_values)
            if self._classification:
                if probabilities is None:
                    if is_teacher_probability:
                        raise Exception("Probabilities not specified for output type 'teacher_probability'")
                    if self.multiclass:
                        probabilities = self._lgbm.predict_proba(evaluation_examples)
                    else:
                        probabilities = expit(self._lgbm.predict(evaluation_examples))
                        probabilities = probabilities.reshape((probabilities.shape[0], 1))
                shap_values = _scale_tree_shap(shap_values, expected_values, probabilities)
        return shap_values

    @property
    def expected_values(self):
        """Use TreeExplainer to get the expected values.

        :return: The expected values of the LightGBM tree model.
        :rtype: list
        """
        if self._tree_explainer is None:
            self._tree_explainer = shap.TreeExplainer(self._lgbm)
        expected_values = self._tree_explainer.expected_value
        if self._classification:
            if not self.multiclass:
                expected_values = [-expected_values, expected_values]
            is_probability = self._shap_values_output == ShapValuesOutput.PROBABILITY
            is_teacher_probability = self._shap_values_output == ShapValuesOutput.TEACHER_PROBABILITY
            if is_probability or is_teacher_probability:
                return expit(expected_values)
        return expected_values

    @property
    def model(self):
        """Retrieve the underlying model.

        :return: The lightgbm model, either classifier or regressor.
        :rtype: Union[LGBMClassifier, LGBMRegressor]
        """
        return self._lgbm
