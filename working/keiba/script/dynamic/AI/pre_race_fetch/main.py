from datetime import datetime
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
import re
import sys
import subprocess

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument('--disable-gpu')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')
options.add_argument('--disable-web-security')
options.add_argument('--blink-settings=imagesEnabled=false')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--no-sandbox')

driver = webdriver.Chrome(options=options)

now = datetime.now()
day_now=int(now.day)
month_now=int(now.month)
year_now = now.year
weekday_now=now.weekday()

#数字が一桁の場合二けたにする
day_now=str(day_now)
month_now=str(month_now)
if len(day_now)==1:
    day_now="0"+str(day_now)
if len(month_now)==1:
    month_now="0"+str(month_now)
year_now=str(year_now)
    
#NNへの学習を考慮して土曜:0,日曜:1,その他:2という区分けにする
if weekday_now==5:
    weekday_now=0
elif weekday_now==6:
    weekday_now=1
else:
    weekday_now=2
ymd=year_now+month_now+day_now
md=month_now+day_now

#要素を変数に格納する
elements_day = driver.find_elements(By.XPATH, xpath_day)
for elem_3 in elements_day:
    day_elem=elem_3.text.split()
day_match=r"(\d+)月(\d+)日"
day_count=0
check_array=[]
while len(day_elem)>day_count:
    check_3=day_elem[day_count]
    check_3=re.search(day_match,check_3)
    race_month=check_3.group(1)
    race_day=check_3.group(2)
    if len(race_month)==1:
        race_month="0"+race_month
    if len(race_day)==1:
        race_day="0"+race_day
    check_4=race_month+race_day
    check_array.append(check_4)
    day_count=day_count+1
print(check_array)

if md in check_array:
    mkdir_path="/home/aweqse/dev/working/keiba/output/"+ymd
    path_1="/home/aweqse/dev/working/keiba/script/dynamic/AI/pre_race_fetch/get_racetime.py"
    path_2=""
    #生成したファイルを格納するフォルダを作る
    subprocess.run["mkdir",]
    subprocess.run["python3",path_1]


















else:
    print("競馬の開催日ではないのでプログラムを終了します")
    sys.exit()
