import allure
import requests

from Base_client import BaseClient
from schemas import InputStudent


class StudentClient(BaseClient):
    """HTTP-клиент для операций со студентами."""

    @allure.step("GET /student — получить список студентов")
    def get_students(self) -> requests.Response:
        return self.get("/student")

    @allure.step("GET /student/{student_id} — получить студента по id")
    def get_student_by_id(self, student_id: int) -> requests.Response:
        return self.get(f"/student/{student_id}")

    @allure.step("POST /student — создать студента")
    def post_student(self, input_student: InputStudent) -> requests.Response:
        return self.post("/student", json=input_student.model_dump())

    @allure.step("PUT /student/{student_id} — обновить студента")
    def put_student(self, student_id: int, input_student: InputStudent) -> requests.Response:
        return self.put(
            f"/student/{student_id}",
            json=input_student.model_dump(exclude={"phone_no"}),
        )

    @allure.step("DELETE /student/{student_id} — удалить студента")
    def delete_student(self, student_id: int) -> requests.Response:
        return self.delete(f"/student/{student_id}")
