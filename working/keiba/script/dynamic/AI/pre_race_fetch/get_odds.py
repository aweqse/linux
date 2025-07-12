from datetime import datetime
from selenium import webdriver
import pandas as pd
from time import sleep
from selenium.webdriver.common.by import By
import re

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
    ymd=get_datetime
    win_array,umaren_array,wide_1array,sanrenpuku_array=read_csv(ymd)
    get_odds(win_array,umaren_array,wide_1array,sanrenpuku_array)

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
    return ymd

def read_csv(ymd):
    print("")
    #csvファイルを読み取りレースIDを抽出しURLを生成する
    path_1="/home/aweqse/dev/working/keiba/output/pre_odds_csv/"+str(ymd)+"_racetime.csv"
    #テスト用
    path_1="/home/aweqse/dev/working/keiba/output/pre_odds_csv/20250706_racetime.csv" 
    df = pd.read_csv(path_1,index_col=False)
    
    #カラム名を配列に格納して時刻とオッズURLを辞書型にする
    win_url="https://race.netkeiba.com/odds/index.html?race_id="
    umaren_url_1="https://race.netkeiba.com/odds/index.html?type=b4&race_id="
    wide_url_1="https://race.netkeiba.com/odds/index.html?type=b5&race_id="
    sanrenpuku_url_1="https://race.netkeiba.com/odds/index.html?type=b7&race_id="
    url_2="&housiki=c99"
    race_id=df["レースID"]
    before_30min=df["発送時刻30分前"]
    before_10min=df["発送時刻10分前"]
    before_5min=df["発送時刻5分前"]

    #urlの生成
    win_url_araay=[win_url+ str(s) for s in race_id]
    umaren_url_array=[umaren_url_1 + str(s) + url_2 for s in race_id]
    wide_url_1array=[wide_url_1 + str(s) + url_2 for s in race_id]
    sanrenpuku_url_1_array=[sanrenpuku_url_1 + str(s) + url_2 for s in race_id]
    print("urlの格納完了")
    print("辞書の作成開始")
    umaren_array={}
    win_array={}
    wide_1array={}
    sanrenpuku_array={}

    #30分前
    before_30min_win=dict(zip(before_30min, win_url_araay))
    before_30min_umaren=dict(zip(before_30min, umaren_url_array))
    before_30min_wide=dict(zip(before_30min, wide_url_1array))
    before_30min_sanrenpuku=dict(zip(before_30min, sanrenpuku_url_1_array))

    #10分前
    before_10min_win=dict(zip(before_10min, win_url_araay))
    before_10min_umaren=dict(zip(before_10min, umaren_url_array))
    before_10min_wide=dict(zip(before_10min, wide_url_1array))
    before_10min_sanrenpuku=dict(zip(before_10min, sanrenpuku_url_1_array))

    #5分前
    before_5min_win=dict(zip(before_5min, win_url_araay))
    before_5min_umaren=dict(zip(before_5min, umaren_url_array))
    before_5min_wide=dict(zip(before_5min, wide_url_1array))
    before_5min_sanrenpuku=dict(zip(before_5min, sanrenpuku_url_1_array))

    #辞書の統合
    win_array = {**before_30min_win, **before_10min_win,**before_5min_win}
    umaren_array = {**before_30min_umaren, **before_10min_umaren,**before_5min_umaren}
    wide_1array = {**before_30min_wide, **before_10min_wide,**before_5min_wide}
    sanrenpuku_array = {**before_30min_sanrenpuku, **before_10min_sanrenpuku,**before_5min_sanrenpuku}
    return win_array,umaren_array,wide_1array,sanrenpuku_array

