import pytest
import helper_functions


@pytest.fixture
def courier():
    courier = helper_functions.register_new_courier_and_return_login_password()
    yield courier
    courier_id = helper_functions.get_courier_id(courier[0], courier[1])
    helper_functions.delete_courier(courier_id)
