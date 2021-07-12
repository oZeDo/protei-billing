from contextlib import contextmanager
from time import perf_counter
import xmltodict
import json
from faker import Faker


@contextmanager
def check_execution_duration():
    """
    Measures execution duration via context manager end returns callable object with execution time in seconds
    :return: lambda() -> execution time
    """
    __start = perf_counter()
    yield lambda: perf_counter() - __start


def log_http_request(logger, request_object):
    logger.info(f"Response headers: {request_object.headers}")

    logger.info(f"Request {request_object.request.method}: {request_object.url}")
    logger.info(f"Response code: {request_object.status_code}")
    logger.info(f"Response body: {request_object.text}")
    logger.info(f"Elapsed: {request_object.elapsed}")


def get_result(xml):
    response = json.dumps(xmltodict.parse(xml, xml_attribs=False))
    response = json.loads(response)
    return response['result']


class Fake(Faker):
    pass
