import logging
from io import StringIO

import allure
import pytest
import requests

from Base_client import HTTP_LOG
from Students_client import StudentClient


@pytest.fixture(scope="session")
def session() -> requests.Session:
    return requests.Session()


@pytest.fixture(scope="session")
def student_session(session: requests.Session) -> StudentClient:
    return StudentClient(session, base_url="http://194.87.126.16/")


@pytest.fixture(autouse=True)
def attach_test_log():
    buffer = StringIO()
    handler = logging.StreamHandler(buffer)
    handler.setFormatter(logging.Formatter("%(message)s"))

    log = logging.getLogger(HTTP_LOG)
    log.setLevel(logging.INFO)
    log.addHandler(handler)

    yield

    log.removeHandler(handler)
    allure.attach(
        buffer.getvalue() or "(пустой лог)",
        name="test.log",
        attachment_type=allure.attachment_type.TEXT,
    )
