import helper_functions
from data import Data
from response_messages import ResponseMessages
import allure
import pytest


class TestCourierCreation:

    @allure.title('Курьера можно создать')
    @allure.description('Проверяем, что после создания курьера срабатывает логин с созданными параметрами')
    def test_courier_creation_successful_login_check(self, courier):
        response = helper_functions.login_courier(courier[0], courier[1])
        assert response.status_code == 200

    @allure.title('Нельзя создать двух одинаковых курьеров')
    @allure.description('Проверяем, что после повторного вызова создания курьера вернется ожидаемое сообщение')
    def test_courier_creation_data_already_in_use(self):
        response = helper_functions.create_courier(Data.test_login, Data.test_password, Data.test_name) #создаем курьера
        response = helper_functions.create_courier(Data.test_login, Data.test_password, Data.test_name) #здесь курьер не создастся тк уже существует с этими данными
        assert ResponseMessages.same_users in response.text
        helper_functions.delete_courier_by_login_and_password(Data.test_login, Data.test_password) #удаляем курьера

    @allure.title('Поля Login, password обязательные для метода создания курьера')
    @allure.description('Ожижаем сообщение валидации при пустых значениях сначала логина, затем пароля')
    @pytest.mark.parametrize('test_login, test_password, test_name', [
        ["", "pass", "name"],
        ["login", "", "name"]
    ])
    def test_courier_creation_with_empty_required_field(self, test_login, test_password, test_name):
        response = helper_functions.create_courier(test_login, test_password, test_name)
        assert ResponseMessages.required_field in response.text

    @allure.title('Запрос Создания курьера возвращает код ответа 201')
    @allure.description('Создание курьера методом Post вернет код ответа 201')
    def test_courier_creation_successful_returns_code_201(self):
        response = helper_functions.create_courier(Data.test_login, Data.test_password, Data.test_name)
        assert response.status_code == 201
        helper_functions.delete_courier_by_login_and_password(Data.test_login, Data.test_password)

    @allure.title('Успешный запрос Создания курьера возвращает ok:true')
    @allure.description('Создание курьера методом Post вернет сообщение ok:true')
    def test_courier_creation_successful_message_check(self):
        response = helper_functions.create_courier(Data.test_login, Data.test_password, Data.test_name) #создали курьера
        assert ResponseMessages.successful_courier_creation in response.text
        helper_functions.delete_courier_by_login_and_password(Data.test_login, Data.test_password) #удалили курьера

    @allure.title('Если при создании курьера нет поля Login, запрос возвращает ожидаемое сообщение')
    @allure.description('Проверяем, что при отсутствии поля login вернется ожидаемое сообщение')
    def test_courier_creation_without_login_field(self):
        payload = {'password': Data.test_password, 'firstName': Data.test_name}
        response = helper_functions.create_courier_with_payload(payload)
        assert ResponseMessages.required_field in response.text

    @allure.title('Если при создании курьера нет поля Password, запрос возвращает ожидаемое сообщение')
    @allure.description('Проверяем поведение при отсутствии поля password')
    def test_courier_creation_without_password_field(self):
        payload = {'login': Data.test_login, 'firstName': Data.test_name}
        response = helper_functions.create_courier_with_payload(payload)
        assert ResponseMessages.required_field in response.text

    @allure.title('Если создать пользователя с логином, который уже есть, возвращается ошибка.')
    @allure.description('Нельзя создать курьера с таким же login и другим password')
    def test_courier_creation_with_login_which_is_in_use(self):
        response = helper_functions.create_courier(Data.test_login_exists, Data.test_password, Data.test_name) #создаем курьера
        response = helper_functions.create_courier(Data.test_login_exists, "another password", Data.test_name)
        assert ResponseMessages.same_users in response.text
        helper_functions.delete_courier_by_login_and_password(Data.test_login_exists, Data.test_password) #удаляем курьера






