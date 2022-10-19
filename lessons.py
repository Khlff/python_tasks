import requests

weather_api = 'b4819bc1fc3f0bac87716929d12c4f13'


def get_weath(s_city):
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/find",
                           params={'q': s_city, 'units': 'metric', 'lang': 'ru', 'APPID': weather_api})
        data = res.json()
        strana = 'Страна: ' + str(data['list'][0]['sys']['country'])
        first_str = "Температура в городе " + s_city + ': ' + str(data['list'][0]['main']['temp'])
        second_str = "Ощущается как: " + str(data['list'][0]['main']['feels_like'])
        third_str = "Влажность: " + str(data['list'][0]['main']['humidity']) + '%'
        fourth_str = "Сейчас:  " + str(data['list'][0]['weather'][0]['description'])
        rain = ''
        snow = ''
        if data['list'][0]['rain'] != None:
            rain = 'Идёт дождь'
        if data['list'][0]['snow'] != None:
            snow = 'Идёт снег'
    except Exception as e:
        print("Exception (forecast):", e)
        pass
    return [strana, first_str, second_str, third_str, fourth_str, rain, snow]


print(get_weath('Нью-Йорк'))
