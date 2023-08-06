.. highlight:: shell

============
Installation
============

Requirements
------------

``testml`` is tested on python 3.6. It won't work in 3.7, as there is no TensorFlow release for
this python version, and it probably won't work either on 3.5 since I use f-strings extensively.

Contributions are more than welcome to make the project compatible with other python versions!

Stable release
--------------

To install neu, run this command in your terminal:

.. code-block:: console

    $ pip install testml

This is the preferred method to install neu, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/



Extras
------

Depending from which library you plan on using `test-ml`, you'll need to install it. The options are:

1. Scikit-learn support

.. code-block:: console

    $ pip install testml[sklearn]


2. XGBoost support

.. code-block:: console

    $ pip install testml[xgboost]

3. Kears support

.. code-block:: console

    $ pip install testml[tf]


4. Kears support with gpu

.. code-block:: console

    $ pip install testml[gpu]


`Keras is now part of TensorFlow <https://github.com/keras-team/keras/issues/5299>`_, so installing
tensorflow will enable you to work with any keras-based models.



From sources
------------

The sources for neu can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/carlomazzaferro/test-ml

Or download the `tarball`_:

.. code-block:: console

    $ curl  -OL https://github.com/carlomazzaferro/neu/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ python setup.py install


.. _Github repo: https://github.com/carlomazzaferro/neu
.. _tarball: https://github.com/carlomazzaferro/neu/tarball/master
