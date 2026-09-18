import requests

# 查詢地點：台北市
latitude = 25.0330
longitude = 121.5654

# ---------------------------
# 取得天氣資料
# ---------------------------
weather_url = "https://api.open-meteo.com/v1/forecast"

weather_params = {
    "latitude": latitude,
    "longitude": longitude,
    "daily": [
        "temperature_2m_max",
        "precipitation_probability_max"
    ],
    "timezone": "Asia/Taipei",
    "forecast_days": 1
}

weather_response = requests.get(
    weather_url,
    params=weather_params,
    timeout=10
)

weather_response.raise_for_status()
weather_data = weather_response.json()

date = weather_data["daily"]["time"][0]
temperature = weather_data["daily"]["temperature_2m_max"][0]
rain_probability = weather_data["daily"][
    "precipitation_probability_max"
][0]

# ---------------------------
# 取得空氣品質資料
# ---------------------------
air_url = "https://air-quality-api.open-meteo.com/v1/air-quality"

air_params = {
    "latitude": latitude,
    "longitude": longitude,
    "current": "us_aqi",
    "timezone": "Asia/Taipei"
}

air_response = requests.get(
    air_url,
    params=air_params,
    timeout=10
)

air_response.raise_for_status()
air_data = air_response.json()

aqi = air_data["current"]["us_aqi"]

# ---------------------------
# 顯示查詢結果
# ---------------------------
print("預報日期：", date)
print("最高溫度：", temperature, "°C")
print("最高降雨機率：", rain_probability, "%")
print("空氣品質 AQI：", aqi)