def get_odds(win_array,umaren_array,wide_1array,sanrenpuku_array):
    #時刻を取得する
    now = datetime.now()
    hour = now.hour
    minute = now.minute
    hour_min=hour*60+minute #時刻を分に変換する

    #テスト用
    hour_min=615
    
    while hour_min<1020:
        #時刻の再取得
        now = datetime.now()
        hour = now.hour
        minute = now.minute
        hour_min=hour*60+minute 

        #テスト用
        hour_min=615
        
        while (hour_min in umaren_array):
            print("処理を開始します。")
            #urlの読み込み
            load_url_win=win_array[hour_min]
            load_url_umaren=umaren_array[hour_min]
            load_url_wide=wide_1array[hour_min]
            load_url_sanrenpuku=sanrenpuku_array[hour_min]

            xpath_win=         "/html/body/div[1]/div[3]/div[2]/div[1]/div[1]/div[1]/table"
            xpath_umaren=      "/html/body/div[1]/div[3]/div[2]/div[1]/div[3]/table/tbody"
            xpath_wide=        "/html/body/div[1]/div[3]/div[2]/div[1]/div[3]/table/tbody"
            xpath_sanrenpuku=  "/html/body/div[1]/div[3]/div[2]/div[1]/div[3]/table/tbody"

            #単勝・複勝のオッズを取得する
            driver.get(load_url_win)
            page_state=driver.execute_script("return document.readyState")
            sleep(5)
            while page_state=="complete":
                print("url読み込み完了")
                break
            else:
                print("URLの読み込みに失敗したため再読み込みします。")
                driver.get(load_url_win)
                sleep(10)
                page_state=driver.execute_script("return document.readyState")
            
            #要素を変数に格納する
            elements_win = driver.find_elements(By.XPATH, xpath_win)
            
            #現在の時刻を取得する
            now = datetime.now()
            hour = now.hour
            minute = now.minute
            win_time=hour*60+minute 

            for elem_1 in elements_win:
                win_ele=elem_1.text.replace("\n","")
            print(win_ele)
            #配列の加工
            split_match=r"(\d+)\s(\d+)\s(\d+)([^\d\s]+)\s(\d+\.\d)\s(\d+\.\d)\s*-\s*(\d+\.\d)"
            win_ele=re.findall(split_match,win_ele)
            odds_rank=win_ele.group(1)
            gate_number=win_ele.group(2)
            horse_number=win_ele.group(3)
            horse_name=win_ele.group(4)
            odds=win_ele.group(5)
            min_place=win_ele.group(6)
            max_place=win_ele.group(7)

            print(horse_name)








            #馬連の要素を取得する
            driver.get(load_url_umaren)
            page_state=driver.execute_script("return document.readyState")
            sleep(5)
            while page_state=="complete":
                print("url読み込み完了")
                break
            else:
                print("URLの読み込みに失敗したため再読み込みします。")
                driver.get(load_url_umaren)
                sleep(10)
                page_state=driver.execute_script("return document.readyState")
            
            #要素を変数に格納する
            elements_umaren = driver.find_elements(By.XPATH, xpath_umaren)
            
            #現在の時刻を取得する
            now = datetime.now()
            hour = now.hour
            minute = now.minute
            umaren_time=hour*60+minute 



            #ワイドの要素を取得する
            driver.get(load_url_wide)
            page_state=driver.execute_script("return document.readyState")
            sleep(5)
            while page_state=="complete":
                print("url読み込み完了")
                break
            else:
                print("URLの読み込みに失敗したため再読み込みします。")
                driver.get(load_url_wide)
                sleep(10)
                page_state=driver.execute_script("return document.readyState")
            
            #要素を変数に格納する
            elements_wide = driver.find_elements(By.XPATH, xpath_wide)

            #現在の時刻を取得する
            now = datetime.now()
            hour = now.hour
            minute = now.minute
            wide_time=hour*60+minute 



            #三連複の要素を取得する
            driver.get(load_url_sanrenpuku)
            page_state=driver.execute_script("return document.readyState")
            sleep(5)
            while page_state=="complete":
                print("url読み込み完了")
                break
            else:
                print("URLの読み込みに失敗したため再読み込みします。")
                driver.get(load_url_sanrenpuku)
                sleep(10)
                page_state=driver.execute_script("return document.readyState")
            
            #要素を変数に格納する
            elements_sanrenpuku = driver.find_elements(By.XPATH, xpath_sanrenpuku)

            #現在の時刻を取得する
            now = datetime.now()
            hour = now.hour
            minute = now.minute
            sanrenpuku_time=hour*60+minute 

                
            
            
            
            
            
            
            
            
            print("ダミー")










        print("該当時刻ではないので待機します")
        sleep(20)
        now = datetime.now()
        hour = now.hour
        minute = now.minute
        hour_min=hour*60+minute
        continue 

    print("競馬の終了時刻となったので待機を終了します")


    #hour=
    #while 


main()

