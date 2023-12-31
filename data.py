class Data:
    base_url = "https://qa-scooter.praktikum-services.ru/api/v1/"
    api_courier_creation = "courier"
    api_login = "courier/login"
    api_delete = "courier/"
    api_order = "orders"
    api_orders_of_courier = "orders?courierId="
    test_login = "somelogin1"
    test_password = "somepassword1"
    test_name = "somename1"
    test_login_exists = "exists"
    test_login_is_in_system = "some"
    test_password_is_in_system = "some"
    test_login_not_existing = "notexistinguser"
    default_user_payload = {'login': test_login, 'password': test_password, 'firstName': test_name}
    default_user_payload_for_login = {'login': test_login, 'password': test_password}
    response_text_same_users = "Этот логин уже используется. Попробуйте другой."
    response_text_required_field = "Недостаточно данных для создания учетной записи"
    response_text_successful_courier_creation = '{"ok":true}'
    response_text_not_enough_data_for_login = "Недостаточно данных для входа"
    response_text_credentials_not_found = "Учетная запись не найдена"
    order_payload = {"firstName": "Name", "lastName": "Last", "address": "adr", "metroStation": 4,
               "phone": "+7 800 355 35 35", "rentTime": 5, "deliveryDate": "2023-12-30", "comment": "Happy new Year",
               "color": []}

