# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Defines the Explanation dashboard class."""

from .ExplanationWidget import ExplanationWidget
from IPython.display import display
import numpy as np
import sys


class ExplanationDashboard(object):
    """The dashboard class, wraps the dashboard component."""

    def __init__(self, explanationObject, learner, dataset):
        """Initialize the Explanation Dashboard.

        :param explanationObject: An object that represents an explanation. It is assumed that it
            has a local_importance_values property that is a 2d array in teh case of regression,
            and 3d array in the case of classification. Dimensions are either samples x features, or
            classes x samples x features. Optionally, it may have a features array that is the string name
            of the features, and a classes array that is the string name of the classes.
        :type explanationObject: object
        :param learner: An object that represents a model. It is assumed that for the classification case
            it has a method of predict_proba() returning the prediction probabilities for each
            class and for the regression case a method of predict() returning the prediction value.
        :type learner: object
        :param dataset:  A matrix of feature vector examples (# examples x # features), the same sampels
            used to build the explanationObject.
        :type dataset: numpy.array or list[][]
        """
        self._widget_instance = ExplanationWidget()
        try:
            if (type(dataset) != list):
                dataset = dataset.tolist()
            localExplanations = explanationObject.local_importance_values
            if (type(localExplanations) != list):
                localExplanations = localExplanations.tolist()
            globalExplanation = explanationObject.global_importance_values
            if (type(globalExplanation) != list):
                globalExplanation = globalExplanation.tolist()
            y_pred = learner.predict(dataset).tolist()
            local_dim = len(np.shape(localExplanations))
            if local_dim != 2 and local_dim != 3:
                display("Error: Unexpected types")
            else:
                dataArg = {
                    "localExplanations": localExplanations,
                    "predictedY": y_pred,
                    "trainingData": dataset,
                    "globalExplanation": globalExplanation}
                if hasattr(explanationObject, 'features'):
                    features = explanationObject.features
                    if (type(features) != list):
                        features = features.tolist()
                    dataArg['featureNames'] = features
                if hasattr(explanationObject, 'classes'):
                    classNames = explanationObject.classes
                    if (type(classNames) != list):
                        classNames = classNames.tolist()
                    dataArg['classNames'] = classNames
                self._widget_instance.value = dataArg
                display(self._widget_instance)
        except:
            print("Error: ", sys.exc_info()[0])

    def _show(self):
        display(self._widget_instance)
