class TestMlException(Exception):
    """The base of all TestMl exceptions."""
    ...


class LibraryNotInstalledException(TestMlException):
    ...


class ConfigFileException(TestMlException):
    ...


class ConfigException(TestMlException):
    ...


class ModelLoadingException(ConfigException):
    ...


class ModelNotFoundException(ModelLoadingException):
    ...


class DataNotFoundException(ConfigException):
    ...
