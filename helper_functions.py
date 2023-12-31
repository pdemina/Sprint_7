import requests
import random
import string
import allure
from data import Data
from faker import Faker

# метод регистрации нового курьера возвращает список из логина и пароля
# если регистрация не удалась, возвращает пустой список
def register_new_courier_and_return_login_password():
    # метод генерирует строку, состоящую только из букв нижнего регистра, в качестве параметра передаём длину строки
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    # создаём список, чтобы метод мог его вернуть
    login_pass = []

    # генерируем логин, пароль и имя курьера
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    # собираем тело запроса
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    # отправляем запрос на регистрацию курьера и сохраняем ответ в переменную response
    response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)

    # если регистрация прошла успешно (код ответа 201), добавляем в список логин и пароль курьера
    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)

    # возвращаем список
    return login_pass

@allure.step('Выполняем Login метод и получаем id курьера')
def get_courier_id(login, password):
    payload = {'login': login, 'password': password}
    courier_id = requests.post(Data.base_url+Data.api_login, payload).json()['id']
    return courier_id

@allure.step('Удаляем курьера по id')
def delete_courier(courier_id):
    response = requests.delete(Data.base_url + Data.api_delete + str(courier_id))
    return response

@allure.step('Удаляем курьера по логину и паролю')
def delete_courier_by_login_and_password(login, password):
    courier_id = get_courier_id(login, password)
    delete_courier(courier_id)

@allure.step('Создаем курьера')
def create_courier(login, password, name):
    payload = {'login': login, 'password': password, 'firstName': name}
    response = requests.post(Data.base_url + Data.api_courier_creation, payload)
    return response

@allure.step('Создаем курьера')
def create_courier_with_payload(payload):
    response = requests.post(Data.base_url + Data.api_courier_creation, payload)
    return response

@allure.step('Логин курьером')
def login_courier(login, password):
    response = requests.post(Data.base_url + Data.api_login, {'login': login, 'password': password})
    return response

@allure.step('Логин курьером')
def login_courier_with_payload(payload):
    response = requests.post(Data.base_url + Data.api_login, payload)
    return response

@allure.step('Создание заказа')
def create_order(payload):
    response = requests.post(Data.base_url + Data.api_order, payload)
    return response

@allure.step('Создание заказа')
def get_order_of_courier(id_courier):
    response = requests.get(Data.base_url + Data.api_orders_of_courier+id_courier)
    return response

@allure.step('Получение списка заказов')
def get_orders_list():
    response = requests.get(Data.base_url + Data.api_order)
    return response

