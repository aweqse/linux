from datetime import datetime
import pandas as pd

now = datetime.now()
day_now=int(now.day)
month_now=int(now.month)
year_now = now.year
weekday_now=now.weekday()
hour = now.hour
minute = now.minute
hour_min=hour*60+minute

#曜日を取得する
weekday_sat=weekday_sun=weekday_oth=0
if weekday_now==5:
    weekday_sat=1
elif weekday_now==6:
    weekday_sun=1
else:
    weekday_oth=1

#数字が一桁の場合二けたにする
day_now=str(day_now)
month_now=str(month_now)
if len(day_now)==1:
    day_now="0"+str(day_now)
if len(month_now)==1:
    month_now="0"+str(month_now)
year_now=str(year_now)
ymd=year_now+month_now+day_now
md=month_now+day_now
    #テスト用
    #md="0713"

mkdir_path_1="/home/aweqse/keiba/output/"+ymd
mkdir_path_2="/home/aweqse/keiba/output/"+ymd+"/before_30min"
mkdir_path_3="/home/aweqse/keiba/output/"+ymd+"/before_10min"
mkdir_path_4="/home/aweqse/keiba/output/"+ymd+"/before_05min"
mkdir_path_5="/home/aweqse/keiba/output/"+ymd+"/racedata"
py_path_1=   "/home/aweqse/keiba/script/dynamic/AI/pre_race_fetch/get_racetime.py"
py_path_2=   "/home/aweqse/keiba/script/dynamic/AI/pre_race_fetch/get_odds.py"

