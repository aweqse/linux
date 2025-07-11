import datetime
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
import mysql.connector
import subprocess
import hashlib
import unicodedata
import sys
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
    start_ym,ym_now,start_year,start_mouth=get_day()
    url_list,load_url=get_month_url(start_ym,ym_now,start_year,start_mouth)
    race_url_list=get_url_day(url_list,load_url)
    get_data(race_url_list)




def get_day():
    #プログラムを起動した日を取得する
    now = datetime.datetime.now()
    day_now=now.day
    month_now=now.month
    year_now = now.year
    weekday_now=now.weekday() #月曜日なら0が返される

    #以下テスト用
    #month_now=10
    #day_now=1
    #weekday_now=6
    #ear_now=2023

    #直前の月曜日の日にちを確定させる
    monday_value=day_now-weekday_now
    year=year_now

    #前の月曜日が先月の場合の処理
    #先月が30日の場合
    if (month_now==5 or month_now==7 or month_now==10 or month_now==12) and monday_value<=0:
        if monday_value==0:
            monday=30
        else:
            #monday_valueはマイナスの値なので+
            monday=30+(monday_value)
        month=month_now-1
    #先月が31日までの場合
    elif (month_now==1 or month_now==2 or month_now==4 or month_now==6 or month_now==8 or month_now==9 or month_now==11) and monday_value<=0:
        if monday_value==0:
            monday=31
        else:
            monday=31+(monday_value)
        month=month_now-1
        #先月が12月の場合去年の値にする
        if month==0:
            month=12
            year=year-1
    #2月の場合
    elif month_now==3 and monday_value<=0: 
        monday=28+(monday_value)
        month=month_now-1
    else: #前の月曜日が月をまたがない場合
        monday=monday_value
        year=year_now
        month=month_now

    #monday_month,monday_dayが一桁の場合０を加えて二桁にする
    year=str(year)
    month=str(month)
    monday=str(monday)
    if len(month)==1:
        month="0"+month
    if len(monday)==1:
        monday="0"+monday
    monday_ymd=year+month+monday
    print("日付の処理完了""")

    #最終更新日はバックアップファイルと同じディレクトリにあるBK_resultに書き込んであるのでそれを読みこむ
    #最終更新日はレース日なのでstart_dayを+1する。
    #mySQL_result_path="C:\\workspace\\mySQL\\BK_result.txt"
    mySQL_result_path="/home/aweqse/keiba/mysql/BK_result.txt"
    f=open(mySQL_result_path,"r",encoding="utf-8")
    result_list=f.readlines()
    f.close()
    end_lines= len(result_list)
    start_ymd=result_list[end_lines-1].strip()
    start_year=start_ymd[0]+start_ymd[1]+start_ymd[2]+start_ymd[3]
    start_mouth=start_ymd[4]+start_ymd[5]
    start_day=start_ymd[6]+start_ymd[7]
    start_day=int(start_day)+1
    start_day=str(start_day)
    start_ym=start_year+start_mouth
    start_ym=int(start_ym)
    print("最終更新日の読み込み完了")

    #バックアップの日付が月末の場合次の月に行く処理
    start_day=int(start_day)
    if start_mouth=="02" and start_day+6>28:
        start_mouth=int(start_mouth)
        start_mouth=start_mouth+1
        start_day=1
        if start_mouth==13:
            start_year=int(start_year)
            start_year=start_year+1
            start_mouth=1
            
    if start_day+6>31:
        start_mouth=int(start_mouth)
        start_mouth=start_mouth+1
        start_day=1
        if start_mouth==13:
            start_year=int(start_year)
            start_year=start_year+1
            start_mouth=1
            
    #自動の場合
    start_year=str(start_year)
    start_mouth=str(start_mouth)
    start_day=str(start_day)
    if len(start_mouth)==1:
        start_mouth="0"+start_mouth
    if len(start_day)==1:
        start_day="0"+start_day
    start_ym=start_year+start_mouth
    start_ym=int(start_ym)
    start_ymd=start_year+start_mouth+start_day

    #以下手動の場合
    ##start_year=2024
    #start_mouth=6
    #start_day=1
    #start_ym=start_year+start_mouth
    #start_ym=int(start_ym)
    #start_ymd=start_year+start_mouth+start_day

    #月が一桁の場合"0"を足す処理をする
    month_now=str(month_now)
    if len(month_now)==1:
        month_now="0"+month_now
    year_now=str(year_now)
    ym_now=year_now+month_now
    ym_now=int(ym_now)
    return start_ym,ym_now,start_year,start_mouth


