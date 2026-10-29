from Base_client import BaseClient
from schemas import InputStudent


class StudentClient(BaseClient):
    def get_students(self):
        return self.get('/student')

    def get_student_by_id(self, student_id: int):
        return self.get('/student/{}'.format(student_id))

    def post_student(self, input_student: InputStudent):
        return self.post('/student', json=input_student.model_dump())

    def put_student(self, student_id: int, input_student: InputStudent):
        return self.put(
            f"/student/{student_id}",
            json=input_student.model_dump(exclude={"phone_no"}),
        )

    def delete_student(self, student_id: int):
        return self.delete('/student/{}'.format(student_id))