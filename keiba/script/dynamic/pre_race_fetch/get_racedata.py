from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd

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
    ymd=get_datetime()
    url_array=read_csv(ymd)
    header_array=get_header_data(url_array)
    export_csv(header_array)

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

    return ymd

def read_csv(ymd):
    #csvファイルを読み取りレースIDを抽出しURLを生成する
    path_1="/home/aweqse/working/keiba/output/pre_odds_csv/"+ymd+"_racetime.csv"
    path_1="/home/aweqse/working/keiba/output/pre_odds_csv/20250705_racetime.csv" #テスト用
    df = pd.read_csv(path_1,index_col=False)
    race_id=df["レースID"]
    url_count=0
    url_array=[]
    while len(race_id)>url_count:
        tmp_1=race_id[url_count]
        url="https://race.netkeiba.com/race/shutuba.html?race_id="+str(tmp_1)
        url_array.append(url)
        url_count=url_count+1

    return url_array

def  get_header_data(url_array):
    load_count=0
    header_array=[]
    header_flag=0
    while len(url_array)>load_count:
        print("ヘッダーの情報格納開始")
        load_url=url_array[load_count]

        #テスト用URL
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
        print(load_url)
        xpath_1="/html/body/div[1]/div[2]/div/div[1]/div[3]/div[2]"
        xpath_2="/html/body/div[1]/div[2]/div/div[1]/div[3]/div[2]/h1/span"
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

        #headerを取得
        elements_1 = driver.find_elements(By.XPATH, xpath_1)
        for elem_1 in elements_1:
            hearder=elem_1.text.split()        

        #G1,G2等をアイコンのクラスから判別するため取り出す
        elements_2 = driver.find_elements(By.XPATH, xpath_2)
        for elem_2 in elements_2:
            class_str = elem_2.get_attribute("class")          

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
            
            #要素を変数に格納する処理
            if check_1=="/":
                del hearder[0]
                continue    

            if (("芝" in check_1) or ("ダ" in check_1) or ("障" in check_1)) and ("m" in check_1):
                if ("芝" in check_1):
                    course_turf=1
                    distance=check_1.replace("芝","").replace("m","")
                    del hearder[0]
                    continue                           
                elif ("ダ" in check_1):
                    course_dirt=1
                    distance=check_1.replace("ダ","").replace("m","")
                    del hearder[0]
                    continue   
                elif ("障" in check_1):
                    course_jump=1
                    distance=check_1.replace("障","").replace("m","")
                    del hearder[0]
                    continue
                else:
                    course_other=1
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

            if ("サラ系" in check_1):
                if check_1=="サラ系３歳":
                    old_3age=1
                    del hearder[0]
                    continue 
                elif check_1=="サラ系２歳":
                    old_2age=1
                    del hearder[0]
                    continue 
                elif check_1=="サラ系３歳以上":
                    old_3age_over=1
                    del hearder[0]
                    continue 
                elif check_1=="サラ系４歳以上":
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
            
            #URLからrace_idを読み取る
            race_id=int(load_url[-12:])
            
            del hearder[0]
            continue 
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
    return header_array

def export_csv(header_array):
    path_1="/home/aweqse/est.csv"
    df_2=pd.DataFrame(header_array)
    df_2.to_csv(path_1, index=False, header=False, encoding='utf-8-sig')




            


        









    
    



main()