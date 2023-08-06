from importlib import import_module

from testml.exceptions import LibraryNotInstalledException
from testml.types import MetricT

__metrics__ = {

    'tf': [
        'accuracy',
        'auc',
        'average_precision_at_k',
        'false_negatives',
        'false_negatives_at_thresholds',
        'false_positives',
        'false_positives_at_thresholds',
        'mean',
        'mean_absolute_error',
        'mean_cosine_distance',
        'mean_iou',
        'mean_per_class_accuracy',
        'mean_relative_error',
        'mean_squared_error',
        'mean_tensor',
        'percentage_below',
        'precision',
        'precision_at_k',
        'precision_at_thresholds',
        'precision_at_top_k',
        'recall',
        'recall_at_k',
        'recall_at_thresholds',
        'recall_at_top_k',
        'root_mean_squared_error',
        'sensitivity_at_specificity',
        'sparse_average_precision_at_k',
        'sparse_precision_at_k',
        'specificity_at_sensitivity',
        'true_negatives',
        'true_negatives_at_thresholds',
        'true_positives',
        'true_positives_at_thresholds',
    ],
    'keras': [
        'binary_accuracy',
        'categorical_accuracy',
        'sparse_top_k_categorical_accuracy',
        'top_k_categorical_accuracy',
    ],
    'sklearn': [
        'accuracy_score',
        'confusion_matrix',
        'recall_score',
        'f1_score',
        'fbeta_score',
        'precision_score',
        'cohen_kappa_score',
        'jaccard_similarity_score',
        'matthews_corrcoef',
        'zero_one_loss',
        'balanced_accuracy_score',
        'hamming_loss',
        'log_loss',
        'hinge_loss',
        'brier_score_loss'
    ]
}


class Metric(MetricT):

    __all__ = __metrics__['tf'] + __metrics__['keras'] + __metrics__['sklearn']
    LIB = None

    def __init__(self, name):
        if name not in self.__all__:
            raise ValueError(f'Invalid metric: {name}')
        self.name = name
        if self.name in __metrics__['tf']:
            self.LIB = 'tf'
            metrics = import_module('tensorflow.metrics')
        elif self.name in __metrics__['keras']:
            self.LIB = 'kears'
            metrics = import_module('tensorflow.keras.metrics')
        else:
            self.LIB = 'sklearn'
            metrics = import_module('sklearn.metrics')
        self.metric = getattr(metrics, self.name)

    def __call__(self, y_true, y_pred, **kwargs):
        if self.LIB != 'sklearn':
            try:
                import tensorflow as tf
                import tensorflow.keras.backend as K
            except ImportError:
                raise LibraryNotInstalledException(f'The metric: {self.name} requires Tensorflow to beinstalled.')
            score = self.metric(y_true, y_pred)[1]
            K.get_session().run(tf.local_variables_initializer())
            return K.eval(score)
        else:
            return self.metric(y_true, y_pred, **kwargs)

