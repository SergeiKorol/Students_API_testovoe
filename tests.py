from schemas import InputStudent, StudentStatus, CreateStudentResponse


class TestStudentAPI:
    def test_get_student(self, student_session):
        response = student_session.get_students()
        assert response.status_code == 200

    def test_create_student(self, student_session):
        student_data = InputStudent(status=StudentStatus.ACTIVE)
        response = student_session.post_student(student_data)
        assert response.status_code == 200, "Ожидали HTTP 200 от POST /student"
        output = CreateStudentResponse.model_validate_json(response.text, strict=True)
        assert output.status == 1, "Ожидали status=1 в теле ответа"
        assert output.message == "Student created successfully"
        assert output.student.email == student_data.email
        assert output.student.name == student_data.name
