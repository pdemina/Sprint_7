import helper_functions
from data import Data
from response_messages import ResponseMessages
import allure
import pytest


class TestCourierLogin:
    @allure.title('Курьер может авторизоваться')
    @allure.description('Проверяем, что срабатывает логин после создания курьера с созданными параметрами')
    def test_successful_login_after_courier_creation(self, courier):
        response = helper_functions.login_courier(courier[0], courier[1])
        assert response.status_code == 200

    @allure.title('Для авторизации нужно передать все обязательные поля(Login и Password)')
    @allure.description('Проверяем, что не срабатывает логин если поочередно вводить только валидный логин без пароля и только валидный пароль без логина')
    @pytest.mark.parametrize('test_login, test_password', [
        ["", Data.test_password_is_in_system],
        [Data.test_login_is_in_system, ""]
    ])
    def test_unsuccessful_login_without_login_or_password_value(self, test_login, test_password):
        helper_functions.create_courier(Data.test_login_is_in_system, Data.test_password_is_in_system, Data.test_name) #создание курьера, чтобы точно убедиться что курьер есть
        response = helper_functions.login_courier(test_login, test_password) # пробуем зайти с частью данных созданного курьера
        assert ResponseMessages.not_enough_data_for_login in response.text
        helper_functions.delete_courier_by_login_and_password(Data.test_login_is_in_system, Data.test_password_is_in_system) #удаление курьера

    @allure.title('Система вернёт ошибку, если неправильно указать логин или пароль при авторизации')
    @allure.description('Проверяем, что не срабатывает логин если поочередно водить только валидный Login с неправильным паролем и только валидный пароль с неправильным логином')
    @pytest.mark.parametrize('test_login, test_password', [
        [Data.test_login_is_in_system, Data.test_password_is_in_system+'1'],
        [Data.test_login_is_in_system+'1', Data.test_password_is_in_system]
    ])
    def test_unsuccessful_login_with_incorrect_credentials(self, test_login, test_password):
        helper_functions.create_courier(Data.test_login_is_in_system, Data.test_password_is_in_system, Data.test_name) #создали курьера
        response = helper_functions.login_courier(test_login, test_password)
        assert ResponseMessages.credentials_not_found in response.text
        helper_functions.delete_courier_by_login_and_password(Data.test_login_is_in_system,
                                                              Data.test_password_is_in_system) #удалили курьера

    @allure.title('Если password поля нет, авторизация возвращает cообщение валидации')
    @allure.description('Проверяем, что если нет поля  password вернется cообщение валидации')
    def test_unsuccessful_login_without_password(self):
        helper_functions.create_courier(Data.test_login_is_in_system, Data.test_password_is_in_system, Data.test_name) # создали курьера
        response = helper_functions.login_courier_with_payload({'login': Data.test_login_is_in_system})
        assert ResponseMessages.not_enough_data_for_login in response.text
        helper_functions.delete_courier_by_login_and_password(Data.test_login_is_in_system,
                                                              Data.test_password_is_in_system)  # удалили курьера

    @allure.title('Если login поля нет, авторизация возвращает cообщение валидации')
    @allure.description('Проверяем, что если нет поля Login вернется cообщение валидации')
    def test_unsuccessful_login_without_login(self):
        helper_functions.create_courier(Data.test_login_is_in_system, Data.test_password_is_in_system, Data.test_name) # создали курьера
        response = helper_functions.login_courier_with_payload({'password': 'some'})
        assert ResponseMessages.not_enough_data_for_login in response.text
        helper_functions.delete_courier_by_login_and_password(Data.test_login_is_in_system,
                                                              Data.test_password_is_in_system)  # удалили курьера

    @allure.title('Если авторизоваться под несуществующим пользователем, запрос возвращает cообщение валидации')
    @allure.description('Проверяем, что вернулся ожидаемый текст cообщения валидации')
    def test_unsuccessful_login_with_not_existing_credentials(self):
        response = helper_functions.login_courier(Data.test_login_not_existing, Data.test_password)
        assert ResponseMessages.credentials_not_found in response.text

    @allure.title('При успешной авторизации возвращается id')
    @allure.description('Проверяем, что возвращается не пустой id')
    def test_successful_login_after_courier_creation(self, courier):
        response = helper_functions.login_courier(courier[0], courier[1])
        assert response.json()['id'] is not ""
