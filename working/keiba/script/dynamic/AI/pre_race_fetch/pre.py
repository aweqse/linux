from datetime import datetime
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
import re
import sys
import subprocess
import get_day_and_config

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

#今日がレースの日なのかを判定するための情報を取得する
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

#今日がレース日かを判定する
md=get_day_and_config.md

#テスト用パラメーター
#md="0713"

if md in check_array:
    mkdir_path_1=get_day_and_config.mkdir_path_1
    mkdir_path_2=get_day_and_config.mkdir_path_2
    mkdir_path_3=get_day_and_config.mkdir_path_3
    mkdir_path_4=get_day_and_config.mkdir_path_4
    mkdir_path_5=get_day_and_config.mkdir_path_5
    py_path_1=get_day_and_config.py_path_1
    py_path_2=get_day_and_config.py_path_2

    #生成したファイルを格納するフォルダを作る
    subprocess.run(["mkdir",mkdir_path_1])
    subprocess.run(["mkdir",mkdir_path_2])
    subprocess.run(["mkdir",mkdir_path_3])
    subprocess.run(["mkdir",mkdir_path_4])
    subprocess.run(["mkdir",mkdir_path_5])
    
    #プログラムを起動する
    subprocess.run(["python3",py_path_1])
    subprocess.run(["python3",py_path_2])
    subprocess.run(["pkill","chrome"])

else:
    print("競馬の開催日ではないのでプログラムを終了します")
    sys.exit()

