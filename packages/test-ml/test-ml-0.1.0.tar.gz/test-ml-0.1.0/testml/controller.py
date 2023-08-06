# -*- coding: utf-8 -*-
import os
from typing import List, Union

from testml.constants import LIKELY_EXTENSIONS
from testml.exceptions import ModelNotFoundException, ConfigException, DataNotFoundException
from testml.manager import ConfigManager
from testml.metrics import Metric

"""Top-level package for testml."""

__author__ = """Carlo Mazzaferro"""
__email__ = 'carlo.mazzaferro@gmail.com'
__version__ = '0.1.0'


class TestMlController(object):

    CONFIG_MANAGER = ConfigManager
    RUN_SECTION = ConfigManager.CONFIG_SECTIONS['RUN']
    REPORT_SECTION = ConfigManager.CONFIG_SECTIONS['REPORT']

    def __init__(self, config: str, data: str, metrics: List, model: str, loader: str):
        self.config = self.CONFIG_MANAGER.read_config_file(config)
        self._metrics = self.CONFIG_MANAGER.set_value(self.RUN_SECTION, 'metrics', metrics)

        self.libs = [lib.LIB for lib in self.metrics]

        if loader == 'sagemaker' and self.config.has_option(self.RUN_SECTION, 'model'):
            raise ConfigException('When using sagemaker loader, you must provide the model argument with the name'
                                  'of the deployed endpoint to be called')

        if not model and not self.config.has_option(self.RUN_SECTION, 'data'):
            data = self.infer_data()

        if not model and not self.config.has_option(self.RUN_SECTION, 'model'):
            model = self.infer_model()

        if loader == 'infer':
            if self.config.has_option(self.RUN_SECTION, 'loader'):
                loader = self.config.get('run', 'loader')
                if loader in ['pickle', 'joblib']:
                    loader = 'sklearn'
            else:
                loader = self.infer_loader()

        self.model = self.CONFIG_MANAGER.set_value(self.RUN_SECTION, 'model', model)
        self.loader = self.CONFIG_MANAGER.set_value(self.RUN_SECTION, 'loader', loader)
        self.data = self.CONFIG_MANAGER.set_value(self.RUN_SECTION, 'data', data)

    @property
    def metrics(self) -> List[Metric]:
        """

        Returns
        -------

        """
        if isinstance(self._metrics, str):
            if ',' in self._metrics:
                self._metrics = [i.rstrip().lstrip() for i in self._metrics.split(',')]
            else:
                self._metrics = [self._metrics]

        ms = [Metric(metric) for metric in self._metrics]
        if len(set([lib.LIB for lib in ms])) > 1:
            raise ConfigException(
                f'Metrics provided come from two different libraries. Namely: {", ".join(self.libs)}. Please provide'
                'metrics from a single library only'
            )
        return ms

    def infer_model(self) -> str:
        """

        Returns
        -------

        """
        exts = None
        for lib in self.libs:
            if lib == 'sklearn':
                exts = LIKELY_EXTENSIONS['SK-LIKE']
            else:
                exts = LIKELY_EXTENSIONS['KERAS']

        if not exts:
            raise ModelNotFoundException('Model could not be found. It either wasn\'t specified on the inputs, or'
                                         'its location could not be inferred')

        for d in [os.getcwd(), os.path.join(os.getcwd(), 'models')]:
            for file in os.listdir(d):
                ext = ConfigManager.get_extension(file)
                if ext in exts:
                    return file

        raise ModelNotFoundException('Model could not be found. It either wasn\'t specified on the inputs, or'
                                     'its location could not be inferred')

    def infer_loader(self) -> Union[List, str]:
        """

        Returns
        -------

        """
        if 'sklearn' in self.libs:
            return ['joblib', 'pickle']
        elif 'keras' in self.libs:
            return 'keras'
        else:
            return 'tensorflow'

    @staticmethod
    def infer_data() -> str:
        """

        Returns
        -------

        """
        for d in [os.getcwd(), os.path.join(os.getcwd(), 'data')]:
            for file in os.listdir(d):
                ext = ConfigManager.get_extension(file)
                if ext == '.csv':
                    return file
        raise DataNotFoundException('Data could not be inferred. Please pass it as a cli argument or add it to your'
                                    'configuration file')

