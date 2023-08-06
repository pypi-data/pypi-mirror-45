import abc

from testml.exceptions import ModelLoadingException, ModelNotFoundException
from testml.types import ModelT, LoaderT


class Loader(LoaderT):
    """
    Base class for all loaders. A loader must implement a couple of methods, namely a `load` method and optionally
    a `find_model` model file. The latter will specify how the loader is supposed to find the desired model. If
    the `find_model` method is not specified, `testml` will look for files that match a set of typical file
    extensions commonly used to serialized models.

    """

    __metaclass__ = abc.ABCMeta

    def __init__(self, model_file: str):
        self.model_file = model_file

    @abc.abstractmethod
    def load(self) -> ModelT:
        """
        Load the model. See the `KerasLoader` and `SklearnLoader` classes for some ideas of how this is used.
        If your model requires more complicated loading processes, for instance in the case of loading from a model's
        checkpoint in TensorFlow, you should add the custom logic there.

        Returns
        -------
        Model: ModelT

        """

        raise NotImplementedError


class KerasLoader(Loader):

    def load(self) -> ModelT:
        """

        Returns
        -------
        Model: ModelT

        """

        if not self.model_file:
            raise ModelNotFoundException('Model file could not be located. Have you specified the correct extension?')
        from tensorflow.keras.models import load_model
        return load_model(self.model_file)


class SklearnLoader(Loader):

    def load(self) -> ModelT:
        """

        Returns
        -------
        Model: ModelT

        """

        from sklearn.externals import joblib
        import pickle
        try:
            return joblib.load(self.model_file)
        except (UnicodeDecodeError, TypeError):
            try:
                with open(self.model_file, 'rb') as mdl:
                    return pickle.load(mdl)
            except (UnicodeDecodeError, TypeError):
                raise ModelLoadingException('Could not load model using either pickle or joblib')


class SageMakerLoader(Loader):

    def load(self):
        """

        Returns
        -------

        """
        return self.model_file

