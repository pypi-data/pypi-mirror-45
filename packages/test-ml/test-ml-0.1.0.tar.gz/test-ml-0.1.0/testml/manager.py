import os
import pathlib
from collections import defaultdict
from testml.conf import ConfigParser
from testml.exceptions import ConfigFileException


class ConfigManager:

    PARSER = None
    CONFIG_FILE = None
    IS_MLRC = False
    REQUIRED_CONFIG_FILE_OPTIONS = ('run:metrics', 'run:data', 'run:model', 'run:loader')
    POSSIBLE_FILES = ['setup.cfg', 'tox.ini']
    CONFIG_SECTIONS = {'RUN': 'run', 'REPORT': 'report'}

    @classmethod
    def load_config(cls, file: str) -> None:
        cls.CONFIG_FILE = os.path.expanduser(file)
        if '.mlrc' in file:
            cls.IS_MLRC = True
            os.environ['ML_RCFILE'] = cls.CONFIG_FILE
        cls.PARSER = ConfigParser(cls.IS_MLRC)

    @classmethod
    def is_initialized(cls) -> None:
        return cls.PARSER is not None

    @classmethod
    def set_config(cls, file: str) -> None:
        if not cls.is_initialized():
            return None
        cls.CONFIG = cls.read_config_file(file)

    @classmethod
    def validate(cls, config: ConfigParser) -> ConfigParser:
        all_options = defaultdict(set)
        for option_spec in cls.REQUIRED_CONFIG_FILE_OPTIONS:
            section, option = option_spec.split(":")
            all_options[section].add(option)

        for section, options in all_options.items():
            real_section = cls.PARSER.has_section(section)
            if real_section:
                for unknown in set(config.options(section)) - options:
                    raise ConfigFileException(
                        f'Unrecognized option \'[{real_section}] {unknown}=\' in config file {cls.CONFIG_FILE}'
                        )
        return config

    @classmethod
    def read_config_file(cls, config_file: str) -> ConfigParser:
        """Read the testml configuration.

        Arguments:
            config_file: a boolean or string, see the `Coverage` class for the
                tricky details.
            all others: keyword arguments from the `Coverage` class, used for
                setting values in the configuration.

        Returns:
            config:
                config is a CoverageConfig object read from the appropriate
                configuration file.

        """
        # Build the configuration from a number

        # 2) from a file:

        cls.load_config(config_file)

        if cls.IS_MLRC:
            cls.PARSER.read(cls.CONFIG_FILE)
        else:
            files_to_try = cls.POSSIBLE_FILES
            for file in files_to_try:
                if os.path.exists(file):
                    cls.PARSER.read(file)
        return cls.validate(cls.PARSER)

    @classmethod
    def get_value(cls, section, option):
        return cls.PARSER.get(section, option)

    @classmethod
    def set_value(cls, section, option, value):
        return cls.PARSER.set(section, option, value)

    @staticmethod
    def get_extension(fpath):
        return pathlib.PurePosixPath(fpath).suffix

