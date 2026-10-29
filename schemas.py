import pydantic
import faker
from enum import IntEnum
from typing import Literal

fake = faker.Faker()


class StudentStatus(IntEnum):
    INACTIVE = 0
    ACTIVE = 1

class InputStudent(pydantic.BaseModel):
    email: str = pydantic.Field(default_factory=fake.email)
    gender: str = pydantic.Field(default_factory=lambda: fake.random_element(elements=("male", "female")))
    name: str = pydantic.Field(default_factory=fake.first_name)
    phone_no: str = pydantic.Field(default_factory=fake.phone_number)
    status: StudentStatus = StudentStatus.ACTIVE

class Student(pydantic.BaseModel):
    """Объект student в ответах API."""
    id: int
    email: str
    gender: Literal["male", "female"]
    name: str
    phone_no: str
    status: StudentStatus
class CreateStudentResponse(pydantic.BaseModel):
    """Тело ответа POST /student — аналог OutputUser для create."""
    message: str
    status: int
    student: Student


