*****
Usage
*****


************************
Testing Your First Model
************************

You can see a set of full examples `here <https://github.com/bytecubed/test-ml/blob/master/examples>`_


Quickstart
==========


To test a new model, you'll need first to serialize it. For scikit-learn-like models, you can easily do that with
either `pickle <https://docs.python.org/3/library/pickle.html>`_ or `joblib <https://scikit-learn.org/stable/modules/model_persistence.html>`_

For keras-based models, you can use keras built-in `save model method <https://www.tensorflow.org/api_docs/python/tf/keras/models/save_model>`_.

We will also need a test dataset. The format of the dataset is documented here: :ref:`Runner`. Briefly, it will
be a csv file with labels specified in the last column.

Configuration
-------------

Create a ``.mlrc`` file. See :ref:`Config` for an extensive overview of how to configure a run.

Running
-------

.. code-block:: console

    $  testml --data test.csv --metrics accuracy_score --model mdl.joblib


