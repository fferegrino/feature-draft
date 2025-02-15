import pandas as pd
from sklearn.model_selection import StratifiedKFold

from feature_draft import estimator


class CrossValidator:
    """Class to perform cross validation model builds"""

    def __init__(self, n_splits: int = 5):

        self.n_splits = n_splits

        # TODO: Add more fold options
        self.fold_object = StratifiedKFold(n_splits=n_splits)

    def cross_validation_build(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        model: estimator.BaseEstimator
    ):
        """
        Perform a cross validation build, and return a 1d array of
        the evaluation metric on each of the holdout samples. The
        output will be length k, where k is the number of folds.

        """

        metrics_array = []

        for train_index, val_index in self.fold_object.split(X, y):

            # TODO: Offer row sampling
            X_train, y_train = X.iloc[train_index], y[train_index]
            X_val, y_val = X.iloc[val_index], y[val_index]

            metrics_array.append(model.fit_and_evaluate(
                X=X_train,
                y=y_train,
                X_val=X_val,
                y_val=y_val,
            ))

        return metrics_array