def get_month_url(start_ym,ym_now,start_year,start_mouth):
    url_list=[]
    while start_ym<=ym_now:
        load_url="https://race.netkeiba.com/top/calendar.html?year="+str(start_year)+"&month="+str(start_mouth)
        driver.get(load_url)
        sleep(2)
        #ページが読み込まれたかどうかを判定する(completeで読み込まれた状態)
        page_state=driver.execute_script("return document.readyState")
        sleep(2)
        print("urlが読み込まれているかをチェックします。")
        while page_state!="complete":
            driver.get(load_url)
            print("URLの読み込みに失敗したため再読み込みします。")
            sleep(20)
            page_state=driver.execute_script("return document.readyState")
        print("url読み込み完了")

        #一か月分の開催のURLを取得してurl_listに格納する
        elements = driver.find_elements(By.XPATH, ("/html/body/div[1]/div/div[1]/div[1]/div/div[3]/table//a[@href]"))
        for element in elements:
            element=element.get_attribute("href")
            url_list.append(element)
            
        #レース結果が確定していないurlをmonday_ymdと比較し削除する
        max_index=len(url_list)
        monday_ymd=int(monday_ymd)
        start_ymd=int(start_ymd)
        index=0
        while index<max_index:
            url_list_int=int(url_list[index][-8:])
            if monday_ymd<url_list_int:
                    del url_list[index]
                    max_index=len(url_list)
                    continue
            index=index+1
        index=0
        while index<max_index:
            url_list_int=int(url_list[index][-8:])
            if url_list_int<start_ymd:
                    del url_list[index]
                    max_index=len(url_list)
                    continue
            index=index+1
        print("1ヶ月単位のURLの取得完了")
        return url_list,load_url


def get_url_day(url_list,load_url):
     #月内初めての日曜日を過ぎていない場合の処理
    if len(url_list)==0:
        print("取得する情報尾はありません")
        sys.exit()

    #バックアップのための日付を取得する
    BK_index=len(url_list)
    BK_now=url_list[BK_index-1][-8:]

    #各種変数を初期化する
    max_list=len(url_list)
    index_list=0
    race_url_list=[]

    #以下テスト
    #url_list_cache=url_list[0]
    #url_list=[]
    #url_list.append(url_list_cache)
    #test_flag=1

    #ulr_listからurlにアクセスして開催回数、競馬場、日にちを取得する
    while index_list<max_list:
        driver.get(url_list[index_list])
        
        #ページが読み込まれたかどうかを判定する(completeで読み込まれた状態)
        page_state=driver.execute_script("return document.readyState")
        sleep(2)
        print("urlが読み込まれているかをチェックします。")
        while page_state!="complete":
            driver.get(load_url)
            print("URLの読み込みに失敗したため再読み込みします。")
            sleep(20)
            page_state=driver.execute_script("return document.readyState")
        print("url読み込み完了")
        
        #1日ごとのテスト
        #driver.get("https://race.netkeiba.com/top/race_list.html?kaisai_date=20180204")
        
        #パラメーターを初期化をする
        race_url_list=[]
        #一日単位のレースのURLを取得する
        elements=driver.find_elements(By.XPATH,("/html/body/div[1]/div/div[1]/div/div[2]/div/div[1]//a[@href]"))
        for element in elements:                
            element=element.get_attribute("href")
            race_url_list.append(element)

        #余分なリンク先を削除する
        day_index=0
        max_day_index=len(race_url_list)
        while day_index<max_day_index:
            if ("payback" in race_url_list[day_index])==True or ("javascript" in race_url_list[day_index])==True  or ("top" in race_url_list[day_index])==True or ("movie" in race_url_list[day_index])==True or ("tv" in race_url_list[day_index])==True:
                del race_url_list[day_index]
                max_day_index=len(race_url_list)
            else:
                day_index=day_index+1
        
        #レースの日付を取得する
        ymd_year=(url_list[index_list][-8:-4])
        ymd_month=(url_list[index_list][-4:-2])
        ymd_day=(url_list[index_list][-2:])
        print("1日単位のURL取得完了")
        return race_url_list


