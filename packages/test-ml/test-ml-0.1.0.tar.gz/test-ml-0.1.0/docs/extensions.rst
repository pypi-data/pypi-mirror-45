.. highlight:: shell


##########
Extensions
##########

The project is built with the premise of getting to a working prototype quickly without
sacrificing flexibility.

This is achieved by leveraging the full capabilities of TFS while enabling the user to interact
with a simple, expressive API.


Custom Loaders
==============

Currently, vanilla loaders for `scikit-learn <https://scikit-learn.org>`_ and and `keras <https://keras.io>`_
have been implemented. You can find the base and concrete implementations here: :class:`testml.loader.KerasLoader`
and :class:`testml.loader.SklearnLoader`. To get a sense of how you'd go about implementing a different type of loader.

.. note:: needs example

Custom Runner
=============

Like a custom loader, you can use a custom runner. For instance, you may want to specify a specifc transformation
to the data prior to running the evaluation, or maybe you require a loader for tensroflow that loads from a specific
checkpoint

.. note:: needs example


Custom Metric
=============

You can also specify a custom metric. Currently, the supported metrics are the following:

Keras/TensorFlow
----------------

::

    accuracy
    auc
    average_precision_at_k
    true_positives
    true_positives_at_thresholds
    binary_accuracy
    false_negatives
    false_negatives_at_thresholds
    false_positives
    false_positives_at_thresholds
    mean
    mean_absolute_error
    mean_cosine_distance
    mean_iou
    mean_per_class_accuracy
    mean_relative_error
    mean_squared_error
    mean_tensor
    percentage_below
    precision
    precision_at_k
    precision_at_thresholds
    precision_at_top_k
    recall
    recall_at_k
    recall_at_thresholds
    recall_at_top_k
    root_mean_squared_error
    sensitivity_at_specificity
    sparse_average_precision_at_k
    sparse_precision_at_k
    specificity_at_sensitivity
    categorical_accuracy
    sparse_top_k_categorical_accuracy
    top_k_categorical_accuracy


Scikit-Learn
------------

::

    accuracy_score
    confusion_matrix
    recall_score
    f1_score
    fbeta_score
    precision_score
    cohen_kappa_score
    jaccard_similarity_score
    matthews_corrcoef
    zero_one_loss
    balanced_accuracy_score
    hamming_loss
    log_loss
    hinge_loss
    brier_score_loss



.. note:: needs example on custom metric


