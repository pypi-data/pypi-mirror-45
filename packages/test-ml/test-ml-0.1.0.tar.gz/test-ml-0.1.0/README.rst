#######
test-ml
#######

.. image:: https://travis-ci.org/carlomazzaferro/neu.svg?branch=master
    :target: https://travis-ci.org/carlomazzaferro/test-ml

.. image:: https://img.shields.io/pypi/v/test-ml.svg
    :target: https://pypi.python.org/pypi/test-ml

.. image:: https://readthedocs.org/projects/test-ml/badge/?version=latest
    :target: https://test-ml.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://coveralls.io/repos/github/carlomazzaferro/test-ml/badge.svg?branch=master
    :target: https://coveralls.io/github/carlomazzaferro/test-ml?branch=master
    :alt: Coverage


Treat your machine learning models like any other software asset: properly test them and fail builds if they don't meet
your desired performance.

* Documentation: https://test-ml.readthedocs.io/en/latest/ (not live yet). For now, you can build the docs locally:

.. code-block:: console

    $ cd docs && make clean && make html

Open then ``index.html`` in the newly created ``docs/_build`` folder and you're good to go.


Overview
--------

This library enables you to easily test machine learning artifacts. Specify a set of target metric,
and the rest is taken care of.


.. note:: Status: alpha. Active development, but breaking changes may come.


Features
--------

* Rich CLI capabilities that enable you to configure metrics, input data, performance cut-offs, and more
* Small, statically typed codebase, and extensive docstrings
* Public API enabling embedding this library in any build process
* Easily extensible with custom loaders, runners, and metrics


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

