import os
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
# ---------------------------
# 多條件智慧判斷
# ---------------------------
suggestions = []

if rain_probability >= 60:
    suggestions.append("☔ 降雨機率偏高，請攜帶雨傘")

if temperature >= 33:
    suggestions.append("🔥 今日高溫，請注意防曬並補充水分")

if aqi >= 100:
    suggestions.append("😷 空氣品質不佳，建議配戴口罩")

# 如果所有數值都在正常範圍
if not suggestions:
    suggestions.append("✅ 今日天氣狀況良好，適合外出通勤")

# 將建議清單組合成多行文字
suggestion_text = "\n".join(suggestions)

# 建立完整通知訊息
message = f"""
【台北市智慧通勤提醒】

📅 預報日期：{date}
🌡️ 最高溫度：{temperature}°C
🌧️ 最高降雨機率：{rain_probability}%
🌫️ 空氣品質 AQI：{aqi}

【今日建議】
{suggestion_text}
""".strip()

print(message)

# ---------------------------
# 傳送 Telegram 通知
# ---------------------------
telegram_bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
telegram_chat_id = os.environ.get("TELEGRAM_CHAT_ID")

if not telegram_bot_token or not telegram_chat_id:
    raise ValueError("找不到 Telegram Bot Token 或 Chat ID")

telegram_url = (
    f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
)

telegram_data = {
    "chat_id": telegram_chat_id,
    "text": message
}

telegram_response = requests.post(
    telegram_url,
    data=telegram_data,
    timeout=10
)

# 必須先顯示 Telegram 回應，再檢查錯誤
print(
    "Telegram 回應狀態：",
    telegram_response.status_code,
    flush=True
)

print(
    "Telegram 回應內容：",
    telegram_response.text,
    flush=True
)

if telegram_response.status_code != 200:
    raise RuntimeError(
        f"Telegram 傳送失敗：{telegram_response.text}"
    )

print("Telegram 通勤提醒傳送成功！")
