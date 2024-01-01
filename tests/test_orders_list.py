import helper_functions
import allure


class TestOrderList:
    @allure.title('Проверяем что список заказов возвращается не пустым')
    @allure.description('Проверяем, что список заказов не пуст')
    def test_order_body_is_not_empty(self):
        response = helper_functions.get_orders_list()
        response_dict = response.json()
        assert response_dict

