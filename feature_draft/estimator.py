import lightgbm as lgbm
import pandas as pd
from sklearn import metrics


class BaseEstimator:
    """
    Base estimator class, used as a framework for
    estimators available for use in FeatureDraft.

    """

    # TODO: code skeleton estimator and metric rather than using None
    _estimator_config = {
        type(None): [None]
    }

    def __init__(self, estimator, metric=None, **kwargs):
        self.estimator = estimator
        self.metric = metric

    @property
    def estimator(self):
        return self._estimator

    @estimator.setter
    def estimator(self, estimator):
        if type(estimator) not in self._estimator_config.keys():
            raise TypeError(
                "estimator must be one of"
                f" {list(self._estimator_config.keys())},"
                f" instead got {type(estimator)}"
            )
        self._estimator = estimator

    @property
    def metric(self):
        return self._metric

    @metric.setter
    def metric(self, metric):
        if metric is None:
            # set metric to first available for estimator, if not provided
            self._metric = self._estimator_config[type(self.estimator)][0]

        elif metric not in self._estimator_config[type(self.estimator)]:
            raise ValueError("Metric supplied is not suitable for estimator")

        else:
            self._metric = metric

    # TODO: implement skeleton fit method to reduce repeated code
    def fit(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        X_val: pd.DataFrame = None,
        y_val: pd.Series = None
    ):
        pass

    # TODO: implement skeleton predict method to reduce repeated code
    def predict(self, X: pd.DataFrame):
        return None

    def evaluate(self, y_true, y_pred):
        return self.metric(y_true, y_pred)

    def fit_and_evaluate(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        X_val: pd.DataFrame = None,
        y_val: pd.Series = None
    ):
        self.fit(X, y, X_val, y_val)
        predictions = self.predict(X_val)
        return self.evaluate(y_val, predictions)


class LightGBMEstimator(BaseEstimator):
    """LightGBM implementation for FeatureDraft."""

    _estimator_config = {
        lgbm.LGBMClassifier: [metrics.roc_auc_score],
        lgbm.LGBMRegressor: [metrics.mean_squared_error]
    }

    _train_method = "fit"

    def __init__(self, estimator, **kwargs):
        super().__init__(estimator=estimator)

    def fit(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        X_val: pd.DataFrame = None,
        y_val: pd.Series = None
    ):

        # TODO: remove hard coded early stopping value into config file
        self.estimator.fit(
            X=X,
            y=y,
            eval_set=[(X_val, y_val)],
            callbacks=[
                lgbm.early_stopping(10, verbose=0),
            ],
        )

    def predict(self, X: pd.DataFrame):

        if isinstance(self.estimator, lgbm.LGBMClassifier):
            # TODO: Update so works for multi-class classification
            predictions = self.estimator.predict_proba(X)[:, 1]
        else:
            predictions = self.estimator.predict(X)

        return predictions


def build_estimator(model):
    """
    Constructor function to build estimator class
    from native estimator supplied by user.

    """

    # TODO: change from hard-coded classes
    for estimator_class in [BaseEstimator, LightGBMEstimator]:
        if type(model) in estimator_class._estimator_config.keys():
            return estimator_class(estimator=model)

    raise TypeError(
        f"model type {type(model)} is not compatible with feature_draft"
    )


# TODO: Code XGBoost Estimator
