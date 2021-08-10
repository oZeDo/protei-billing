import pytest
from config.xgate_consts import DEFAULT_USER, DEFAULT_PASSWORD, DEFAULT_INITIATOR
from contextlib import contextmanager
from time import perf_counter
import xmltodict
import json
from faker import Faker
from hashlib import md5


def convert_to_md5(data):
    return md5(data.encode('utf-8')).hexdigest().upper()


@contextmanager
def check_execution_duration():
    """
    Measures execution duration via context manager end returns callable object with execution time in seconds
    :return: lambda() -> execution time
    """
    __start = perf_counter()
    yield lambda: perf_counter() - __start


def make_cookies_header(cookies):
    return ';'.join([x + '=' + cookies[x] for x in cookies])


def log_http_request(logger, request_object):
    logger.info(f"Response headers: {request_object.headers}")

    logger.info(f"Request {request_object.request.method}: {request_object.url}")
    logger.info(f"Response code: {request_object.status_code}")
    logger.info(f"Response body: {request_object.text}")
    logger.info(f"Elapsed: {request_object.elapsed}")


def make_auth_headers(user=None, password=None, initiator=None):
    return {
        "X-Login": DEFAULT_USER if not user else user,
        "X-Password": convert_to_md5(DEFAULT_PASSWORD if not password else password),
        "X-ReqInitiator": DEFAULT_INITIATOR if not initiator else initiator
    }


def xml_to_dict(xml):
    response = json.dumps(xmltodict.parse(xml, xml_attribs=False))
    response = json.loads(response)
    return response['result']


def get_result(__response, *, model):
    __response = xml_to_dict(__response.text)
    if __response.get("status") == "OK":
        model = model.from_dict(__response['resultObject'])
        return model
    return __response


class Fake(Faker):
    pass
