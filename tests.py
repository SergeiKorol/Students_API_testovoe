import allure

from schemas import (
    CreateStudentResponse,
    DeleteStudentResponse,
    ErrorResponse,
    GetStudentResponse,
    GetStudentsResponse,
    InputStudent,
    StudentStatus,
    UpdateStudentResponse,
)


@allure.feature("Students API")
@allure.story("Операции со студентами")
class TestStudentAPI:
    @allure.title("GET /student: созданный студент есть в списке ровно один раз")
    def test_get_students_list(self, student_session) -> None:
        with allure.step("Подготовка: создание студента"):
            student_data = InputStudent(status=StudentStatus.ACTIVE)
            create_response = student_session.post_student(student_data)
            assert create_response.status_code == 200, "Ожидали HTTP 200 от POST /student"
            created = CreateStudentResponse.model_validate_json(
                create_response.text, strict=True
            )
            student_id = created.student.id

        with allure.step("Запрос списка студентов"):
            response = student_session.get_students()
            assert response.status_code == 200, "Ожидали HTTP 200 от GET /student"

        with allure.step("Проверка: структура ответа и наличие id в списке"):
            output = GetStudentsResponse.model_validate_json(response.text, strict=True)
            assert output.status == 1, "Ожидали status=1 в теле ответа"
            assert isinstance(output.students, list), "Поле students должно быть списком"
            ids_in_list = [student.id for student in output.students]
            assert student_id in ids_in_list, (
                f"Созданный студент id={student_id} должен быть в списке students"
            )
            count = ids_in_list.count(student_id)
            assert count == 1, (
                f"Созданный студент id={student_id} должен встречаться ровно 1 раз, "
                f"а встречается {count} раз(а)"
            )

        with allure.step("Очистка: удаление созданного студента"):
            delete_response = student_session.delete_student(student_id)
            assert delete_response.status_code == 200, "Ожидали HTTP 200 от DELETE /student/{id}"

    @allure.title("POST /student: успешное создание студента")
    def test_create_student(self, student_session) -> None:
        with allure.step("Подготовка: формирование тела запроса"):
            student_data = InputStudent(status=StudentStatus.ACTIVE)

        with allure.step("Действие: создание студента"):
            response = student_session.post_student(student_data)
            assert response.status_code == 200, "Ожидали HTTP 200 от POST /student"

        with allure.step("Проверка: структура ответа"):
            output = CreateStudentResponse.model_validate_json(response.text, strict=True)
            student_id = output.student.id
            assert output.status == 1, "Ожидали status=1 в теле ответа"
            assert output.message == "Student created successfully"
            assert output.student.email == student_data.email
            assert output.student.name == student_data.name

        with allure.step("Очистка: удаление созданного студента"):
            delete_response = student_session.delete_student(student_id)
            assert delete_response.status_code == 200, "Ожидали HTTP 200 от DELETE /student/{id}"

    @allure.title("GET /student/{id}: получение существующего студента")
    def test_get_student_by_id(self, student_session) -> None:
        with allure.step("Подготовка: создание студента"):
            student_data = InputStudent(status=StudentStatus.ACTIVE)
            create_response = student_session.post_student(student_data)
            assert create_response.status_code == 200, "Ожидали HTTP 200 от POST /student"
            created = CreateStudentResponse.model_validate_json(
                create_response.text, strict=True
            )
            student_id = created.student.id

        with allure.step("Действие: GET студента по id"):
            response = student_session.get_student_by_id(student_id)
            assert response.status_code == 200, "Ожидали HTTP 200 от GET /student/{id}"

        with allure.step("Проверка: полученные данные совпадают с созданными"):
            output = GetStudentResponse.model_validate_json(response.text, strict=True)
            assert output.status == 1, "Ожидали status=1 в теле ответа"
            assert output.student.id == student_id, "ID в ответе должен совпадать с запрошенным"
            assert output.student.email == student_data.email
            assert output.student.name == student_data.name
            assert output.student.gender == student_data.gender
            assert output.student.phone_no == student_data.phone_no
            assert output.student.status == student_data.status

        with allure.step("Очистка: удаление студента"):
            delete_response = student_session.delete_student(student_id)
            assert delete_response.status_code == 200, "Ожидали HTTP 200 от DELETE /student/{id}"

    @allure.title("GET /student/{id}: Запрос несуществующего студента")
    def test_get_student_by_invalid_id(self, student_session) -> None:
        with allure.step("Действие: GET по несуществующему id"):
            response = student_session.get_student_by_id(999_999_999)
            assert response.status_code == 200, "Ожидали HTTP 200 даже если студент не найден"

        with allure.step("Проверка: ErrorResponse в теле ответа"):
            output = ErrorResponse.model_validate_json(response.text, strict=True)
            assert output.status == 0, "Ожидали status=0 для несуществующего id"
            assert "not found" in output.message.lower(), (
                "Ожидали сообщение о том, что студент не найден"
            )

    @allure.title("DELETE /student/{id}: успешное удаление")
    def test_delete_student(self, student_session) -> None:
        with allure.step("Подготовка: создание студента"):
            student_data = InputStudent(status=StudentStatus.ACTIVE)
            create_response = student_session.post_student(student_data)
            assert create_response.status_code == 200, "Ожидали HTTP 200 от POST /student"
            created = CreateStudentResponse.model_validate_json(
                create_response.text, strict=True
            )
            student_id = created.student.id

        with allure.step("Действие: удаление студента"):
            delete_response = student_session.delete_student(student_id)
            assert delete_response.status_code == 200, "Ожидали HTTP 200 от DELETE /student/{id}"

        with allure.step("Проверка: структура ответа и отсутствие студента при GET"):
            deleted = DeleteStudentResponse.model_validate_json(
                delete_response.text, strict=True
            )
            assert deleted.status == 1, "Ожидали status=1 в теле ответа удаления"
            assert deleted.message == "Student deleted successfully"
            get_response = student_session.get_student_by_id(student_id)
            assert get_response.status_code == 200, "Ожидали HTTP 200 от GET"
            not_found = ErrorResponse.model_validate_json(get_response.text, strict=True)
            assert not_found.status == 0, "После удаления GET должен вернуть status=0"
            assert "not found" in not_found.message.lower(), (
                "Ожидали сообщение, что студент не найден"
            )

    @allure.title("DELETE /student/{id}: удаление несуществующего студента")
    def test_delete_unexisting_student(self, student_session) -> None:
        with allure.step("Действие: DELETE по несуществующему id"):
            response = student_session.delete_student(999_999_999)
            assert response.status_code == 200, "Ожидали HTTP 200 от DELETE"

        with allure.step("Проверка: ErrorResponse в теле"):
            output = ErrorResponse.model_validate_json(response.text, strict=True)
            assert output.status == 0, "Ожидали status=0 для несуществующего id"
            assert "not found" in output.message.lower()

    @allure.title("PUT /student/{id}: успешное обновление данных")
    def test_update_student(self, student_session) -> None:
        with allure.step("Подготовка: создание студента"):
            student_data = InputStudent(status=StudentStatus.ACTIVE)
            create_response = student_session.post_student(student_data)
            assert create_response.status_code == 200, "Ожидали HTTP 200 от POST /student"
            created = CreateStudentResponse.model_validate_json(
                create_response.text, strict=True
            )
            assert created.status == 1, "Не удалось создать студента для теста обновления"
            student_id = created.student.id
            original_phone = created.student.phone_no

        with allure.step("Подготовка: новые данные для PUT"):
            update_data = InputStudent(
                name="Ivan Petrov Updated",
                email="petrov.updated@example.com",
                gender="female",
                status=StudentStatus.INACTIVE,
                phone_no=student_data.phone_no,
            )

        with allure.step("Действие: обновление студента"):
            update_response = student_session.put_student(student_id, update_data)
            assert update_response.status_code == 200, "Ожидали HTTP 200 от PUT /student/{id}"

        with allure.step("Проверка: структура ответа PUT и сохранение phone_no"):
            updated = UpdateStudentResponse.model_validate_json(
                update_response.text, strict=True
            )
            assert updated.status == 1, "Ожидали status=1 в теле ответа"
            assert updated.message == "Student updated successfully"
            assert updated.student.id == student_id
            assert updated.student.name == update_data.name
            assert updated.student.email == update_data.email
            assert updated.student.gender == update_data.gender
            assert updated.student.status == update_data.status
            assert updated.student.phone_no == original_phone, (
                "phone_no не передаётся в PUT и должен сохраниться после создания"
            )

        with allure.step("Проверка: GET подтверждает обновление"):
            get_response = student_session.get_student_by_id(student_id)
            assert get_response.status_code == 200, "Ожидали HTTP 200 от GET после PUT"
            fetched = GetStudentResponse.model_validate_json(get_response.text, strict=True)
            assert fetched.status == 1, "После обновления GET должен вернуть status=1"
            assert fetched.student.name == update_data.name
            assert fetched.student.phone_no == original_phone

        with allure.step("Очистка: удаление студента"):
            delete_response = student_session.delete_student(student_id)
            assert delete_response.status_code == 200, "Ожидали HTTP 200 от DELETE /student/{id}"

    @allure.title("PUT /student/{id}: обновление несуществующего студента")
    def test_update_unexisting_student(self, student_session) -> None:
        with allure.step("Подготовка: тело PUT"):
            update_data = InputStudent(
                name="aa",
                email="a@example.com",
                gender="male",
                status=StudentStatus.ACTIVE,
            )

        with allure.step("Действие: PUT по несуществующему id"):
            response = student_session.put_student(999_999_999, update_data)
            assert response.status_code == 200, "Ожидали HTTP 200 от PUT"

        with allure.step("Проверка: ErrorResponse в теле"):
            output = ErrorResponse.model_validate_json(response.text, strict=True)
            assert output.status == 0, "Ожидали status=0 для несуществующего id"
            assert "not found" in output.message.lower(), (
                "Ожидали сообщение о том, что студент не найден"
            )
