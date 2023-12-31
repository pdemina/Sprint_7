import helper_functions
from data import Data
import allure
import pytest
import json


class TestOrderCreation:

    @allure.title('тело ответа содержит track при любых возможных комбинациях цвета')
    @allure.description('Проверяем, что тело ответа будет содержать track при требуемых параметрах')
    @pytest.mark.parametrize('color', [
        '[]',
        '["BLACK"]',
        '["GREY"]',
        '["BLACK", "GREY"]'])
    def test_successful_login_after_courier_creation(self, color):
        Data.order_payload["color"] = color
        payload = Data.order_payload
        response = helper_functions.create_order(json.dumps(payload))
        assert "track" in response.text
