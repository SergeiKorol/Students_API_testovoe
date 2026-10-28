from Base_client import BaseClient


class StudentClient(BaseClient):
    def get_students(self):
        return self.get('/student')

    def get_student_by_id(self, student_id):
        return self.get('/student/{}'.format(student_id))

    def post_student(self):
        return self.post('/student')

    def put_student(self, student_id):
        return self.put('/student/{}'.format(student_id))