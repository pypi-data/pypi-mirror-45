import abc
from typing import List, Type

from pandas import DataFrame, Series


class MatrixT(DataFrame):
    ...


class VectorT(Series):
    ...


class ModelT(abc.ABC):

    @abc.abstractmethod
    def predict(self, x: MatrixT):
        """

        Parameters
        ----------
        x :

        Returns
        -------

        """
        ...

    @abc.abstractmethod
    def evaluate(self, x: MatrixT):
        """

        Parameters
        ----------
        x :

        Returns
        -------

        """
        ...


class LoaderT(abc.ABC):

    @abc.abstractmethod
    def load(self) -> ModelT:
        """

        Returns
        -------

        """
        ...


class MetricT(abc.ABC):

    @abc.abstractmethod
    def __call__(self, *args, **kwargs):
        """

        Parameters
        ----------
        args :
        kwargs :

        Returns
        -------

        """
        ...


class RunnerT(abc.ABC):

    @abc.abstractmethod
    def run(self, x: MatrixT, labels: VectorT, metrics: List[MetricT], **kwargs):
        """

        Parameters
        ----------
        x :
        labels :
        metrics :
        kwargs :

        Returns
        -------

        """
        ...

    @abc.abstractmethod
    def evaluate(self, labels: MatrixT, metrics: List[MetricT], **kwargs) -> List:
        """

        Parameters
        ----------
        labels :
        metrics :
        kwargs :

        Returns
        -------

        """
        ...
