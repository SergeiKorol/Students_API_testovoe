import pytest
import requests
from Students_client import StudentClient


@pytest.fixture(scope="session")
def session() -> requests.Session:
    new_session = requests.Session()
    return new_session

@pytest.fixture(scope="session")
def student_session(session) -> StudentClient:
    return StudentClient(session, base_url="http://194.87.126.16/")