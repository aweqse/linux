from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd
import re
import get_day_and_config

def selenium():
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
    return driver

def main(load_url,odds_win,min_odds_place,max_odds_place,odds_rank,win_time):
    driver=selenium()
    total_array,race_id=get_and_prosees_data(driver,load_url,odds_win,min_odds_place,max_odds_place,odds_rank,win_time)
    export_csv(total_array,race_id)

def  get_and_prosees_data(driver,load_url,odds_win,min_odds_place,max_odds_place,odds_rank,win_time):
    year_now=get_day_and_config.year_now
    month_now=get_day_and_config.month_now
    day_now=get_day_and_config.day_now
    weekday_sat=get_day_and_config.weekday_sat
    weekday_sun=get_day_and_config.weekday_sun
    weekday_oth=get_day_and_config.weekday_oth

    print("ヘッダーの情報格納開始")

    #テスト用URL,本番時はマスクする
    #G1
    #load_url="https://race.netkeiba.com/race/shutuba.html?race_id=202509030411"
    #g2
    #load_url="https://race.netkeiba.com/race/result.html?race_id=202505021212"
    #g3
    #load_url="https://race.netkeiba.com/race/shutuba.html?race_id=202510020411"
    #L
    #load_url="https://race.netkeiba.com/race/result.html?race_id=202508021211"
    #op
    #load_url="https://race.netkeiba.com/race/result.html?race_id=202505021111"
    #jg1
    #load_url="https://race.netkeiba.com/race/result.html?race_id=202506030711"
    #jg2
    #load_url="https://race.netkeiba.com/race/result.html?race_id=202508020708"
    #jg3
    #load_url="https://race.netkeiba.com/race/result.html?race_id=202510010708"
    #牝馬
    #load_url="https://race.netkeiba.com/race/result.html?race_id=202505010511"

    #load_url="https://race.netkeiba.com/race/shutuba.html?race_id=202505021011"
    #load_url="https://race.netkeiba.com/race/shutuba.html?race_id=202502011009"

    driver.get(load_url)

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

    #webページから情報を取得する
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
        "Icon_GradeType Icon_GradeType12": "jG3",
    }

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
    place_sapporo=place_hakodate=place_fukushima=place_nigata=place_nakayama=place_tokyo=place_chukyo=place_kyoto=place_hanshin=place_kokura=0

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

        #テスト用パラメーター
        #check_1="障1800m"

        #要素を変数に格納する処理
        if check_1=="/":
            del hearder[0]
            continue    

        #コースと距離の算出
        match_1=r"^([芝ダ障])(\d+)m$"
        check_rematch=re.match(match_1,check_1)
        if check_rematch is not None:
            course=check_rematch.group(1)
            distance=int(check_rematch.group(2))
            if course=="芝":
                course_turf=1
            elif course=="ダ":
                course_dirt=1
            else:
                course_jump=1
            del hearder[0]
            continue

        #左回り、右回りを判定する
        match_2=r"^(札幌|函館|福島|新潟|中山|東京|中京|京都|阪神|小倉)$"
        check_rematch=re.match(match_2,check_1)
        if (check_rematch is not None):
                place=check_rematch.group(1)
                if place=="札幌":
                    place_sapporo=1
                elif place=="函館":
                    place_hakodate=1
                elif place=="福島":
                    place_fukushima=1
                elif place=="新潟":
                    place_nigata=1
                elif place=="中山":
                    place_nakayama=1
                elif place=="東京":
                    place_tokyo=1
                elif place=="中京":
                    place_chukyo=1
                elif place=="京都":
                    place_tokyo=1
                elif place=="阪神":
                    place_hanshin=1
                elif place=="小倉":
                    place_kokura=1
            
                if (place=="東京"or place=="新潟"or place=="中京"):
                    left_handed=1
                else:
                    right_handed=1
                del hearder[0]
                continue

        match_3=r"(A|B|C|D|内|外|内2周)\)?"
        check_rematch=re.match(match_3,check_1)
        if (check_rematch is not None):
            course_type=check_rematch.group(1)
            if course_type=="A":
                course_type_A=1
            elif course_type=="B":
                course_type_B=1
            elif course_type=="C":
                course_type_C=1
            elif course_type=="D":
                course_type_D=1
            elif course_type=="外":
                course_type_out=1
            elif course_type=="内":
                course_type_in=1
            elif course_type=="内2周":
                course_type_two=1
            del hearder[0]
            continue 
        
        match_4=r"^(天候:[^\n]+)$"
        check_rematch=re.match(match_4,check_1)
        if (check_rematch is not None):
            course_type=check_rematch.group(1)
            if course_type=="天候:晴":
                weather_sunny=1
            elif course_type=="天候:曇":
                weather_cloudy=1
            elif course_type=="天候:小雨":
                weather_light_rain=1               
            elif course_type=="天候:雨":
                weather_rain=1                
            elif course_type=="天候:小雪":
                weather_light_snow=1                
            elif course_type=="天候:雪":
                weather_snow=1
            else:
                weather_other=1
            del hearder[0]
            continue 

        match_5=r"^(馬場:[^\n])$"
        check_rematch=re.match(match_5,check_1)
        if (check_rematch is not None):
            baba=check_rematch.group(1)
            if baba=="馬場:良":
                baba_good=1
            elif baba=="馬場:稍":
                baba_light_good=1
            elif baba=="馬場:重":
                baba_light_soft=1
            elif baba=="馬場:不":
                baba_soft=1
            del hearder[0]
            continue 

        match_6=r"^(サラ系|障害)(\d歳[^\n]*)$"
        check_rematch=re.match(match_6,check_1)
        if (check_rematch is not None):
            age=check_rematch.group(2)
            if age=="３歳":
                old_3age=1
            elif age=="２歳":
                old_2age=1
            elif age=="３歳以上":
                old_3age_over=1
            elif age=="４歳以上":
                old_4age_over=1
            del hearder[0]
            continue 

        match_7=r"^(新馬|未勝利|１勝クラス|２勝クラス|３勝クラス|オープン)$"
        check_rematch=re.match(match_7,check_1)
        if (check_rematch is not None):
            rank=check_rematch.group(1)
            if rank=="新馬":
                racerank_shinba=1
            elif rank=="未勝利":
                racerank_nowin=1
            elif rank=="１勝クラス":
                racerank_1win=1                
            elif rank=="２勝クラス":
                racerank_2win=1                
            elif rank=="３勝クラス":
                racerank_3win=1
            elif rank=="オープン":
                racerank_open=1
            del hearder[0]
            continue 

        match_8=r"^牝(\(.*?\))?$"
        check_rematch=re.match(match_8,check_1)
        if (check_rematch is not None):
            if (check_rematch is not None):
                only_hinba=1
            del hearder[0]
            continue 

        match_9=r"^(馬齢|定量|別定|ハンデ)$"
        check_rematch=re.match(match_9,check_1)
        if (check_rematch is not None):
            rank=check_rematch.group(1)
            if rank=="馬齢":
                weght_set=1
            elif rank=="定量":
                weght_level=1
            elif rank=="別定":
                weght_allowance=1                
            elif rank=="ハンデ":
                weght_handicap=1 
            del hearder[0]
            continue 
        
        match_10=r"^(\d+)頭$"
        check_rematch=re.match(match_10,check_1)
        if (check_rematch is not None):
            feild_size=check_rematch.group(1)
            del hearder[0]
            continue 
        feild_size=-1
        del hearder[0]
        continue 
    else:
        #URLからrace_idを読み取る
        race_id=int(load_url[-12:])
            
        #変数を格納する
        header_data=[
        race_id,
        year_now,month_now,day_now,weekday_sat,weekday_sun,weekday_oth,
        racerank_shinba,racerank_nowin,racerank_1win,racerank_2win,racerank_3win,racerank_open,
        racegrade_g1,racegrade_g2,racegrade_g3,racegrade_l,racegrade_op,racegrade_jg1,racegrade_jg2,racegrade_jg3,
        course_turf,course_dirt,course_jump,
        int(distance),
        place_sapporo,place_hakodate,place_fukushima,place_nigata,place_nakayama,place_tokyo,place_chukyo,place_kyoto,place_hanshin,place_kokura,        
        right_handed,left_handed,other_handed,
        course_type_A,course_type_B,course_type_C,course_type_D,course_type_out,course_type_in,course_type_two,
        weather_sunny,weather_cloudy,weather_light_rain,weather_rain,weather_snow,weather_light_snow,weather_other,
        baba_good,baba_light_good,baba_light_soft,baba_soft,
        old_3age,old_2age,old_3age_over,old_4age_over,
        only_hinba,
        weght_set,weght_level,weght_allowance,weght_handicap,
        int(feild_size)
        ]
        print("ヘッダーの情報格納完了")
    
    #配列を要素に分割する
    maindata_count=0
    total_array=[]
    data_colme=["レースID","年","月","日","土曜日","日曜日","その他","新馬","未勝利","1勝クラス","2勝クラス","3勝クラス","オープン","G1","G2","G3","L","OP","JG1","JG2","JG3",
                "芝","ダート","障害","距離","札幌競馬場","函館競馬場","福島競馬場","新潟競馬場","中山競馬場","東京競馬場","中京競馬場","京都競馬場","阪神競馬場","小倉競馬場",
                "右","左","その他","A","B","C","D","外","内","2周","晴","曇","小雨","雨","小雪","雪","天候:その他","良","稍","重","不",
                "3歳","2歳","3歳以上","4歳以上","牝馬限定戦","馬齢","定量","別定","ハンデ","頭数","枠番","馬番","馬名","馬ID","牡馬","牝馬","騙馬","馬齢","斤量",
                "騎手","騎手ID","美浦","栗東","海外","調教師","調教師ID","馬体重","増減","単勝オッズ","最低複勝オッズ","最高複勝オッズ","単勝人気","オッズ取得時刻"]
    print("出走馬の情報を取得開始")
    total_array.append(data_colme)
    match_11=r"\s*(\d+)\s+(\d+)\s+([^\s]+)\s+([牝牡セ])(\d+)\s+(\d+\.\d)\s+([^\s]+)\s+(栗東|美浦|海外)([^\s]+)\s+(\d+)\(([-+]?\d+|前計不)\)"
    match_12=r"\s*(\d+)\s+(\d+)\s+(除外|取消)?\s*([^\s]+)\s+([牝牡セ])(\d+)\s+(\d+\.\d)?\s*([^\s]+)?\s*(栗東|美浦|海外)?([^\s]+)?"
    
    while len(maindata)>maindata_count:
        #変数の初期化
        sex_male=sex_female=sex_gelding=0
        belong_east=belong_west=belong_oversea=0
        
        #判定する配列を取り出す
        check_2=maindata[maindata_count]
        if len(check_2)==0:
            maindata_count=maindata_count+1
            pass
        else:
            #余計な文字を空白に置き換えてまとめて削除して要素に分割する
            check_2 = check_2.replace("--", " ").replace("\n", " ")
            re_match=re.match(match_11,str(check_2))
            re_match_2=re.match(match_12,str(check_2))

            #除外,取消がないい場合は通常の処理、ある場合はスキップする
            if re_match:
                wakuban=re_match.group(1)
                umaban=re_match.group(2)
                horse_name=re_match.group(3)

                #horse_idのテーブルができたらそこから取り出す処理を書くので仮の値で-10
                horse_id=-10
                
                sex=re_match.group(4)
                if sex=="牡":
                    sex_male=1
                elif sex=="牝":
                    sex_female=1
                elif sex=="セ":
                    sex_gelding=1
                horse_age=re_match.group(5)
                assigned_weight=re_match.group(6)
                jockey=re_match.group(7)

                #jockey_idのテーブルができたらそこから取り出す処理を書くので仮の値で-10
                kopckey_id=-10

                belong_trainer=re_match.group(8)
                if belong_trainer=="美浦":
                    belong_east=1
                elif belong_trainer=="栗東":
                    belong_west=1
                elif belong_trainer=="海外":
                    belong_oversea=1
                trainer=re_match.group(9)

                #trainer_idのテーブルができたらそこから取り出す処理を書くので仮の値で-10
                trainer_id=-10
        
                horse_weight=re_match.group(10)
                if horse_weight=="前計不":
                    horse_weight=-1
                weight_change=re_match.group(11)

                #変数を入れ配列を作成する
                maindate_array=[ int(wakuban),int(umaban),horse_name,horse_id,sex_male,sex_female,sex_gelding,
                                int(horse_age),float(assigned_weight),jockey,kopckey_id,belong_east,belong_west,belong_oversea,
                                trainer,trainer_id,int(horse_weight),int(weight_change),
                                odds_win,min_odds_place,max_odds_place,odds_rank,win_time
                                ]
                add_array=header_data+maindate_array
                total_array.append(add_array)
                maindata_count=maindata_count+1
                continue
            
            elif re_match_2:
                maindata_count=maindata_count+1
                continue


    print("要素の分離と配列の格納完了")
    #chromeを閉じる
    driver.quit()
    print("情報取得完了!!")
    return total_array,race_id

def export_csv(total_array,race_id):
    ymd=get_day_and_config.ymd
    print("csvに出力開始")
    path_1="/home/aweqse/dev/working/keiba/output/"+ymd+"/"+str(race_id)+ "_racedate.csv"
    df_2=pd.DataFrame(total_array)
    df_2.to_csv(path_1, index=False, header=False, encoding='utf-8-sig')
    print("csvに出力完了")

if __name__ == "__main__":
    # テスト用のダミーデータ
    load_url = "https://race.netkeiba.com/race/shutuba.html?race_id=202505021011"
    odds_win = 3.4
    min_odds_place = 1.8
    max_odds_place = 2.6
    odds_rank = 2
    win_time = 10  # オッズ取得時刻（例：発走10分前）

    main(load_url,odds_win,min_odds_place,max_odds_place,odds_rank,win_time)