# -*- coding: utf-8 -*-

"""Console script for test-ml."""

import click

# from testml.conf import setup_logging

from testml import TestMlRunner

__author__ = "Carlo Mazzaferro"
__copyright__ = "Carlo Mazzaferro"
__license__ = "GNU General Public License v3"


@click.command()
@click.option('-c', '--config', default='.mlrc', help='Configuration file to be read. If not passed, it will be looked'
                                                      'for in the current directory. By default, testml will look for'
                                                      'files in the following order: a .mlrc file, a setup.cfg file, '
                                                      'or a tox.ini file')
@click.option('-d', '--data', help='CSV input data to be fed to the model. The only required formatting is that it can'
                                   'be loaded by pandas and the very last column has the labels for each of the row'
                                   'inputs.', required=True)
@click.option('-s', '--metrics', help='Metrics to be used', required=True)
@click.option('-m', '--model', help='Model to be loaded', default=None)
@click.option('-l', '--loader', help='Which loader to use',
              type=click.Choice(['joblib', 'pickle', 'keras', 'tensorflow', 'infer']), default='infer')
def cli(config, data, metrics, model, loader):
    """Simple program that greets NAME for a total of COUNT times."""
    runner = TestMlRunner(config=config, data=data, metrics=metrics, model=model, loader=loader)
    print(runner.run())



