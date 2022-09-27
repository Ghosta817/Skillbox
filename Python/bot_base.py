from typing import Any, Optional
import requests
import settings
import json


def get_city_id(city: str) -> int:
    """Делает запрос на Hotels.com и возвращает id города либо None если город написан с ошибкой"""

    querystring = {"query": city, "locale": settings.locale, "currency": settings.currency}
    response = requests.request("GET", settings.city_url, headers=settings.headers, params=querystring)
    data = response.json()

    try:
        for suggestion in data["suggestions"]:
            if suggestion["group"] == "CITY_GROUP":
                for entity in suggestion["entities"]:
                    if entity["type"] == "CITY" and entity["name"].lower() in city.lower():
                        print(f'get_city_id({city}) отработал штатно, результат: {entity["destinationId"]}\n')
                        result = entity["destinationId"]
                        if result is not None:
                            return result
    except KeyError:
        print('Строка не является городом')
    return 0


class Hotels:
    """
    Базовый класс Отели

    Args:
        city_id (int): id города в котором ищутся отели
        checkin (str): дата заезда в отель в виде ГГГГ-ММ-ДД
        checkout (str): дата выезда из отеля в виде ГГГГ-ММ-ДД
        sort (str): вид сортировки в выдаче по API
        amount (int): количество отелей
        photos (int): количество фотографий для отеля
        price (tuple): диапазон цен в $ за одну ночь
        distance (tuple): диапазон расстояний от центра города в км.

    Attributes:
        city_id (int): id города в котором ищутся отели
        checkin (str): дата заезда в отель в виде ГГГГ-ММ-ДД
        checkout (str): дата выезда из отеля в виде ГГГГ-ММ-ДД
        sort (str): вид сортировки в выдаче по API
        amount (int): количество отелей
        photos (int): количество фотографий для отеля
        price (tuple): диапазон цен в $ за одну ночь
        distance (tuple): диапазон расстояний от центра города в км.

    """

    def __init__(
            self, city_id: int, checkin: str, checkout: str, sort: str, amount: int,
            photos: int, price: tuple, distance: tuple) -> None:

        self.city_id = city_id
        self.checkin = checkin
        self.checkout = checkout
        self.sort = sort
        self.amount = amount
        self.photos = photos
        self.price = price
        self.distance = distance

    def _get_hotels_raw_data(self) -> Optional[dict]:
        """Делает запрос на Hotels.com и возвращает необработанный список отелей в данном городе,
        если отелей в городе нет, возвращает None."""

        try:
            querystring = {
                "destinationId": self.city_id, "pageNumber": "1", "pageSize": "25",
                "checkIn": self.checkin, "checkOut": self.checkout, "adults1": "1", "sortOrder": self.sort,
                "locale": settings.locale, "currency": settings.currency
            }
            response = requests.request("GET", settings.prop_url, headers=settings.headers, params=querystring)
            answer = response.json()
            hotels_dict = self._find_key(answer, 'results')
        except Exception:  # Тут могут быть разные исключения (пустой json, отсутствует ключ 'results')
            return None  # С первой ошибкой столкнулся уже во время работы (появилась не сразу)

        # Пишет json файл со всеми отелями в городе
        # with open(f'{self.city_id}_hotels.json', 'w', encoding='utf-8') as file:
        #     json.dump(hotels_dict, file, indent=4, ensure_ascii=False)
        print('get_hotels_raw_data() отработал штатно.\n')
        return hotels_dict

    def _processing_raw_data(self) -> Optional[list]:
        """Возвращает список словарей с информацией об отелях, только с полной информацией (адрес, цена и т.д.),
        если таких отелей не нашлось, возвращает None"""

        raw_hotels_list = self._get_hotels_raw_data()
        if raw_hotels_list:
            hotels_result_list = list()
            num_hotels = 0
            for raw_hotel in raw_hotels_list:
                hotel = dict()
                try:
                    all_nights = raw_hotel["ratePlan"]["price"]["fullyBundledPricePerStay"].split()
                    distance = round(float(raw_hotel["landmarks"][0]["distance"].split()[0]) * 1.6, 2)
                    price = raw_hotel["ratePlan"]["price"]["exactCurrent"]

                    if (self.distance[0] <= distance <= self.distance[1]) and (self.price[0] <= price <= self.price[1]):
                        hotel["id"] = raw_hotel["id"]
                        hotel["name"] = raw_hotel["name"]
                        hotel["country"] = raw_hotel["address"]["countryName"]
                        hotel["locality"] = raw_hotel["address"]["locality"]
                        hotel["street"] = raw_hotel["address"]["streetAddress"]
                        hotel["street_2"] = raw_hotel["address"]["extendedAddress"]
                        hotel["distance"] = distance
                        hotel["exactCurrent"] = int(price)
                        hotel["fullPricePerStay"] = all_nights[1]
                        hotel["Nights"] = all_nights[3][:all_nights[3].find("&")]
                        hotel["link"] = f'https://hotels.com/ho{hotel["id"]}/?q-check-in={self.checkin}&q-check-out=' \
                                        f'{self.checkout}{settings.end_of_link}'
                        hotels_result_list.append(hotel)
                        num_hotels += 1
                        if num_hotels == self.amount:
                            break
                except (KeyError, ValueError):  # Если что-то не нашлось, то просто пропускаем этот отель
                    continue

            print('processing_raw_data() отработал штатно.')
            return hotels_result_list
        return None

    def hotels_bot_output_format(self) -> Optional[list]:
        """Возвращает отформатированный для вывода в Telegram список с информацией об отелях и со списком фотографий
         (если их нужно было получить), если из processing_raw_data() получили None, возвращает None"""

        hotels_list = self._processing_raw_data()
        hotels_output_list = list()
        if hotels_list:
            for hotel in hotels_list:
                hotel_out = list()
                all_nights = f'{hotel["fullPricePerStay"]} за {hotel["Nights"]} ночи(ей), без учета налогов и сборов'
                hotel_address = ', '.join([hotel["country"], hotel["locality"], hotel["street"], hotel["street_2"]])

                hotel_out.append(hotel['name'])  # Для добавления в историю
                hotel_out.append(f"[{hotel['name']}]({hotel['link']})\n"
                                 f"Адрес: {hotel_address}\n"
                                 f"Расположен в {hotel['distance']} км от центра города\n"
                                 f"Цена за ночь: ${hotel['exactCurrent']}\n"
                                 f"Всего: {all_nights}\n")
                if self.photos > 0:
                    hotel_photos = self._get_photo(hotel["id"])
                    hotel_out.append(hotel_photos)
                hotels_output_list.append(hotel_out)
            return hotels_output_list
        return None

    @classmethod
    def _find_key(cls, struct: dict, key: str) -> Optional[Any]:
        """Рекурсивно проходит по заданной структуре и находит значение заданного ключа,
         если такого ключа нет возвращает None"""

        if key in struct:
            return struct[key]
        for sub_struct in struct.values():
            if isinstance(sub_struct, dict):
                result = cls._find_key(sub_struct, key)
                if result:
                    break
        else:
            result = None
        return result

    def _get_photo(self, hotel_id: int) -> list:
        """Отправляет запрос на Hotels.com и возвращает список со ссылками на фотографии для отеля"""

        querystring = {"id": hotel_id}
        response = requests.request("GET", settings.photos_url, headers=settings.headers, params=querystring)
        raw_data = response.json()
        photos_list = []
        for i_index in range(self.photos):
            photo_link = (raw_data["hotelImages"][i_index]["baseUrl"])
            photos_list.append(photo_link.replace('{size}', settings.photo_size))
        return photos_list


if __name__ == '__main__':
    pass
