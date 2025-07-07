from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
import mysql.connector
import hashlib
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument('--disable-gpu')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')
options.add_argument('--disable-web-security')
options.add_argument('--blink-settings=imagesEnabled=false')
options.add_argument('--ignore-certificate-errors')
driver = webdriver.Chrome(options=options)

#データベースに接続する
conn = mysql.connector.connect(
    host='localhost',
    port='3306',
    user='connect',
    password='Fujieda1217', 
    database='keiba'
)
cursor = conn.cursor()

#各種変数を初期化する
index_list=0
race_number_list=[]
race_url_list=[]
race_cache=0
access_index=0
all_race_df=[]
insert_list=[]

#手動　以下に日付を入力する(一桁の場合は０を入れて文字列として入力する)
ymd_year="2025"
ymd_month="05"
ymd_day="31"

#自動 月日のリストを手動で作成する
ymd_list_index=0
ymd_md_list=[""]
while len(ymd_md_list)>ymd_list_index:

    #手動　1日ごとのテスト
    driver.get("https://race.netkeiba.com/top/race_list.html?kaisai_date="+ymd_year+ymd_month+ymd_day)

    #自動
    #ymd_md=ymd_md_list[ymd_list_index]
    #driver.get("https://race.netkeiba.com/top/race_list.html?kaisai_date="+ymd_year+ymd_md)

    #パラメーターを初期化をする
    race_url_list=[]
    access_index=0

   #読み込み待ちの処理
    wait=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/div/div[1]/div/div[2]/div/div[1]//a[@href]")))

    #一日単位のレースのURLを取得する
    sleep(1)
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
    print("URL取得完了")

    race_cache=len(race_url_list)
    while race_cache>access_index:#ここは一括で取得したURLを条件とする　
        driver.get(race_url_list[access_index])
        sleep(5)
        #1レースごとのテスト
        #driver.get("https://race.netkeiba.com/race/result.html?race_id=202406020304")

        #読み込み待ちの処理
        wait=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/div[2]/div/div[1]/div[3]/div[1]/span")))
        
        #レースの基本情報を取得する
        hantei_2=driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div/div[1]/div[3]/div[2]")
        hantei_4=driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div/div[1]/div[3]/div[1]/span")
        hantei_2=hantei_2.text.split()
        hantei_4=hantei_4.text

        #配列修正　不要な情報を削除する
        del_index=0
        while del_index<len(hantei_2):    
            if ("発走" in hantei_2[del_index])==True or ("/" in hantei_2[del_index])==True or ("天候" in hantei_2[del_index])==True or ("本賞金" in hantei_2[del_index])==True:
                del hantei_2[del_index]
                continue
            del_index=del_index+1

        #配列修正　取りやめの場合挿入する
        if ("取り止め" in hantei_2[0])==True:
            hantei_2.insert(4,"0回")
        
        #配列修正　障害戦でダートと芝両方の馬場状態が取得されるので削除する
        check_1=hantei_2[2]
        check_2=hantei_2[3]
        if ("芝" in check_1) or ("ダート" in check_1)==True: 
            if ("芝" in check_2) or ("ダート" in check_2)==True:
                del hantei_2[3]
                del hantei_2[4]    

        #配列修正　アルファベット（右・Bなど）が含まれている場合削除する
        check_8=hantei_2[3]
        check_9=hantei_2[4]
        if ("A" in check_8) or ("B" in check_8) or ("C" in check_8) or ("D" in check_8)==True:
            del hantei_2[3]
        if ("A" in check_9) or ("B" in check_9) or ("C" in check_9) or ("D" in check_9)==True:
            del hantei_2[4]
            
        #配列修正　余分な要素を削除する
        if ("牝" in hantei_2[9])==False:
            if (")" in hantei_2[9])==True or ("]" in hantei_2[9])==True or ("見習"in hantei_2[9])==True:
                del hantei_2[9]
        if ("牝" in hantei_2[10])==False:
        #配列修正　余分な要素を削除する
            if (")" in hantei_2[10])==True or ("]" in hantei_2[10])==True or ("見習"in hantei_2[10])==True:
                del hantei_2[10]

        #外回りの判定をする
        #hinba_indexはレース名に”外”がつくものを除外するため1から始める
        out_flag=0
        out_index=1
        while out_index<len(hantei_2):    
            if ("外" in hantei_2[out_index])==True:
                del hantei_2[out_index]
                out_flag=1
                break
            out_index=out_index+1
        
        #長距離の場合の（内2週）を削除する
        if ("2周" in hantei_2[3])==True:
            del hantei_2[3]

        #牝馬限定戦の判定をする
        #hinba_indexはレース名に”牝”がつくものを除外するため1から始める
        hinba_flag=0
        hinba_index=1
        while hinba_index<len(hantei_2):    
            if ("牝" in hantei_2[hinba_index])==True:
                del hantei_2[hinba_index]
                hinba_flag=1
                break
            hinba_index=hinba_index+1
        
        #九州産馬限定戦の場合削除する
        if hantei_2[9]=="九州産馬":
            del hantei_2[9]
            
        race_name=hantei_2[0]
        number_of_race=hantei_4.replace("R","")
        course=hantei_2[1]
        baba=hantei_2[3][-1]
        kaisaijou=hantei_2[5]
        conditions_age=hantei_2[7]

        #同じコースで内・外の区別がある場合に判定する
        if kaisaijou=="京都" and (course=="芝1400m" or course=="芝1600m"):
            if out_flag==1:
                out_in="外"
                course=course+"外"
            elif out_flag==0:
                out_in="内"
                course=course+"内"
        elif kaisaijou=="新潟" and course=="芝2000m":
            if out_flag==1:
                out_in="外"
                course=course+"外"
            elif out_flag==0:
                out_in="内"
                course=course+"内"
        else:
            out_in="NaN"

        #レース名を現代に合わせる
        race_rank=hantei_2[8]
        if ("新馬" in race_rank)==True:
            race_rank="新馬"
        if ("未勝利" in race_rank)==True:
            race_rank="未勝利"
        if ("５００万下" in race_rank)==True:
            race_rank="1勝クラス"
        if ("１０００万下" in race_rank)==True:
            race_rank="2勝クラス"
        if ("１６００万下" in race_rank)==True:
            race_rank="3勝クラス"

        if hinba_flag==1:
            only_hinba="牝"
        else:
            only_hinba="NaN"

        conditions_weight=hantei_2[9]
        head_count=hantei_2[10].replace("頭", "")

        race_kai=hantei_2[4].replace("回", "")
        race_kaisuu=hantei_2[6].replace("日目", "")

        #変数のデータ型を変換する
        ymd_year=int(ymd_year)
        #手動
        ymd_month=int(ymd_month)
        ymd_day=int(ymd_day)

        #自動
        #ymd_month=int(ymd_md[0]+ymd_md[1])
        #ymd_day=int(ymd_md[2]+ymd_md[3])
        #race_kai=int(race_kai)
        #race_kaisuu=int(race_kaisuu)
        #head_count=int(head_count)
        #number_of_race=int(number_of_race)

        header=(ymd_year,ymd_month,ymd_day,race_kai,race_kaisuu,kaisaijou,number_of_race,course,out_in,head_count,baba,race_name,race_rank,conditions_age,only_hinba,conditions_weight)

        #差分インサートのためにkaisaijouを集合に格納する
        keibakosu=kaisaijou+course
        insert_list.append(keibakosu)

        #レースが取り止めの場合はここで処理する
        if ("取り止め" in race_name)==True:
            race_df=list(header)
            order_of_arrival=wakuban=umaban=horse_name=sex=old=race_weight=jockey=race_time=arrival=popular=odds=after_3_haong=corner_rank_1=corner_rank_2=corner_rank_3=corner_rank_4=stable_EW=stable=horse_weight=horse_weight_rise_and_fall="0"
            order_of_arrival=int(order_of_arrival)
            wakuban=int(wakuban)
            umaban=int(umaban)
            old=int(old)
            race_weight=float(race_weight)
            race_time=float(race_time)
            popular=int(popular)
            odds=float(odds)
            after_3_haong=float(after_3_haong)
            corner_rank_1=int(corner_rank_1)
            corner_rank_2=int(corner_rank_2)
            corner_rank_3=int(corner_rank_3)
            corner_rank_4=int(corner_rank_4)
            horse_weight=int(horse_weight)
            dat="取り止め"
            hs = hashlib.md5(dat.encode()).hexdigest()
            horse_weight_rise_and_fall=int(horse_weight_rise_and_fall)
            race_result=[order_of_arrival,wakuban,umaban,horse_name,sex,old,race_weight,jockey,race_time,arrival,popular,odds,after_3_haong,corner_rank_1,corner_rank_2,corner_rank_3,corner_rank_4,stable_EW,stable,horse_weight,horse_weight_rise_and_fall]
            rap_list=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,hs]
            race_df=list(header)
            race_df.extend(race_result)
            race_df.extend(rap_list)
            all_race_df.append(race_df)
            race_result.clear
            print("配列格納完了")
            header=()
            rap_list=()
            access_index=access_index+1
            continue
            
        #レース結果から情報を取得する
        hantei_1=driver.find_element(By.XPATH,"/html/body/div[1]/div[3]/div[2]/div[1]/table/tbody")
        hantei_1=hantei_1.text.split()
        loop_count=len(hantei_1)
        list_index=0

        #配列修正　最終行の馬体重がないときに挿入する
        #配列修正　最終行の馬体重がないときに挿入する
        if ("(" in hantei_1[-1])==False and (("美浦" in hantei_1[-1])==True or ("栗東" in hantei_1[-1])==True or ("美浦" in hantei_1[-1])==True) :
            insert_index=len(hantei_1)
            hantei_1.insert(insert_index,"000(0)")
            
        while loop_count>list_index:
            order_of_arrival=hantei_1[0+list_index]

            #再計算フラグを初期化する
            recalculation_flag=0
            reason=""
            
            #以下処理順を意識しなければ正しく処理できないので注意
            #配列修正　一着馬の挿入処理
            if list_index==0:
                hantei_1.insert(8,"NaN")
                recalculation_flag=1
            
            #配列修正　中止の挿入処理
            if order_of_arrival=="中止":
                recalculation_flag=1
                order_of_arrival=0
                hantei_1.insert(7+list_index,"0")
                hantei_1.insert(8+list_index,"中止")
                hantei_1.insert(11+list_index,"0")               

            #配列修正　取消・除外の挿入処理
            elif (order_of_arrival=="取消") or (order_of_arrival=="除外"):
                recalculation_flag=1
                reason=order_of_arrival
                order_of_arrival=0
                hantei_1.insert(7+list_index,"0")
                hantei_1.insert(8+list_index,reason)
                hantei_1.insert(9+list_index,0)
                hantei_1.insert(10+list_index,0)
                hantei_1.insert(11+list_index,"0")
                hantei_1.insert(12+list_index,"0")
                if reason=="取消" or ("美浦"in hantei_1[-1]==True or "栗東"in hantei_1[-1]==True or "海外"in hantei_1[-1]==True):
                    hantei_1.insert(14+list_index,"000(0)")
                    
            #"失格"の場合の挿入処理
            elif order_of_arrival=="失格":
                order_of_arrival=0
                hantei_1.insert(8+list_index,"NaN")
                recalculation_flag=1

            #配列修正　騎手の苗字と名前が分かれているときに処理する
            #hantei_1[7+list_index]の右の値がレースタイムでない場合、要素を削除する
            check_4=hantei_1[7+list_index][0]
            if check_4=="0" or check_4=="1" or check_4=="2" or check_4=="3" or check_4=="4" or check_4=="5" or hantei_1[7+list_index]==0:
                pass
            else:
                del hantei_1[7+list_index]
                recalculation_flag=1

            #上り３ハロンがない場合、0を挿入する。
            if len(hantei_1[12+list_index])>=2:
                check_3=hantei_1[12+list_index][0]+hantei_1[12+list_index][1]
            else:
                check_3="例外"

            if check_3=="美浦":
                hantei_1.insert(11+list_index,"0")
            elif check_3=="栗東":
                hantei_1.insert(11+list_index,"0")
            elif check_3=="海外":
                hantei_1.insert(11+list_index,"0")   

            #コーナー通貨順位がない場合の処理
            if ("-" in hantei_1[11+list_index])==True:
                hantei_1.insert(11+list_index,"0")

            #配列修正　調教師の苗字と名前が分かれているときに処理する
            #"除外","中止"の場合
            check_7=hantei_1[14+list_index][0]
            if  check_7=="3" or check_7=="4" or check_7=="5" or check_7=="6" or check_7=="0" or check_7=="9" or check_7=="除" or check_7=="中" or check_7=="取":
                pass
            else:
                del hantei_1[14+list_index]
                recalculation_flag=1

            #配列修正　最終行以外の馬体重がないときに挿入する
            check_list=hantei_1[list_index:15+list_index]
            if len(check_list[-1])<3:
                hantei_1.insert(14+list_index,"000(0)")

            if len(hantei_1[14+list_index])<3:
                hantei_1[14+list_index]=hantei_1[14+list_index]+"(0)"        
                    
            #取消の場合
            elif order_of_arrival==0  and reason=="取消" and len(hantei_1)>15+list_index: 
                check_6=hantei_1[15+list_index]
                if not(check_6=="中止" or check_6=="取消" or check_6=="除外"):
                    del hantei_1[15+list_index]
                    recalculation_flag=1

            #通常の場合
            elif reason=="":
                check_5=hantei_1[14+list_index][0]
                if check_5=="0" or check_5=="3" or check_5=="4" or check_5=="5" or check_5=="6":
                    pass
                else:
                    del hantei_1[14+list_index]
                    recalculation_flag=1

            #配列を追加・削除した後にloop_countを再計算する
            if recalculation_flag==1:
                loop_count=len(hantei_1)

            #配列から変数に値を格納する    
            wakuban=hantei_1[1+list_index]
            umaban=hantei_1[2+list_index]
            horse_name=hantei_1[3+list_index]
            sex=hantei_1[4+list_index][0]
            old=hantei_1[4+list_index][1]
            race_weight=hantei_1[5+list_index]
            jockey=hantei_1[6+list_index]
                
            #タイムをfloat型に変換する処理をする
            race_time=hantei_1[7+list_index]
            if race_time=="0":
                race_time=0
            if race_time!=0:
                m=int(race_time[0])
                if m>=1:
                    add=60*m
                    race_time=race_time[2:]
                    race_time=float(race_time)
                    race_time=race_time+add
                else:
                    race_time=race_time[2:]
                    race_time=float(race_time)

            arrival=hantei_1[8+list_index]
            popular=hantei_1[9+list_index]
            odds=hantei_1[10+list_index]
            after_3_haong=hantei_1[11+list_index]
            corner_=hantei_1[12+list_index]
            corner_=corner_.split("-")
            corner_rank_1=corner_rank_2=corner_rank_3=corner_rank_4=0
            if len(corner_)==1:
                corner_rank_4=corner_[0]
            elif len(corner_)==2:
                corner_rank_3=corner_[0]
                corner_rank_4=corner_[1]
            elif len(corner_)==3:
                corner_rank_2=corner_[0]
                corner_rank_3=corner_[1]
                corner_rank_4=corner_[2]
            elif len(corner_)==4:
                corner_rank_1=corner_[0]
                corner_rank_2=corner_[1]
                corner_rank_3=corner_[2]
                corner_rank_4=corner_[3]

            #中止の場合コーナー順位を削除する
            if ("-" in hantei_1[13+list_index])==True:
                del hantei_1[13+list_index]

            stable=hantei_1[13+list_index]
            stable_EW=stable[0]+stable[1]
            stable=stable.lstrip(stable[:2])

            horse_weight_about=hantei_1[14+list_index]
            horse_weight=horse_weight_about[0:3]
            horse_weight_rise_and_fall=horse_weight_about[3:].replace("(", "").replace(")", "")
            if horse_weight_rise_and_fall=="":
                horse_weight_rise_and_fall=0

            #変数をsqlのデータ型に合せて変換する
            order_of_arrival=int(order_of_arrival)
            wakuban=int(wakuban)
            umaban=int(umaban)
            old=int(old)
            race_weight=float(race_weight)
            race_time=float(race_time)
            popular=int(popular)
            odds=float(odds)
            after_3_haong=float(after_3_haong)
            corner_rank_1=int(corner_rank_1)
            corner_rank_2=int(corner_rank_2)
            corner_rank_3=int(corner_rank_3)
            corner_rank_4=int(corner_rank_4)
            horse_weight=int(horse_weight)
            horse_weight_rise_and_fall=int(horse_weight_rise_and_fall)

            #ラップタイムを取得する（障害戦のラップタイムはデータがないのですべてゼロ)
            rap_list=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            if ("障" in course)==False:
                hantei_3=driver.find_elements(By.XPATH,"/html/body/div[1]/div[3]/div[2]/div[2]/div[2]/div[2]/table/tbody/tr[3]")
                if len(hantei_3)==0:
                    break
                hantei_3=driver.find_element(By.XPATH,"/html/body/div[1]/div[3]/div[2]/div[2]/div[2]/div[2]/table/tbody/tr[3]")            
                hantei_3=hantei_3.text.split()
                loop_index=0
                rap_index=len(hantei_3)
                while rap_index>loop_index:
                    rap_list[loop_index]=hantei_3[loop_index]
                    loop_index=loop_index+1
            
            #rap_indexをfloat型に変換する
            rap_list=list(map(float,rap_list))

            #IDとしてハッシュ値を算出するために文字列に変換する
            ymd_year=str(ymd_year)
            ymd_month=str(ymd_month)
            ymd_day=str(ymd_day)
            odds=str(odds)
            race_time=str(race_time)
            if len(ymd_month)==1:
                hs_month="0"+ymd_month
            else:
                hs_month=ymd_month

            if len(ymd_day)==1:
                hs_day="0"+ymd_day
            else:
                hs_day=ymd_day
            
            dat=ymd_year+hs_month+hs_day+horse_name+odds+race_time
            hs = hashlib.md5(dat.encode()).hexdigest()
            
            #文字列から元に戻す
            odds=float(odds)
            race_time=float(race_time)

            #取得した情報をリスト化しヘッダーと統合する
            race_result=[order_of_arrival,wakuban,umaban,horse_name,sex,old,race_weight,jockey,race_time,arrival,popular,odds,after_3_haong,corner_rank_1,corner_rank_2,corner_rank_3,corner_rank_4,stable_EW,stable,horse_weight,horse_weight_rise_and_fall]
            race_df=list(header)
            race_df.extend(race_result)
            race_df.extend(rap_list)
            race_df.append(hs)
            all_race_df.append(race_df)
            
            #各種変数の調整をする
            list_index=list_index+15
            race_result.clear
            print("配列格納完了")

        header=()
        rap_list=()
        access_index=access_index+1
        continue

    sql_index=0
    sql_list=[]
    sql_after=""
    sql_before="INSERT INTO all_race VALUES"
    end_index=len(all_race_df)-1
    while end_index>=sql_index:
        if end_index>sql_index:
            end_str="),"
        elif end_index==sql_index: 
            end_str=")"
        sql_cache=all_race_df[sql_index]
        sql_str="("+str(sql_cache).replace("[","").replace("]","")+end_str
        sql_after=sql_after+sql_str
        sql_index=sql_index+1
    sql=sql_before+sql_after
    cursor.execute(sql)
    conn.commit() # コミットしてトランザクション実行
    print("sqlコミット完了")

    sleep(1)

    sql=""
    all_race_df=[]
    ymd_list_index=ymd_list_index+1


print("リスト内の処理すべて終了")