from typing import Dict
from os import getenv
import telebot
from telebot import types
import check_data
import bot_base


bot_token = getenv('BOT_TOKEN')

bot = telebot.TeleBot(bot_token)


class User:
    """
    Вспомогательный класс нужен для сбора данных о пользователе и хранения полученных данных от него

    Args:
        user_id (int): id пользователя написавшего команду для бота

    Attributes:
        user_id (int): id пользователя написавшего команду для бота
        search_m (str): метод обработки результатов
        city (str): название города
        city_id (int): id города
        checkin (str): дата заезда в отель в виде ГГГГ-ММ-ДД
        checkout (str): дата отъезда из отеля в виде ГГГГ-ММ-ДД
        sort (str): вид сортировки в выдаче по API
        hotels (int): кол-во отелей в выдаче
        photos (int): кол-во фотографий для каждого отеля, по умолчанию 0 (не выводятся)
        price (tuple): диапазон цен в $ за одну ночь
        distance (tuple): диапазон расстояний от центра города в км.
    """

    def __init__(self, user_id):
        self.user_id: int = user_id
        self.search_m: str = ''
        self.city: str = ''
        self.city_id: int = 0
        self.checkin: str = ''
        self.checkout: str = ''
        self.sort: str = 'PRICE'
        self.hotels: int = 10
        self.photos: int = 0
        self.price: tuple = (0, 100000)
        self.distance: tuple = (0, 100)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    """Получает команду от пользователя, обрабатывает и отвечает на нее, либо перенаправляет далее."""

    if message.text == '/start':
        bot.send_message(message.from_user.id, 'Добро пожаловать в турагентство Too Easy Travel.\n'
                                               'Введите команду или /help')
    elif message.text == '/help':
        bot.send_message(message.from_user.id,
                         'Доступные команды на данном боте\n'
                         '/lowprice — вывод самых дешёвых отелей в городе\n'
                         '/highprice — вывод самых дорогих отелей в городе\n'
                         '/bestdeal — вывод отелей, наиболее подходящих по цене и расположению от центра\n'
                         '/history — вывод истории поиска отелей'
                         )

    elif message.text in ('/lowprice', '/highprice', '/bestdeal'):
        user_id = message.from_user.id
        user = User(user_id)
        user_dict[user_id] = user
        if message.text == '/lowprice':
            user.search_m = 'LowPrice'
        elif message.text == '/highprice':
            user.search_m = 'HighPrice'
        else:
            user.search_m = 'BestDeal'
        print(user.user_id, user.search_m)
        bot.send_message(message.from_user.id, "Введите название города латиницей.\nНапример: Paris или Paris, France")
        bot.register_next_step_handler(message, get_city)
    elif message.text == '/history':
        user_id = message.from_user.id
        history_text = check_data.read_history(user_id=user_id)
        bot.send_message(message.from_user.id, history_text)
    else:
        bot.send_message(message.from_user.id, 'Не понял вашу команду, повторите ввод.\n'
                                               'Чтобы увидеть все доступные команды напишите: /help ')


def get_city(message):
    """Проверяет, существует ли такой город, если да то добавляет его название и id в "user" и перенаправляет
    к следующему вопросу, если нет то отправляет в начало функции.
    Город пишется на английском языке, возможно написание с названием страны через запятую с пробелом.
    Так же возможно написание строчными буквами."""

    city = message.text
    city_id = bot_base.get_city_id(city=city)

    if city_id == 0:
        bot.send_message(message.from_user.id, "Возможно название города написано с ошибкой, попробуйте еще раз!")
        bot.register_next_step_handler(message, get_city)
    else:
        user = user_dict[message.from_user.id]
        user.city = city.split(', ')[0].capitalize()
        user.city_id = city_id
        bot.send_message(message.from_user.id, "Введите дату заезда в формате:\nГГГГ-ММ-ДД (2022-02-22)")
        bot.register_next_step_handler(message, get_checkin)


def get_checkin(message):
    """Проверяет дату заезда, если корректна добавляет ее в "user" и перенаправляет к следующему вопросу,
    если нет то отправляет в начало функции.
    Дата должна быть записана в формате: ГГГГ-ММ-ДД и не должна быть меньше текущей даты."""

    check_in_date = message.text
    if not check_data.check_date(check_in_date):
        bot.send_message(message.from_user.id, "Введенная дата не является корректной, повторите ввод!")
        bot.register_next_step_handler(message, get_checkin)
    else:
        user = user_dict[message.from_user.id]
        user.checkin = check_in_date
        bot.send_message(message.from_user.id, "Введите дату отъезда в формате:\nГГГГ-ММ-ДД (2022-03-23)")
        bot.register_next_step_handler(message, get_checkout)


def get_checkout(message):
    """Проверяет дату отъезда и диапазон дат
    Дата должна быть записана в формате: ГГГГ-ММ-ДД и не должна быть меньше либо равна "дате заезда"."""

    check_out_date = message.text
    user = user_dict[message.from_user.id]
    check_in_date = user.checkin
    if not check_data.check_date(check_out_date):
        bot.send_message(message.from_user.id, "Введенная дата не является корректной, повторите ввод!")
        bot.register_next_step_handler(message, get_checkout)
    elif not check_data.check_date_range(check_in_date, check_out_date):
        bot.send_message(message.from_user.id, "Введенная дата отъезда меньше либо равна дате заезда")
        bot.register_next_step_handler(message, get_checkout)
    else:
        user.checkout = check_out_date
        if user.search_m in ('LowPrice', 'HighPrice'):
            bot.send_message(message.from_user.id, "Введите кол-во отелей в выдаче, от 1 до 10")
            bot.register_next_step_handler(message, get_hotels_num)
        else:
            bot.send_message(message.from_user.id, "Введите диапазон цен за одну ночь в долларах сша. "
                                                   "\nНапример: 0-150 (целые числа между ними дефис `-`)")
            bot.register_next_step_handler(message, get_price_range)


