
class TestStudentAPI:
    def test_get_student(self, student_session):
        response = student_session.get_students()
        assert response.status_code == 200
