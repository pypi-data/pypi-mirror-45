import io
import abc
import json
from typing import List, Type, Dict

from testml.types import RunnerT, MetricT, MatrixT, VectorT


class Runner(RunnerT):
    __metaclass__ = abc.ABCMeta

    def __init__(self, model):
        self.model = model
        self.predictions = None

    @abc.abstractmethod
    def run(self, x, labels, metrics, **kwargs):
        ...

    def evaluate(self, labels: VectorT, metrics: List[Type[MetricT]], **kwargs) -> List:
        results = []
        for metric in metrics:
            results.append(metric(labels, self.predictions, **kwargs))
        return results


class KerasRunner(Runner):

    def run(self, x: MatrixT, labels: VectorT, metrics: List[Type[MetricT]], **kwargs) -> List:
        self.predictions = self.model.evaluate(x)
        return self.evaluate(labels, metrics, **kwargs)


class SklearnRunner(Runner):

    def run(self, x: MatrixT, labels: VectorT, metrics: List[Type[MetricT]], **kwargs) -> List:
        self.predictions = self.model.predict(x)
        return self.evaluate(labels, metrics, **kwargs)


class SageMakerRunner(Runner):

    def __int__(self):
        import boto3
        self.client = boto3.client('sagemaker-runtime')

    @staticmethod
    def input_fn_transform(x: MatrixT) -> str:
        test_file = io.StringIO()
        x.to_csv(test_file, header=None, index=None)
        return test_file.getvalue()

    @staticmethod
    def output_fn_transform(response: Dict) -> List:
        result = json.loads(response['Body'].read().decode())
        return result

    def run(self, x: MatrixT, labels: VectorT, metrics: List[Type[MetricT]], **kwargs) -> List:
        x_transf = self.input_fn_transform(x)
        response = self.client.invoke_endpoint(EndpointName=self.model, Body=x_transf, ContentType='text/csv')
        self.predictions = self.output_fn_transform(response)
        return self.evaluate(labels, metrics, **kwargs)
