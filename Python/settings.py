# Ключ для работы с API для https://rapidapi.com по Hotels.com
# x_rapidapi_key = "f88b73ba24mshb4e08e42bef2567p150a3fjsnfe7ed5206c35"  # с 17.03      Лимит исчерпан
x_rapidapi_key = "e6e66e85bamsh00506f5ab0fc73fp131358jsn62d0d6038cc6"  # с 23.03

# Заголовки для запросов в API rapidapi.com по Hotels.com
headers = {'x-rapidapi-host': "hotels4.p.rapidapi.com", 'x-rapidapi-key': x_rapidapi_key}


# Ссылки запросов для API rapidapi.com
city_url = "https://hotels4.p.rapidapi.com/locations/v2/search"             # Поиск города
prop_url = "https://hotels4.p.rapidapi.com/properties/list"                 # Поиск отелей в конкретном городе
photos_url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"   # Поиск фотографий по конкретному отелю


# Вспомогательные переменные
currency = 'USD'    # Валюта в которой происходит выдача результатов API rapidapi.com по Hotels.com
locale = 'en_US'    # Язык на котором происходят запросы и выдача результатов API rapidapi.com по Hotels.com
# locale = 'ru_RU'
# currency = 'RUB'


# Окончание ссылки на страницу отеля для браузера
# Для корректной работы возможно надо почистить cookies
end_of_link = f'&q-rooms=1&q-room-0-adults=1&q-room-0-children=0&pos=HCOM{locale[-3:]}&locale={locale}'

# Positions
# &pos=HCOM_US&locale=en_US     # Английский язык и цены в долларах
# &pos=HCOM_RU&locale=ru_RU     # Русский язык и цены в рублях


# Размеры фотографий в выдаче
# photo_size = 'l'  # МАленькая горизонт
photo_size = 'y'    # Средняя вертикальная


# Возможные виды сортировок для выдачи с API rapidapi.com по Hotels.com
# BEST_SELLER
# STAR_RATING_HIGHEST_FIRST
# STAR_RATING_LOWEST_FIRST
# DISTANCE_FROM_LANDMARK
# GUEST_RATING
# PRICE_HIGHEST_FIRST
# PRICE
