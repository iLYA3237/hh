from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]



def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days
  
KEY = "96b7e38655fe45528eaa427f04ff87a7"  # 你的和风天气 API KEY
LOCATION_ID = "HE2401201350251396"        # 你要查询的城市 LocationID

def get_weather():
    url = f"https://devapi.qweather.com/v7/weather/now?location={LOCATION_ID}&key={KEY}"
    try:
        res = requests.get(url, timeout=5)
        res.raise_for_status()
        data = res.json()

        if data["code"] == "200":
            weather_text = data["now"]["text"]         # 天气状况（如 晴、多云）
            temp = int(float(data["now"]["temp"]))     # 当前温度，转为整数
            return weather_text, temp
        else:
            print(f"API 错误：{data['code']}")
            return "获取失败", 0
    except Exception as e:
        print(f"获取天气失败：{e}")
        return "获取失败", 0

  
def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  max_tries = 10
  current_tries = 0
  while current_tries < max_tries:
    words = requests.get("https://api.shadiao.pro/chp")
    if words.status_code == 200:
      return words.json()['data']['text']
    else:
      current_tries += 1
  return f"请求失败，超过了最大的请求次数：{max_tries}"
  
def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()
data = {"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