def get_data(race_url_list):
    race_number_list=[]
    race_cache=0
    access_index=0
    all_race_df=[]
    access_index=0
    load_count=0
    header_array=[]
    header_flag=0
    race_cache=len(race_url_list)
    while race_cache>access_index:#ここは一括で取得したURLを条件とする　
        driver.get(race_url_list[access_index])

        page_state=driver.execute_script("return document.readyState")
        sleep(2)
        print("urlが読み込まれているかをチェックします。")
        while page_state!="complete":
            driver.get(race_url_list[access_index])
            print("URLの読み込みに失敗したため再読み込みします。")
            sleep(20)
            page_state=driver.execute_script("return document.readyState")
        print("url読み込み完了")
        print(race_url_list[access_index]+"にアクセス完了")

        #1レースごとのテスト
        #driver.get("https://race.netkeiba.com/race/result.html?race_id=202406020301")
        
        #レースの基本情報を取得する
        xpath_1="/html/body/div[1]/div[2]/div/div[1]/div[3]/div[2]"
        xpath_2="/html/body/div[1]/div[2]/div/div[1]/div[3]/div[2]/h1/span[1]"
        xpath_3="/html/body/div[1]/div[3]/div[2]/table/tbody"

        grade_dict={
        "Icon_GradeType Icon_GradeType1": "G1",
        "Icon_GradeType Icon_GradeType2": "G2",
        "Icon_GradeType Icon_GradeType3": "G3",
        "Icon_GradeType Icon_GradeType5": "OP",
        "Icon_GradeType Icon_GradeType15": "L",
        "Icon_GradeType Icon_GradeType10": "jG1",
        "Icon_GradeType Icon_GradeType11": "jG2",
        "Icon_GradeType Icon_GradeType12": "jG3",}

        #変数の初期化
        header_data=[]
        racerank_shinba=racerank_nowin=racerank_1win=racerank_2win=racerank_3win=racerank_open=0
        racegrade_g1=racegrade_g2=racegrade_g3=racegrade_l=racegrade_op=racegrade_jg1=racegrade_jg2=racegrade_jg3=0
        course_turf=course_dirt=course_jump=0
        right_handed=left_handed=other_handed=0
        course_type_A=course_type_B=course_type_C=course_type_D=course_type_out=course_type_in=course_type_two=0
        weather_sunny=weather_cloudy=weather_light_rain=weather_rain=weather_snow=weather_light_snow=weather_other=0.
        baba_good=baba_light_good=baba_light_soft=baba_soft=0
        old_3age=old_2age=old_3age_over=old_4age_over=0
        only_hinba=0
        weght_set=weght_level=weght_allowance=weght_handicap=0
        grade=""

        #headerを取得
        elements_1 = driver.find_elements(By.XPATH, xpath_1)
        for elem_1 in elements_1:
            hearder=elem_1.text.split()        

        #G1,G2等をアイコンのクラスから判別するため取り出す
        elements_2 = driver.find_elements(By.XPATH, xpath_2)
        for elem_2 in elements_2:
            class_str = elem_2.get_attribute("class")    

        #出走表を取得する
        elements_3 = driver.find_elements(By.XPATH, xpath_3)
        for elem_3 in elements_3:
            maindata = elem_3.text.split("編集")

        # class属性の一覧を取得して変数に格納する
        if len(elements_2)!=0 and (class_str in grade_dict):
            grade=grade_dict[class_str]
        
        if grade=="G1":
            racegrade_g1=1
        elif grade=="G2":
            racegrade_g2=1
        elif grade=="G3":
            racegrade_g3=1
        elif grade=="L":
            racegrade_l=1
        elif grade=="OP":
            racegrade_op=1
        elif grade=="jG1":
            racegrade_jg1=1
        elif grade=="jG2":
            racegrade_jg2=1
        elif grade=="jG3":   
            racegrade_jg3=1

        while len(hearder)!=0:
            check_1=hearder[0]
            #見本
            #match_1=re.match(r"^([牡牝セ])(\d+)$",check_2)
            coruse_and_distance=re.match(r"^[芝ダ障](\d))m$",check_1)

            if coruse_and_distance:
                if re.match(r"^芝"):
                    course_turf=1
                    distance=coruse_and_distance.group(1)
                    del hearder[0]
                    continue                           
                elif re.match(r"^ダ"):
                    course_dirt=1
                    distance=coruse_and_distance.group(1)
                    del hearder[0]
                    continue   
                elif re.match(r"^障"):
                    course_jump=1
                    distance=coruse_and_distance.group(1)
                    del hearder[0]
                    continue  
                
            if check_1=="札幌" or check_1=="函館" or check_1=="福島" or check_1=="新潟" or check_1=="中山" or check_1=="東京" or check_1=="中京" or check_1=="京都" or  check_1=="阪神"or check_1=="小倉":
                if  check_1=="新潟" or check_1=="東京"or check_1=="中京":
                    left_handed=1
                    del hearder[0]
                    continue   
                else :
                    right_handed=1
                    del hearder[0]
                    continue

            if (")" in check_1) or len(check_1)==1:
                if ("A" in check_1):
                    course_type_A=1
                    del hearder[0]
                    continue 
                elif ("B" in check_1):
                    course_type_B=1
                    del hearder[0]
                    continue 
                elif ("C" in check_1):
                    course_type_C=1
                    del hearder[0]
                    continue 
                elif ("D" in check_1):
                    course_type_D=1
                    del hearder[0]
                    continue 
                elif ("外" in check_1):
                    course_type_out=1
                    del hearder[0]
                    continue 
                elif ("内" in check_1):
                    course_type_in=1
                    del hearder[0]
                    continue 
                elif ("2周" in check_1):
                    course_type_two=1
                    del hearder[0]
                    continue 
            
            if ("天候:" in check_1):
                if check_1=="天候:晴":
                    weather_sunny=1
                    del hearder[0]
                    continue 
                elif check_1=="天候:曇":
                    weather_cloudy=1
                    del hearder[0]
                    continue 
                elif check_1=="天候:小雨":
                    weather_light_rain=1
                    del hearder[0]
                    continue 
                elif check_1==":天候:雨":
                    weather_rain=1
                    del hearder[0]
                    continue 
                elif check_1=="天候:小雪":
                    weather_cloudy=1
                    del hearder[0]
                    continue 
                elif check_1=="天候:雪":
                    weather_cloudy=1
                    del hearder[0]
                    continue 
                else:
                    weather_other=1
                    del hearder[0]
                    continue 

            if ("馬場:" in check_1):
                if check_1=="馬場:良":
                    baba_good=1
                    del hearder[0]
                    continue 
                elif check_1=="馬場:稍":
                    baba_light_good=1
                    del hearder[0]
                    continue 
                elif check_1=="馬場:重":
                    baba_light_soft=1
                    del hearder[0]
                    continue                
                elif check_1=="馬場:不":
                    baba_soft=1
                    del hearder[0]
                    continue 
            if 
            if ("サラ系" in check_1) or ("障害" in check_1):
                #年齢条件の判定のため加工する
                if ("サラ系" in check_1):
                    check_1=check_1.replace("サラ系","")
                else:
                    check_1=check_1.replace("障害","")

                if check_1=="３歳":
                    old_3age=1
                    del hearder[0]
                    continue 
                elif check_1=="２歳":
                    old_2age=1
                    del hearder[0]
                    continue 
                elif check_1=="３歳以上":
                    old_3age_over=1
                    del hearder[0]
                    continue 
                elif check_1=="４歳以上":
                    old_4age_over=1
                    del hearder[0]
                    continue 
                
            if (check_1=="新馬") or (check_1=="未勝利") or(check_1=="１勝クラス") or (check_1=="２勝クラス") or (check_1=="３勝クラス")  or (check_1=="オープン") :
                if check_1=="新馬":
                    racerank_shinba=1
                    del hearder[0]
                    continue 
                elif check_1=="未勝利":
                    racerank_nowin=1
                    del hearder[0]
                    continue 
                elif check_1=="１勝クラス":
                    racerank_1win=1
                    del hearder[0]
                    continue 
                elif check_1=="２勝クラス":
                    racerank_2win=1
                    del hearder[0]
                    continue 
                elif check_1=="３勝クラス":
                    racerank_3win=1
                    del hearder[0]
                    continue 
                elif check_1=="オープン":
                    racerank_open=1
                    del hearder[0]
                    continue 

            if ("牝" in check_1):
                if check_1=="牝" or ("牝(" in check_1):
                    only_hinba=1
                    del hearder[0]
                    continue 

            if (check_1=="馬齢") or (check_1=="定量") or(check_1=="別定") or (check_1=="ハンデ") :
                if check_1=="馬齢":
                    weght_set=1
                    del hearder[0]
                    continue 
                elif check_1=="定量":
                    weght_level=1
                    del hearder[0]
                    continue 
                elif check_1=="別定": 
                    weght_allowance=1
                    del hearder[0]
                    continue 
                elif check_1=="ハンデ":
                    weght_handicap=1
                    del hearder[0]
                    continue 
            
            if ("頭" in check_1) and 2<=len(check_1)<=3:
                    feild_size=check_1.replace("頭","")
                    del hearder[0]
                    continue
            
            del hearder[0]
            continue 

        #URLからrace_idを読み取る
        race_id=int(load_url[-12:])
            
        header_colmes=["新馬","未勝利","1勝クラス","2勝クラス","3勝クラス","オープン","G1","G2","G3","L","OP","JG1","JG2","JG3","芝","ダート","障害","距離","右","左","その他","A","B","C","D","外","内","2周","晴","曇","小雨","雨","小雪","雪","天候:その他","良","稍","重","不","3歳","2歳","3歳以上","4歳以上","牝馬限定戦","馬齢","定量","別定","ハンデ","頭数","レースID"]
        #変数の初期化
        header_data=[
        racerank_shinba,racerank_nowin,racerank_1win,racerank_2win,racerank_3win,racerank_open,
        racegrade_g1,racegrade_g2,racegrade_g3,racegrade_l,racegrade_op,racegrade_jg1,racegrade_jg2,racegrade_jg3,
        course_turf,course_dirt,course_jump,
        int(distance),
        right_handed,left_handed,other_handed,
        course_type_A,course_type_B,course_type_C,course_type_D,course_type_out,course_type_in,course_type_two,
        weather_sunny,weather_cloudy,weather_light_rain,weather_rain,weather_snow,weather_light_snow,weather_other,
        baba_good,baba_light_good,baba_light_soft,baba_soft,
        old_3age,old_2age,old_3age_over,old_4age_over,
        only_hinba,
        weght_set,weght_level,weght_allowance,weght_handicap,
        int(feild_size),
        race_id
        ]

        if header_flag==0:
            header_array.append(header_colmes)
            header_flag=1

        header_array.append(header_data)
        load_count=load_count+1
        print("ヘッダーの情報格納完了")
            
    #ブラウザを終了する
    driver.quit()






























def connct_database():
    #データベースに接続する
    conn = mysql.connector.connect(
        host='localhost',
        port='3306',
        user='root',
        password='Fujieda1217', 
        database='keiba'
    )
    cursor = conn.cursor()
    print("データベースに接続完了")













































main()