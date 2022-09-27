from typing import Optional
import datetime
from telebot import types


def get_date() -> str:
    """Возвращает текущую дату и время используется в history"""

    now_date = datetime.datetime.now()
    return now_date.strftime('%Y-%m-%d_%H:%M:%S')


def check_date(date: str):
    """Проверка строку на то, является ли она датой, так же она не должна быть "в прошлом".
    Возвращает либо дату, если проверка пройдена, либо None"""

    try:
        valid_date = datetime.date(*map(lambda x: int(x), date.split('-')))
        if valid_date >= datetime.date.today():
            return valid_date
    except (ValueError, AttributeError, TypeError):
        print('Строка не является датой!')
    return None


def check_date_range(check_in: str, check_out: str) -> bool:
    """Проверяет диапазон дат: дата заезда (check_in) всегда должна быть строго меньше даты отъезда (check_out)."""

    try:
        checkin_date = check_date(check_in)
        checkout_date = check_date(check_out)
        if checkin_date < checkout_date:
            return True
    except TypeError:
        pass
    return False


def check_digits(num: str) -> bool:
    """Проверяет, является ли строка целым положительным числом больше 0 и меньше либо равно 10"""

    try:
        result = int(num)
        if 0 < result <= 10:
            return True
    except ValueError:
        pass
    return False


def write_to_history(user_id: int, method: str, hotels: list) -> None:
    """Записывает команду введенную пользователем и найденные отели в файл в History/id_пользователя"""

    with open(f'History/{user_id}.txt', 'a', encoding='utf-8') as w_file:
        result = f'{get_date()}\tКоманда: /{method.lower()}\nРезультаты: {", ".join(hotels)}\n\n'
        w_file.write(result)


def read_history(user_id: int) -> str:
    """Получает id пользователя и возвращает строку с историей его действий"""

    try:
        with open(f'History/{user_id}.txt', 'r', encoding='utf-8') as r_file:
            history = r_file.read()
    except FileNotFoundError:
        history = 'У Вас еще нет пока истории запросов.'
    return history


def photos_to_media_group(*photos) -> list:
    """Получает некоторое кол-во ссылок на фотографии к определенному отелю и возвращает
     специальным образом отформатированный для Бота список. Нужен для красивой выдачи в Telegram"""

    photos_list = []
    for photo in photos:
        photos_list.append(types.InputMediaPhoto(photo))
    return photos_list


def check_price_distance(text: str) -> Optional[tuple]:
    """Проверяет, является ли полученная строка диапазоном чисел расположенных по возрастанию с разделителем "-",
    если да, то возвращает кортеж из этих числе, если нет то None"""

    try:
        x1, x2 = text.split('-')
        x1, x2 = int(x1), int(x2)
        if (x1 >= 0) and (x2 > 0) and (x2 > x1):
            return x1, x2
    except ValueError:
        pass
    return None
