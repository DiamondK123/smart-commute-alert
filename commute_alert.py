import requests

# 查詢地點
latitude = 25.0330
longitude = 121.5654

# Open-Meteo 天氣 API
url = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": latitude,
    "longitude": longitude,
    "daily": [
        "temperature_2m_max",
        "precipitation_probability_max"
    ],
    "timezone": "Asia/Taipei",
    "forecast_days": 1
}

response = requests.get(url, params=params, timeout=10)
response.raise_for_status()

data = response.json()

date = data["daily"]["time"][0]
temperature = data["daily"]["temperature_2m_max"][0]
rain_probability = data["daily"]["precipitation_probability_max"][0]

print("預報日期：", date)
print("最高溫度：", temperature, "°C")
print("最高降雨機率：", rain_probability, "%")
