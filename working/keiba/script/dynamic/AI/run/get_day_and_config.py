from datetime import datetime
from selenium import webdriver
import subprocess

now = datetime.now()
day_now=int(now.day)
month_now=int(now.month)
year_now = now.year
weekday_now=now.weekday()

#ゼロうめ処理
if len(str(month_now)) == 1:
    month_str = "0" + str(month_now)
else:
    month_str = str(month_now)
if len(str(day_now)) == 1:
    day_str = "0" + str(day_now)
else:
    day_str = str(day_now)
year_str = str(year_now)

md=month_str+day_str
ymd=year_str+month_str+day_str

racetime_export_path="/home/aweqse/keiba/output/"+ymd+"/"+ymd+"_racetime.csv"
racetime_load_url="https://race.netkeiba.com/top/race_list.html?kaisai_date="+ymd
mkdir_path_1="/home/aweqse/keiba/output/"+ymd
mkdir_path_2="/home/aweqse/keiba/output/"+ymd+"/before_30min"
mkdir_path_3="/home/aweqse/keiba/output/"+ymd+"/before_10min"
mkdir_path_4="/home/aweqse/keiba/output/"+ymd+"/before_05min"
mkdir_path_5="/home/aweqse/keiba/output/"+ymd+"/racedata"
py_path_1=   "/home/aweqse/keiba/script/dynamic/AI/pre_race_fetch/get_racetime.py"
py_path_2=   "/home/aweqse/keiba/script/dynamic/AI/pre_race_fetch/get_odds.py"

def get_hour_min():
    now = datetime.now() #時刻を更新するのでか鳴らす呼び出す
    hour = now.hour
    minute = now.minute
    hour_min=hour*60+minute
    return hour_min

def get_weekday_sat():
    if weekday_now==5:
        return 1
    else:
        return 0

def get_weekday_sun():
    if weekday_now==6:
        return 1
    else:
        return 0

def get_weekday_oth():
    if weekday_now!=5 and weekday_now!=6:
        return 1
    else:
        return 0

def get_year():
    return year_str

def get_month():
    return month_str

def get_day():
    return day_str

def get_md():
    return md

def get_ymd():
    return ymd

def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument('--disable-gpu')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--disable-web-security')
    options.add_argument('--blink-settings=imagesEnabled=false')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    return driver

def get_pkill():
    #リソース確保のため chromeを終了する
    pkill=subprocess.run(["pkill","chrome"])
    return pkill
