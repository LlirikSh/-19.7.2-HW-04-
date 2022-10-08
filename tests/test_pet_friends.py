from builtins import len, Exception
from app import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os

pf = PetFriends()


def test_get_api_key_valid_user(email=valid_email, password=valid_password):
    '''Проверяем что код статуса запроса 200 и в переменной result
    содержится слово key'''
    status, result = pf.get_app_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    '''Проверяем что код статуса запроса 200 и список всех питомцев не пустой
    Для этого при помощи метода get_app_key() получаем ключ, сохраняем его в переменной
    api_key, затем применяем метод get_list_of_pets() и проверяем статус ответа и то
    что список питомцев не пустой'''
    _, api_key = pf.get_app_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(api_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_add_pets_with_valid_data(name='lord', animal_type='dog', age='3', pet_photo='images/dog.jpg'):
    '''Проверяем что код статуса запроса 200 и что список с добавленными данными не пустой для этого
    в переменную pet_photo сохраняем путь к файлу фотографии питомца, сохраняем ключ в переменную api_key,
    проверяем статус ответа и что в ответе содержатся добавленные данные.
     '''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_app_key(valid_email, valid_password)
    status, result = pf.add_new_pets(api_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

def test_delete_pet():
    '''Проверяем возможность удаления питомца'''
    _, api_key = pf.get_app_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

    if len(my_pets['pets']) == 0:
        pf.add_new_pets(api_key, 'Big-Lord', 'dog', '2', 'images/dog.jpg')
        _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

    pet_id = my_pets['pets'][0]['id']

    status, _ = pf.delete_pets(api_key, pet_id)
    _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

    assert status == 200
    assert pet_id not in my_pets.values()

def test_update_pet_info(name='из', animal_type='измененный', age='3'):
    '''Проверяем возможность изменения данных питомца'''
    _, api_key = pf.get_app_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(api_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("Питомцы отсутствуют")

def test_add_pet_with_a_lot_of_words_in_variable_animal_type(name='Lord', age='2', pet_photo='images/dog.jpg'):
    '''Проверка с негативным сценарием. Добавления питомца название породы которого превышает 10 слов
    Тест не будет пройден если питомец будет добавлен на сайт с названием породы состоящим из более 10 слов'''

    animal_type = 'ghjdthrf yjhhkj jhjkhkjhkjhu fdgfgdf gмиттельшнауцер ньюфаундленд аргентинский дог помесь с бриар басерон'

    _, api_key = pf.get_app_key(valid_email, valid_password)
    status, result = pf.add_new_pets(api_key, name, animal_type, age, pet_photo)

    list_animal_type = result['animal_type'].split()
    word_count = len(list_animal_type)

    assert status == 200
    assert word_count < 10, 'Питомец добавлен с названием породы больше 10 слов'

def test_get_api_key_with_wrong_password_and_correct_mail(email=valid_email, password=invalid_password):
    '''Проверяем запрос с невалидным паролем и с валидным емейлом.
    Проверяем нет ли ключа в ответе'''
    status, result = pf.get_app_key(email, password)
    assert status == 403
    assert 'key' not in result

def test_get_api_key_with_wrong_email_and_correct_password(email=invalid_email, password=valid_password):
    '''Проверяем запрос с невалидным паролем и с валидным емейлом.
    Проверяем нет ли ключа в ответе'''
    status, result = pf.get_app_key(email, password)
    assert status == 403
    assert 'key' not in result

def test_add_pet_negative_age_number(name='Lord', animal_type='dog', age='-1', pet_photo='images/dog.jpg'):
    '''Проверка с негативным сценарием. Добавление питомца с отрицательным числом в переменной age.
    Тест не будет пройден если питомец будет добавлен на сайт с отрицательным числом в поле возраст.
     '''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_app_key(valid_email, valid_password)
    _, result = pf.add_new_pets(api_key, name, animal_type, age, pet_photo)

    assert age not in result['age'], 'Питомец добавлен на сайт с отрицательным числом в поле возраст'

def test_add_pet_with_four_digit_age_number(name='Lord', animal_type='dog', age='-111', pet_photo='images/dog.jpg'):
    '''Проверка с негативным сценарием. Добавление питомца с числом более трех знаков в переменной age.
    Тест не будет пройден ели питомец будет добавлен на сайт с числом превышающим три знака в поле возраст.'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_app_key(valid_email, valid_password)
    _, result = pf.add_new_pets(api_key, name, animal_type, age, pet_photo)
    number = result['age']

    assert len(number) < 4, 'Питомец добавлен на сайт с числом привышающим 3 знака в поле возраст'

def test_add_pet_with_a_lot_of_words_in_variable_name(animal_type='dog', age='-1', pet_photo='images/dog.jpg'):
    '''Проверка с негативным сценарием. Добавления питомца имя которого превышает 10 слов
    Тест не будет пройден если питомец будет добавлен на сайт с именем состоящим из более 10 слов'''

    name = 'sjhghjgjh jhfkjsdhfkj jhdsjf ireutoi rekter;t lrgkjgkl Криспиано де ла Сантисима Тринидад Руиз и Пикассо'

    _, api_key = pf.get_app_key(valid_email, valid_password)
    status, result = pf.add_new_pets(api_key, name, animal_type, age, pet_photo)

    list_name = result['name'].split()
    word_count = len(list_name)

    assert status == 200
    assert word_count < 10, 'Питомец добавлен с именем больше 10 слов'

def test_add_pet_with_numbers_in_variable_animal_type(name='Lord', animal_type='34562', age='3',
                                                      pet_photo='images/dog.jpg'):
    '''Проверка с негативным сценарием. Добавление питомца с цифрами вместо букв в переменной animal_type.
    Тест не будет пройден если питомец будет добавлен на сайт с цифрами вместо букв в поле порода.'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_app_key(valid_email, valid_password)
    status, result = pf.add_new_pets(api_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert animal_type not in result['animal_type'], 'Питомец добавлен на сайт с цифрами вместо букв в поле порода'
