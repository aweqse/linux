from datetime import datetime
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
import re
import sys
import subprocess

#リソース確保のため chromeを終了する
subprocess.run(["pkill","chrome"])

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
ymd=year_now+month_now+day_now
md=month_now+day_now

#今日がレースの日なのかを判定する
load_url="https://race.netkeiba.com/top/"
xpath_day="/html/body/div[1]/div/div[1]/div[5]/div[2]/div/div[1]/ul"
driver.get(load_url)
page_state=driver.execute_script("return document.readyState")
sleep(5)
while page_state=="complete":
    print("url読み込み完了")
    break
else:
    print("URLの読み込みに失敗したため再読み込みします。")
    driver.get(load_url)
    sleep(10)
    page_state=driver.execute_script("return document.readyState")


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

#テスト用
md="0713"

if md in check_array:
    mkdir_path="/home/aweqse/dev/working/keiba/output/"+ymd
    path_1="/home/aweqse/dev/working/keiba/script/dynamic/AI/pre_race_fetch/get_racetime.py"
    path_2="/home/aweqse/dev/working/keiba/script/dynamic/AI/pre_race_fetch/get_racedata.py"
    path_3="/home/aweqse/dev/working/keiba/script/dynamic/AI/pre_race_fetch/get_odds.py"
    
    #生成したファイルを格納するフォルダを作る
    subprocess.run(["mkdir",mkdir_path])
    
    subprocess.run(["python3",path_1])
    subprocess.run(["python3",path_2])
    subprocess.run(["python3",path_3])

else:
    print("競馬の開催日ではないのでプログラムを終了します")
    sys.exit()
