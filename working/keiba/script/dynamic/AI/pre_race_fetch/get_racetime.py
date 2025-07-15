from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import re
import csv
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

def main():
    datetime_array,ymd=get_datetime()
    load_url,day, month, year, week_now =get_url(datetime_array)
    wait_page(load_url)
    starttime_array,match_check_word=get_element()
    alltime_array=process_date(starttime_array,match_check_word,day,month, year, week_now )
    export_csv(alltime_array,ymd)

#現在の日にちと曜日を取得する
def get_datetime():
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
    datetime_array=[day_now,month_now,year_now,weekday_now]
    return datetime_array,ymd

#発送時刻を取得し加工する
def get_url(datetime_array):
    #日値を取り出してULRを生成する
    day, month, year, week_now = datetime_array

    #urlのため曜日を結合する
    url_str=year+month+day
    load_url="https://race.netkeiba.com/top/race_list.html?kaisai_date="+url_str
    
    #テスト用のURL
    #load_url="https://race.netkeiba.com/top/race_list.html?kaisai_date=20250713"

    driver.get(load_url)
    return load_url,day, month, year, week_now 

def wait_page(load_url):
    #ページが読み込まれているかチェックする
    print("urlが読み込まれているかをチェックします。")
    page_state=driver.execute_script("return document.readyState")
    sleep(5)
    while page_state=="complete":
        print("url読み込み完了")
        break
    else:
        print("URLの読み込みに失敗したため再読み込みします。")
        driver.get(load_url)
        sleep(20)
        page_state=driver.execute_script("return document.readyState")

def get_element():
    print("レースタイムの取得開始")
    path_1='//*[@class="RaceList_Box clearfix"]'
    elements = driver.find_elements(By.XPATH, path_1)

    #発送時刻をスクレイピングしてデータを加工する
    starttime_array=[]
    sub_check_word=["R",":","回","日目"]      
    match_check_word=["東京","中山","阪神","京都","札幌","函館","福島","新潟","中京","小倉",]                

    #余計な要素を削除して競馬場、レース数、発送時刻を配列に格納する
    for element in elements:  
        temp = element.text.split()
        for check in temp:
            if any(word in check for word in sub_check_word) or (check in match_check_word):
                starttime_array.append(check)
        return starttime_array,match_check_word

def process_date(starttime_array,match_check_word,day, month, year, week_now ):
    #30分前、10分前,5分前の時刻を算出して◯R→３０分目時刻、１０分目時刻、５分目時刻の順に配列を格納し直す最終的には[年、月、日、レースid(year+month+day+_二桁のレース番号),開催上（数字）,レース数（数字）,30分前オッズ,10分前オッス,５分前オッズ]にする        
    #競馬場を配列の先頭に追加する
    split_count=0
    add_array=[]
    alltime_array=[]
    
    #繰り返し条件のTrueは仮
    head=["年","月","日","回","日目","発送時刻30分前","発送時刻10分前","発送時刻5分前","発送時刻","レースID",]
    alltime_array.append(head)
    while len(starttime_array)>split_count:
        check_2=starttime_array[split_count]
        
        #競馬場があったら挿入するために変数に格納して配列に格納する 
        if  ("回" in check_2):
            kai=check_2.replace("回","")
            if len(kai)==1:
                kai="0"+kai
            split_count=split_count+1

        if (check_2 in match_check_word):
            place_cache=check_2
            #東京:0,中山:1,阪神:2,京都:3,札幌:4,函館:5,福島:6,新潟:7,中京:8,小倉:9
            place_dict = {"東京": "05", "中山": "06", "阪神": "09", "京都": "08","札幌": "01", "函館": "02", "福島": "03", "新潟": "04","中京": "07", "小倉": "10"}
            place_cache = place_dict.get(place_cache, -1) 
            split_count=split_count+1

        if ("日目" in check_2):
            nitime=check_2.replace("日目","")
            if len(nitime)==1:
                nitime="0"+nitime
            split_count=split_count+1

        #レース数を配列に格納する
        if re.match("^\d+R$", check_2):
            #レースID用に加工する
            race=check_2.replace("R","")
            if len(race)==1:
                race="0"+race
            split_count=split_count+1

        #時刻の場合取り出して30分前、１０分前、５分前を算出して配列に挿入する
        elif (":" in check_2):
            time_str=starttime_array[split_count]
            hour,minute=time_str.split(":")
            #30分前の時刻を算出する
            before_30minute=int(hour)*60+int(minute)-30
            #10分前の時刻を算出する
            before_10minute=int(hour)*60+int(minute)-10
            #5分前の時刻を算出する
            before_5minute=int(hour)*60+int(minute)-5
            #発送時刻を変数に格納する
            starttime=int(hour)*60+int(minute)
            #race_idを生成する
            race_id=year+place_cache+kai+nitime+race

            #配列に挿入する
            add_array.extend([year,month,day,kai,nitime,before_30minute, before_10minute, before_5minute,starttime,race_id])
            alltime_array.append(add_array)
            add_array=[]
            split_count=split_count+1

    print("レースタイムの取得完了")
    return alltime_array
    
def export_csv(alltime_array,ymd):
    #path="/home/aweqse/"+ymd+"_racetime.csv"
    path="/home/aweqse/dev/working/keiba/output/"+ymd+"/"+ymd+"_racetime.csv"
    #path="C:\\workspace\\プログラム\\競馬\\AI\\"+ymd+"_racetime.csv"
    with open(path, "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(alltime_array)

main()
