from pytest_mock import mocker

from hamcrest import *
from dtest import Dtest
from dtest.rmqhandler import RabbitMQHandler
from dtest.results_schema import TestResultSchema, TestSuiteResultSchema

connectionConfig = {
    "host": "localhost",
    "username": "guest",
    "password": "guest",
    "exchange": "logs",
    "exchange_type": "fanout"
}
metadata = {
    "description": "This is a test suite",
    "topic": "test.dtest",
    "ruleSet": "Testing some random things",
    "dataSet": "random_data_set_123912731.csv"
}


def test_dtest_suite(mocker):
    mocker.patch.object(RabbitMQHandler, 'connect', autospec=True)
    mocker.patch.object(RabbitMQHandler, 'publishResults', autospec=True)
    mocker.patch.object(RabbitMQHandler, 'closeConnection', autospec=True)

    dt = Dtest(connectionConfig, metadata)

    assert dt.assert_that([0, 1], has_length(2), '', 1) == True

    assert dt.assert_that([0, 1], has_length(1), '', 1) == False

    for result in dt.testSuite.testResultsList:
        assert isinstance(result, TestResultSchema)

    assert dt.publish() == True

    assert isinstance(dt.testSuite, TestSuiteResultSchema)
