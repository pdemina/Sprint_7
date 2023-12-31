import helper_functions
from data import Data
import allure
import pytest


class TestCourierLogin:
    @allure.title('Курьер может авторизоваться')
    @allure.description('Проверяем, что срабатывает логин после создания курьера с созданными параметрами')
    def test_successful_login_after_courier_creation(self, courier):
        response = helper_functions.login_courier(courier[0], courier[1])
        assert response.status_code == 200

    @allure.title('Для авторизации нужно передать все обязательные поля')
    @allure.description('Проверяем, что не срабатывает логин если поочередно водить только валидный Login без пароля и только валидный пароль без логина')
    @pytest.mark.parametrize('test_login, test_password', [
        ["", Data.test_password_is_in_system],
        [Data.test_login_is_in_system, ""]
    ])
    def test_unsuccessful_login_without_login(self, test_login, test_password):
        helper_functions.create_courier("some","some","some")
        response = helper_functions.login_courier(test_login, test_password)
        assert Data.response_text_not_enough_data_for_login in response.text
        helper_functions.delete_courier_by_login_and_password(Data.test_login_is_in_system, Data.test_password_is_in_system)

    @allure.title('Система вернёт ошибку, если неправильно указать логин или пароль')
    @allure.description('Проверяем, что не срабатывает логин если поочередно водить только валидный Login с неправильным паролем и только валидный пароль с неправильным логином')
    @pytest.mark.parametrize('test_login, test_password', [
        [Data.test_login_is_in_system, Data.test_password_is_in_system+'1'],
        [Data.test_login_is_in_system+'1', Data.test_password_is_in_system]
    ])
    def test_unsuccessful_login_without_login(self, test_login, test_password):
        helper_functions.create_courier("some", "some", "some")
        response = helper_functions.login_courier(test_login, test_password)
        assert Data.response_text_credentials_not_found in response.text
        helper_functions.delete_courier_by_login_and_password(Data.test_login_is_in_system,
                                                              Data.test_password_is_in_system)

    @allure.title('Если password поля нет, запрос возвращает ошибку')
    @allure.description('Проверяем, что если нет поля  password вернется ошибка')
    def test_unsuccessful_login_without_password(self):
        helper_functions.create_courier("some", "some", "some")
        response = helper_functions.login_courier_with_payload({'login': 'some'})
        assert Data.response_text_not_enough_data_for_login in response.text

    @allure.title('Если login поля нет, запрос возвращает ошибку')
    @allure.description('Проверяем, что если нет поля  Login вернется ошибка')
    def test_unsuccessful_login_without_login(self):
        helper_functions.create_courier("some", "some", "some")
        response = helper_functions.login_courier_with_payload({'password': 'some'})
        assert Data.response_text_not_enough_data_for_login in response.text

    @allure.title('Если авторизоваться под несуществующим пользователем, запрос возвращает ошибку')
    @allure.description('Проверяем, что вернулся ожидаемый текст ошибки')
    def test_unsuccessful_login_with_not_existing_credentials(self):
        response = helper_functions.login_courier(Data.test_login_not_existing , Data.test_password)
        assert Data.response_text_credentials_not_found in response.text

    @allure.title('Успешный запрос возвращает id')
    @allure.description('Проверяем, что возвращается не пустой id')
    def test_successful_login_after_courier_creation(self, courier):
        response = helper_functions.login_courier(courier[0], courier[1])
        assert response.json()['id'] is not ""
