
from typing import Tuple, Any, List, Union, Type

import pandas


from testml.loader import KerasLoader, SklearnLoader, Loader, SageMakerLoader
from testml.runner import KerasRunner, SklearnRunner, SageMakerRunner
from testml.controller import TestMlController
from testml.types import ModelT, MatrixT, VectorT, LoaderT, RunnerT

__author__ = """Carlo Mazzaferro"""
__email__ = 'carlo.mazzaferro@gmail.com'
__version__ = '0.1.0'


class TestMlRunner(object):

    """
    Main public facing API to programmatically access testml.


    Examples
    --------

    Parameters
    ----------
    kwargs : dict
        Set of parameters to instantiate the runner. These are:

    config : str
        The configuration file to be used. `testml` will default to .mlrc and will look for it in the current
        directory. If not found, it will look for a `setup.cfg` and the for a `tox.ini`.

    metrics : List
        List of metrics to be used

    model : str
        Which model file to use. That is, the relative or full path to the serialized file that will be used. Testml
        will do its best to infer which file represents the model if this is not passed.

    loader : str
        Which loader to use for the model. Available ones are: `joblib`, `pickle`, `keras`, `tensorflow`. Testml
        will do its best to infer which loader to use if this is not passed.

    data : str
        Which data file to use. That is, the relative or full path to the data file to be used for scoring the model.


    Notes
    -----
    The input data should have the following format:

    .. code-block:: bash

        1    2   3    4   ..  y
        ---  --  ---  --  --  --
        0.1  A   1    3       0
        3    B   3    2       1
        10   C   0.4  1       0
        0    B   4    0       0


    Where labels are in the right-most columns.


    """

    def __init__(self, **kwargs):
        self.controller = TestMlController(**kwargs)
        self._x, self._y = self.load_data()
        self._model = self.load_model()
        self._metrics = self.controller.metrics

    def load_data(self) -> Tuple[MatrixT, VectorT]:
        """
        Load the validation set and its labels

        Returns
        -------

        data: Tuple[MatrixT, VectorT]
            Returns the data that will be fed through the model

        """
        data = pandas.read_csv(self.controller.data)
        label = data.columns[-1]
        return data.drop(label, axis=1), data[label]

    def load_model(self) -> ModelT:
        """

        Returns
        -------

        """
        concrete_loader = self.get_concrete_loader()
        # noinspection PyCallingNonCallable
        model = concrete_loader(self.controller.model)
        return model.load()

    def run(self, **kwargs) -> List[float]:
        """

        Parameters
        ----------
        kwargs :

        Returns
        -------

        """
        model_runner = self.get_concrete_runner()
        # noinspection PyCallingNonCallable
        concrete_runner = model_runner(self._model)
        return concrete_runner.run(self._x, self._y, self._metrics, **kwargs)

    def get_concrete_runner(self) -> Type[RunnerT]:
        """

        Returns
        -------
        Runner: RunnerT
            The correct runner class to be used, based on the controller's configured value

        """
        return {
            'sklearn': SklearnRunner,
            'keras': KerasRunner,
            'tensorflow': None,
            'sagemaker': SageMakerRunner
        }[self.controller.loader]

    def get_concrete_loader(self) -> Type[LoaderT]:
        """

        Returns
        -------
        Loader : LoaderT
            The correct loader class to be used, based on the controller's configured value

        """
        return {
            'sklearn': SklearnLoader,
            'keras': KerasLoader,
            'tensorflow': None,
            'sagemaker': SageMakerLoader,
        }[self.controller.loader]