def get_price_range(message):
    """Проверят правильно ли введен диапазон цен за ночь в отеле, если да то добавляет кортеж с числами в "user"
    и перенаправляет к следующему вопросу"""

    price_range = message.text
    result = check_data.check_price_distance(price_range)
    if not result:
        bot.send_message(message.from_user.id, "Введен неправильный диапазон цен, повторите ввод!")
        bot.register_next_step_handler(message, get_price_range)
    else:
        user = user_dict[message.from_user.id]
        user.price = result
        bot.send_message(message.from_user.id, "Введите диапазон расстояний от центра города, на котором"
                                               "может находиться отель в км. \nНапример: 2-10 "
                                               "(целые числа между ними дефис `-`)")
        bot.register_next_step_handler(message, get_distance_range)


def get_distance_range(message):
    """Проверят правильно ли введен диапазон расстояний от центра города, если да то добавляет кортеж с числами в "user"
    и перенаправляет к следующему вопросу"""

    distance_range = message.text
    result = check_data.check_price_distance(distance_range)
    if not result:
        bot.send_message(message.from_user.id, "Введен неправильный диапазон расстояний, повторите ввод!")
        bot.register_next_step_handler(message, get_distance_range)
    else:
        user = user_dict[message.from_user.id]
        user.distance = result
        bot.send_message(message.from_user.id, "Введите кол-во отелей в выдаче, от 1 до 10")
        bot.register_next_step_handler(message, get_hotels_num)


def get_hotels_num(message):
    """Проверяет введено ли целое число в диапазоне (1-10), если да то добавляет ее в "user"
    и перенаправляет к следующему вопросу"""

    hotels_num = message.text
    if not check_data.check_digits(hotels_num):
        bot.send_message(message.from_user.id, "Повторите ввод, нужно ввести число в диапазоне 1-10")
        bot.register_next_step_handler(message, get_hotels_num)
    else:
        user = user_dict[message.from_user.id]
        user.hotels = int(hotels_num)
        keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        yes_button = types.KeyboardButton('Да')
        no_button = types.KeyboardButton('Нет')
        keyboard.add(yes_button, no_button)
        msg = bot.send_message(
            message.from_user.id, 'Фотографии отелей будем показывать: Да/Нет (Yes/No)?', reply_markup=keyboard
        )
        bot.register_next_step_handler(msg, need_photos)


def need_photos(message):
    """Направляет по разным путям далее в зависимости от ответа пользователя, нужны ему фото или нет."""

    keyboard = types.ReplyKeyboardRemove(selective=False)
    user_answer = message.text.lower()
    if user_answer in ('да', 'yes'):
        msg = bot.send_message(
            message.from_user.id, "Введите кол-во фотографий к каждому отелю, от 1 до 10", reply_markup=keyboard
        )
        bot.register_next_step_handler(msg, get_photos)
    elif user_answer in ('нет', 'no'):
        bot.send_message(message.from_user.id, "Подождите, идет обработка...", reply_markup=keyboard)
        counting_results(message)
    else:
        bot.send_message(message.from_user.id, 'Нужно выбрать/написать: Да ли Нет?')
        bot.register_next_step_handler(message, need_photos)


def get_photos(message):
    """Проверяет введено ли целое число в диапазоне (1-10), если да то добавляет его в "user"
    и перенаправляет в последнюю функцию return_results()"""

    photos = message.text
    if not check_data.check_digits(photos):
        bot.send_message(message.from_user.id, "Повторите ввод, нужно ввести число в диапазоне 1-10")
        bot.register_next_step_handler(message, get_photos)
    else:
        user = user_dict[message.from_user.id]
        user.photos = int(photos)
        bot.send_message(message.from_user.id, "Подождите, идет обработка...")
        counting_results(message)


def counting_results(message):
    """Обрабатывает полученные данные от пользователя и направляет в print_results() для вывода в Telegram"""

    user = user_dict[message.from_user.id]
    method_kwargs = {
        'city_id': user.city_id,
        'checkin': user.checkin,
        'checkout': user.checkout,
        'sort': user.sort,
        'amount': user.hotels,
        'photos': user.photos,
        'price': user.price,
        'distance': user.distance
    }
    if user.search_m == 'HighPrice':
        method_kwargs['sort'] = 'PRICE_HIGHEST_FIRST'
    print(method_kwargs)
    search_hotels = bot_base.Hotels(**method_kwargs)
    hotels = search_hotels.hotels_bot_output_format()
    print_results(message, hotels=hotels)


def print_results(message, hotels):
    """Выводит данные пользователю по его запросу в Telegram, если ничего не нашлось, сообщает од этом"""

    user = user_dict[message.from_user.id]
    if hotels:
        hotels_to_history = []
        for hotel in hotels:
            hotels_to_history.append(hotel[0])
            bot.send_message(message.from_user.id, hotel[1], parse_mode='Markdown', disable_web_page_preview=True)
            if user.photos > 0:
                photos = check_data.photos_to_media_group(*hotel[2])
                bot.send_media_group(message.from_user.id, photos)

        check_data.write_to_history(user_id=user.user_id, method=user.search_m, hotels=hotels_to_history)
    else:
        bot.send_message(message.from_user.id, 'Ничего не нашлось..., возможно бушует очередной штамм COVID-19 '
                                               'или город находится в стране под санкциями.\n'
                                               'Можно попробовать изменить даты и сделать новый запрос.')
        print('Что-то пошло не так!')
    bot.send_message(message.from_user.id, 'Я могу еще чем-то помочь?')


def main():
    bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    user_dict: Dict[int, User] = {}
    main()
