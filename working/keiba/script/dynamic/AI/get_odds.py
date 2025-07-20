from datetime import datetime
from selenium import webdriver
import pandas as pd
from time import sleep
import re
from selenium.webdriver.support.ui import Select
import subprocess
import get_day_and_config
import get_racedata
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

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
    win_array,umaren_array,wide_1array,sanrenpuku_array,before_30min,before_10min,before_5min,racedata_dict,race_id=read_csv()
    get_odds(win_array,umaren_array,wide_1array,sanrenpuku_array,before_30min,before_10min,before_5min,racedata_dict,race_id)


def read_csv():
    print("urlの格納開始")
    ymd=get_day_and_config.ymd
    #csvファイルを読み取りレースIDを抽出しURLを生成する
    path_1="/home/aweqse/dev/working/keiba/output/"+str(ymd)+"/"+str(ymd)+"_racetime.csv"
    
    #テスト用
    #path_1="/home/aweqse/dev/working/keiba/output/20250715/20250715_racetime.csv" 

    df = pd.read_csv(path_1,index_col=False)
    #csvファイルから情報を読み取る
    race_id=df["レースID"]
    before_30min=df["発送時刻30分前"]
    before_10min=df["発送時刻10分前"]
    before_5min=df["発送時刻5分前"]

    #カラム名を配列に格納して時刻とオッズURLを辞書型にする
    win_url="https://race.netkeiba.com/odds/index.html?race_id="
    umaren_url_1="https://race.netkeiba.com/odds/index.html?type=b4&race_id="
    wide_url_1="https://race.netkeiba.com/odds/index.html?type=b5&race_id="
    sanrenpuku_url_1="https://race.netkeiba.com/odds/index.html?type=b7&race_id="
    race_date_url="https://race.netkeiba.com/race/shutuba.html?race_id="
    url_2="&housiki=c99"

    #urlの生成
    win_url_araay=[win_url+ str(s) for s in race_id]
    umaren_url_array=[umaren_url_1 + str(s) + url_2 for s in race_id]
    wide_url_1array=[wide_url_1 + str(s) + url_2 for s in race_id]
    sanrenpuku_url_1_array=[sanrenpuku_url_1 + str(s) + url_2 for s in race_id]
    racedate_url_array=[race_date_url+ str(s) for s in race_id]
    print("urlの格納完了")

    print("辞書の作成開始")
    umaren_array={}
    win_array={}
    sanrenpuku_array={}

    #キーが同じ値だと上書きされるため時間とURLは別々で生成する
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
    racedata_dict=dict(zip(before_5min, racedate_url_array))

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
    print("辞書の作成完了")
    return win_array,umaren_array,wide_1array,sanrenpuku_array,before_30min,before_10min,before_5min,racedata_dict,race_id

def get_odds(win_array,umaren_array,wide_1array,sanrenpuku_array,before_30min,before_10min,before_5min,racedata_dict,race_id):
    ymd=get_day_and_config.ymd
    
    #初期値
    hour_min=get_day_and_config.hour_min

#     #テスト用パラメーター
#     hour_min_array=[
#                     580,600,605,
#                     615,635,640,
#                     645,665,670,
#                     675,695,700,
#                     725,745,750,
#                     755,775,780,
#                     785,805,810,
#                     815,835,840,
#                     845,865,870,
#                     880,900,905,
#                     915,935,940,
#                     960,980,985,
#                     571,591,596,
#                     605,625,630,
#                     635,655,660,
#                     665,685,690,
#                     715,735,740,
#                     745,765,770,
#                     775,795,800,
#                     805,825,830,
#                     835,855,860,
#                     871,891,896,
#                     905,925,930,
#                     945,965,970,
#                     560,580,585,
#                     595,615,620,
#                     625,645,650,
#                     655,675,680,
#                     705,725,730,
#                     735,755,760,
#                     765,785,790,
#                     795,815,820,
#                     825,845,850,
#                     860,880,885,
#                     895,915,920,
#                     935,955,960

# ]
#     hour_min_array.sort()
#     hour_min_array_count=0
#     hour_min=hour_min_array[hour_min_array_count]
#     #ここまでテスト用

    #いつの時間の情報なのか判断するために配列の中身を乗り出して判定する
    before_30min_array=before_30min.tolist()
    before_10min_array=before_10min.tolist()
    before_5min_array=before_5min.tolist()

    #配列の中身をソートする
    before_30min_array.sort()
    before_10min_array.sort()
    before_5min_array.sort()
    race_id=race_id.tolist()

    # #テスト用パラメーター
    # hour_min=559
    
    while len(before_30min_array)!=0 and len(before_10min_array)!=0 and len(before_5min_array)!=0:
        #本番は以下のコメントアウトを外す
        # hour_min=get_day_and_config.hour_min

        #初期値
        check_odds_30=before_30min_array[0]
        check_odds_10=before_10min_array[0]
        check_odds_5=before_5min_array[0]


        if len(before_30min_array)!=0:
            check_odds_30=before_30min_array[0]
        if len(before_10min_array)!=0:
            check_odds_10=before_10min_array[0]
        if len(before_5min_array)!=0:
            check_odds_5=before_5min_array[0]

        while (check_odds_30<=hour_min) or (check_odds_10<=hour_min) or (check_odds_5<=hour_min):
            before_30min_flg=before_10min_flg=before_5min_flg=0

            #5分前を最優先で取得する
            if (check_odds_5<=hour_min):
                before_5min_flg=1  
            elif (check_odds_10<=hour_min):
                before_10min_flg=1
            elif (check_odds_30<=hour_min):
                before_30min_flg=1

            #urlの読み込み
            load_url_win=win_array[hour_min]
            load_url_umaren=umaren_array[hour_min]
            load_url_wide=wide_1array[hour_min]
            load_url_sanrenpuku=sanrenpuku_array[hour_min]
            
            #race_idを取り出す
            str_race_id=load_url_win[-12:]

            # #参考
            # xpath_win=         "/html/body/div[1]/div[3]/div[2]/div[1]/div[1]/div[1]/table"    
            # xpath_umaren=      "/html/body/div[1]/div[3]/div[2]/div[1]/div[3]/table/tbody"
            # xpath_wide=        "/html/body/div[1]/div[3]/div[2]/div[1]/div[3]/table/tbody"     
            # xpath_sanrenpuku=  "/html/body/div[1]/div[3]/div[2]/div[1]/div[3]/table/tbody"
            
            elem_1_array=[]
            elem_2_array=[]
            elem_3_array=[]
            elem_4_array=[]

            xpath_prudown=     "Axis_Horse_selectbox"
            class_path_win_place="RaceOdds_HorseList_Table"#他候補　"Ninki" RaceOdds_HorseList Tanfuku
            class_path_umaren= "Odds_Type_b4" #他候補"RaceOdds_HorseList_Table" "Ninki"
            class_path_wide="Odds_Type_b5" #他候補"RaceOdds_HorseList_Table" "Ninki" 
            class_path_sanrenpuku="Odds_Type_b7" #他候補　"RaceOdds_HorseList_Table" "Ninki" 
                    
            before_30min_win_path="/home/aweqse/dev/working/keiba/output/"+ymd+"/before_30min/"+str(str_race_id)+ "_win_place_odds.csv"
            before_30min_umaren_path="/home/aweqse/dev/working/keiba/output/"+ymd+"/before_30min/"+str(str_race_id)+ "_umaren_odds.csv"
            before_30min_wide_path="/home/aweqse/dev/working/keiba/output/"+ymd+"/before_30min/"+str(str_race_id)+ "_wide_odds.csv"
            before_30min_sanrenpuku_path="/home/aweqse/dev/working/keiba/output/"+ymd+"/before_30min/"+str(str_race_id)+ "_sanrenpuku_odds.csv"
            before_10min_win_path="/home/aweqse/dev/working/keiba/output/"+ymd+"/before_10min/"+str(str_race_id)+ "_win_place_odds.csv"
            before_10min_umaren_path="/home/aweqse/dev/working/keiba/output/"+ymd+"/before_10min/"+str(str_race_id)+ "_umaren_odds.csv"
            before_10min_wide_path="/home/aweqse/dev/working/keiba/output/"+ymd+"/before_10min/"+str(str_race_id)+ "_wide_odds.csv"
            before_10min_sanrenpuku_path="/home/aweqse/dev/working/keiba/output/"+ymd+"/before_10min/"+str(str_race_id)+ "_sanrenpuku_odds.csv"
            before_5min_win_path="/home/aweqse/dev/working/keiba/output/"+ymd+"/before_05min/"+str(str_race_id)+ "_win_place_odds.csv"
            before_5min_umaren_path="/home/aweqse/dev/working/keiba/output/"+ymd+"/before_05min/"+str(str_race_id)+ "_umaren_odds.csv"
            before_5min_wide_path="/home/aweqse/dev/working/keiba/output/"+ymd+"/before_05min/"+str(str_race_id)+ "_wide_odds.csv"
            before_5min_sanrenpuku_path="/home/aweqse/dev/working/keiba/output/"+ymd+"/before_05min/"+str(str_race_id)+ "_sanrenpuku_odds.csv"
            marge_csv="/home/aweqse/dev/working/keiba/output/"+ymd+"/"+str(str_race_id)+ "_after_marge.csv"
            racedata_csv="/home/aweqse/dev/working/keiba/output/"+ymd+"/racedata/"+str(str_race_id)+ "_racedate.csv"
            
            print("処理を開始します。")

            #単勝・複勝のオッズを取得する
            print("単勝・複勝の情報取得開始")
            driver.get(load_url_win)
            page_state=driver.execute_script("return document.readyState")
            sleep(5)
            if page_state=="complete":
                print("url読み込み完了")
                #xpathが完全に読み込まれるまで待機する
                WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH,f"//*[contains(@class, '{class_path_win_place}')]")))
            else:
                while True:
                    print("URLの読み込みに失敗したため再読み込みします。")
                    driver.get(load_url_win)
                    sleep(10)
                    WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,f"//*[contains(@class, '{class_path_win_place}')]")))
                    page_state=driver.execute_script("return document.readyState")
                    if page_state=="complete":
                        break
                    else:
                        continue
            
            #要素を変数に格納する
            elements_win = driver.find_elements(By.CLASS_NAME, class_path_win_place)
            
            #単勝の取得時刻を取得する
            win_time=get_day_and_config.hour_min
            print("単勝・複勝の情報取得完了")
            
            #単勝,複勝の情報を加工する
            print("単勝の処理開始")
            for elem_1 in elements_win:
                win_ele=elem_1.text.replace("\n","")
                elem_1_array.append(win_ele)
            win_ele="".join(elem_1_array)
            
            #配列の加工
            split_match=r"(\d+)\s(\d+)\s(\d+)([^\d\s]+)\s(\d+\.\d)\s(\d+\.\d)\s*-\s*(\d+\.\d)"
            win_ele=re.findall(split_match,win_ele)
            win_count=0

            #変数の初期化
            marge_cach=[]
            win_export_array=[]
            cache_1_array=[]
            header_flg=0
            while len(win_ele)>win_count:
                check_1=win_ele[win_count]
                odds_rank=check_1[0]
                umaban=check_1[2]
                odds_win=check_1[4]
                min_odds_place=check_1[5]
                max_odds_place=check_1[6]
                
                #レースIDを取得する
                win_match=r"(\d+)$"
                match=re.search(win_match,load_url_win)
                add_race_id=match.group(1)
                                
                #配列に格納する
                header_1=["レースID","30分前","10分前","5分前","馬番","単勝オッズ","最小複勝オッズ","最大複勝オッズ","人気","取得時間"]
                cache_1_array=[int(add_race_id),before_30min_flg,before_10min_flg,before_5min_flg,int(umaban),float(odds_win),float(min_odds_place),float(max_odds_place),int(odds_rank),win_time]
                marge_array=[umaban,odds_win,min_odds_place,max_odds_place,odds_rank]
                marge_cach.append(marge_array)
                if header_flg==0:
                    win_export_array.append(header_1)
                    header_flg=1
                win_export_array.append(cache_1_array)
                win_count=win_count+1

            #racedate5分前の場合,racedataを作成する
            if before_5min_flg==1:
                if os.path.exists(racedata_csv):
                    pass
                else:
                    load_url=racedata_dict[hour_min]
                    print("レースの基礎情報を取得します・")
                    get_racedata.main(load_url,marge_cach)

            #csvに出力する
            if before_30min_flg==1:
                csv_path_1=before_30min_win_path
            elif before_10min_flg==1:
                csv_path_1=before_10min_win_path
            elif before_5min_flg==1:
                csv_path_1=before_5min_win_path
 
            df_2=pd.DataFrame(win_export_array)
            df_2.to_csv(csv_path_1, index=False, header=False, encoding='utf-8-sig')           
            print("単勝と複勝の処理完了")


                
            


            #馬連の要素を取得する
            print("馬連の情報取得開始")
            driver.get(load_url_umaren)
            page_state=driver.execute_script("return document.readyState")
            sleep(5)
            if page_state=="complete":
                print("url読み込み完了")
                #xpathが完全に読み込まれるまで待機する
                WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH,f"//*[contains(@class, '{class_path_umaren}')]")))
            else:
                while True:
                    print("URLの読み込みに失敗したため再読み込みします。")
                    driver.get(load_url_win)
                    sleep(10)
                    WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,f"//*[contains(@class, '{class_path_umaren}')]")))
                    page_state=driver.execute_script("return document.readyState")
                    if page_state=="complete":
                        break
                    else:
                        continue
            
            
            #要素を変数に格納する
            elements_umaren = driver.find_elements(By.XPATH,f"//*[contains(@class, '{class_path_umaren}')]")
            
            #馬連の取得時効を取得する
            now = datetime.now()
            hour = now.hour
            minute = now.minute
            umaren_time=hour*60+minute 
            print("馬連の情報取得終了")

            #馬連の情報を加工する
            print("馬連の処理開始")
            for elem_2 in elements_umaren:
                umaren_ele=elem_2.text.replace("\n"," ")
                elem_2_array.append(umaren_ele)
            umaren_ele="".join(elem_2_array)

            #配列の加工
            umaren_match=r"(\d+)\s(\d+)\s(\d+)\s(\d+\.\d)\s\d+\s[^\s]+\s\d+\s[^\s]+"
            umaren_ele=re.findall(umaren_match,umaren_ele)

            #30番以降の配列を削除する
            umaren_ele=umaren_ele[:30]

            #配列から要素を変数に格納する
            type_wide=type_sanrenpuku=type_umaren=0
            type_umaren=1
            cache_2_array=[]
            umaren_export_array=[]
            header_flg=0
            umaren_count=0
            header_2=["レースID","ワイド","馬連","三連複","馬番1","馬番2","馬番3","30分前","10分前","5分前","オッズ","最低オッズ","最大オッズ","人気","取得時刻"]
            while len(umaren_ele)>umaren_count:
                check_2=umaren_ele[umaren_count]
                umaren_odds_rank=check_2[0]
                umaban_1=check_2[1]
                umaban_2=check_2[2]
                umaban_3=-1
                umarenn_odds=check_2[3]
                min_odds=-1
                max_odds=-1

                #レースidを取り出す
                race_id_umaren_match=r"(\d{12})"
                match=re.search(race_id_umaren_match,load_url_umaren)
                race_id_umaren=match.group(1)

                #取得した時刻を判定する                
                cache_2_array=[int(race_id_umaren),type_wide,type_umaren,type_sanrenpuku,int(umaban_1),int(umaban_2),int(umaban_3),before_30min_flg,before_10min_flg,before_5min_flg,float(umarenn_odds),float(min_odds),float(max_odds),int(umaren_odds_rank),umaren_time]
                
                if header_flg==0:
                    umaren_export_array.append(header_2)
                    header_flg=1
                umaren_export_array.append(cache_2_array)
                umaren_count=umaren_count+1
            
            #csvに出力する
            if before_30min_flg==1:
                csv_path_1=before_30min_umaren_path
            elif before_10min_flg==1:
                csv_path_1=before_10min_umaren_path
            elif before_5min_flg==1:
                csv_path_1=before_5min_umaren_path
            df_3=pd.DataFrame(umaren_export_array)
            df_3.to_csv(csv_path_1, index=False, header=False, encoding='utf-8-sig') 
            print("馬連の処理終了")






            #ワイドの要素を取得する
            print("ワイドの情報取得開始")
            driver.get(load_url_wide)
            page_state=driver.execute_script("return document.readyState")
            sleep(5)
            if page_state=="complete":
                print("url読み込み完了")
                #xpathが完全に読み込まれるまで待機する
                WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH,f"//*[contains(@class, '{class_path_wide}')]")))
            else:
                while True:
                    print("URLの読み込みに失敗したため再読み込みします。")
                    driver.get(load_url_win)
                    sleep(10)
                    WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,f"//*[contains(@class, '{class_path_wide}')]")))
                    page_state=driver.execute_script("return document.readyState")
                    if page_state=="complete":
                        break
                    else:
                        continue
            
            #要素を変数に格納する
            elements_wide = driver.find_elements(By.XPATH,f"//*[contains(@class, '{class_path_wide}')]")

            #現在の時刻を取得する
            now = datetime.now()
            hour = now.hour
            minute = now.minute
            wide_time=hour*60+minute
            print("ワイドの情報取得完了") 

            #配列を整形する
            print("ワイドの処理開始")
            for elem_3 in elements_wide:
                wide_ele=elem_3.text.replace("\n"," ")
                elem_3_array.append(wide_ele)
            win_ele="".join(elem_3_array)

            #配列の加工
            wide_match = wide_match = r"(\d+)\s+(\d+)\s+(\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+\d+\s+[^\s]+\s+\d+\s+[^\s]+"
            wide_ele=re.findall(wide_match,wide_ele)

            #30番以降の配列を削除する
            wide_ele=wide_ele[:30]

            #配列から要素を変数に格納する
            type_umaren=type_wide=type_sanrenpuku=0
            type_wide=1
            cache_3_array=[]
            wide_export_array=[]
            header_flg=0
            wide_count=0
            while len(wide_ele)>wide_count:
                check_3=wide_ele[wide_count]
                wide_odds_rank=check_3[0]
                umaban_1=check_3[1]
                umaban_2=check_3[2]
                umaban_3=-1
                wide_odds=-1
                min_odds=check_3[3]
                max_odds=check_3[4]
                
                #レースidを取り出す
                wide_match=r"(\d{12})"
                match=re.search(wide_match,load_url_wide)
                race_id_wide=match.group(1)

                cache_3_array=[int(race_id_wide),type_wide,type_umaren,type_sanrenpuku,int(umaban_1),int(umaban_2),umaban_3,before_30min_flg,before_10min_flg,before_5min_flg,wide_odds,float(min_odds),float(max_odds),int(wide_odds_rank),wide_time]
                
                if header_flg==0:
                    wide_export_array.append(header_2)
                    header_flg=1
                wide_export_array.append(cache_3_array)
                wide_count=wide_count+1

            #csvに出力する
            if before_30min_flg==1:
                csv_path_1=before_30min_wide_path
            elif before_10min_flg==1:
                csv_path_1=before_10min_wide_path
            elif before_5min_flg==1:
                csv_path_1=before_5min_wide_path
            df_3=pd.DataFrame(wide_export_array)
            df_3.to_csv(csv_path_1, index=False, header=False, encoding='utf-8-sig') 
            print("ワイドの処理終了")



            print("三連複の情報取得開始")
            driver.get(load_url_sanrenpuku)
            page_state=driver.execute_script("return document.readyState")
            sleep(5)
            if page_state=="complete":
                print("url読み込み完了")
                #xpathが完全に読み込まれるまで待機する
                WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH,f"//*[contains(@class, '{class_path_sanrenpuku}')]")))
            else:
                while True:
                    print("URLの読み込みに失敗したため再読み込みします。")
                    driver.get(load_url_win)
                    sleep(10)
                    WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,f"//*[contains(@class, '{class_path_sanrenpuku}')]")))
                    page_state=driver.execute_script("return document.readyState")
                    if page_state=="complete":
                        break
                    else:
                        continue
            
            #要素を変数に格納する
            elements_sanrenpuku_1 = driver.find_elements(By.XPATH,f"//*[contains(@class, '{class_path_sanrenpuku}')]")

            #現在の時刻を取得する
            now = datetime.now()
            hour = now.hour
            minute = now.minute
            sanrenpuku_time=hour*60+minute 
            print("三連複の情報取得終了")    
            
            #三連複の要素を取得する
            print("三連複の処理開始")
            #配列を整形する(1~100)
            for elem_4 in elements_sanrenpuku_1:
                sanrenpuku_ele_1=elem_4.text.replace("\n"," ")
                elem_4_array.append(sanrenpuku_ele_1)

            #配列の加工
            sanrenpuku_match = sanrenpuku_match = r"(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+\.\d+)"
            sanrenpuku_ele_1=re.findall(sanrenpuku_match,sanrenpuku_ele_1)    

            #プルダウンを操作して101~200を取得する
            select_elem = driver.find_element(By.XPATH, f'//select[contains(@class, {xpath_prudown})]')  # IDは変更の可能性あり
            select = Select(select_elem)
            select.select_by_index(2)
            sleep(5)
            elements_sanrenpuku_2 = driver.find_elements(By.XPATH,f"//*[contains(@class, '{class_path_sanrenpuku}')]")

            #配列を整形する(101~200)
            for elem_5 in elements_sanrenpuku_2:
                sanrenpuku_ele_2=elem_5.text.replace("\n"," ")
                elem_4_array.append(sanrenpuku_ele_2)
            sanrenpuku_ele_2="".join(elem_4_array)

            #配列を加工する
            sanrenpuku_match = sanrenpuku_match = r"(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+\.\d+)"
            sanrenpuku_ele_2=re.findall(sanrenpuku_match,sanrenpuku_ele_2)

            #150まで取得する
            sanrenpuku_ele_2=sanrenpuku_ele_2[:50]         

            #同一の処理をするため配列を統合する
            sanrenpuku_ele_array=sanrenpuku_ele_1+sanrenpuku_ele_2

            #配列から要素を変数に格納する
            type_umaren=type_wide=0
            type_sanrenpuku=1
            cache_4_array=[]
            sanrenpuku_export_array=[]
            header_flg=0
            sanrenpuku_count=0

            while len(sanrenpuku_ele_array)>sanrenpuku_count:
                check_4=sanrenpuku_ele_array[sanrenpuku_count]
                sanrenpuku_odds_rank=check_4[0]
                umaban_1=check_4[1]
                umaban_2=check_4[2]
                umaban_3=check_4[3]
                sanrenpuku_odds=check_4[4]
                min_odds=-1
                max_odds=-1
            
                #レースidを取り出す
                sanrenpuku_match=r"(\d{12})"
                match=re.search(sanrenpuku_match,load_url_sanrenpuku)
                race_id_sanrenpuku=match.group(1)

                cache_4_array=[int(race_id_sanrenpuku),type_wide,type_umaren,type_sanrenpuku,int(umaban_1),int(umaban_2),umaban_3,before_30min_flg,before_10min_flg,before_5min_flg,sanrenpuku_odds,float(min_odds),float(max_odds),int(sanrenpuku_odds_rank),sanrenpuku_time]
                
                if header_flg==0:
                    sanrenpuku_export_array.append(header_2)
                    header_flg=1
                sanrenpuku_export_array.append(cache_4_array)
                sanrenpuku_count=sanrenpuku_count+1

            #csvに出力する
            if before_30min_flg==1:
                csv_path_1=before_30min_sanrenpuku_path
            elif before_10min_flg==1:
                csv_path_1=before_10min_sanrenpuku_path
            elif before_5min_flg==1:
                csv_path_1=before_5min_sanrenpuku_path
            df_4=pd.DataFrame(sanrenpuku_export_array)
            df_4.to_csv(csv_path_1, index=False, header=False, encoding='utf-8-sig') 
            print("三連複の処理終了")

            #時刻(分)を進めないと二重処理になるため1分待機する
            print("取得が完了したので待機します")

            #本番は以下のコメントアウトを外す
            sleep(60)

            #取得した配列を削除する
            if before_5min_flg==1 and len(before_5min_array)!=0:
                del before_5min_array[0]
            elif before_10min_flg==1 and len(before_10min_array)!=0:
                del before_10min_array[0]     
            elif before_30min_flg==1 and len(before_30min_array)!=0:
                del before_30min_array[0]  

            if len(before_30min_array)!=0:
                check_odds_30=before_30min_array[0]
            if len(before_10min_array)!=0:
                check_odds_10=before_10min_array[0]
            if len(before_5min_array)!=0:
                check_odds_5=before_5min_array[0]
            
            #テスト用
            # hour_min_array_count=hour_min_array_count+1
            # if len(before_30min_array)!=0 and len(before_10min_array)!=0 and len(before_5min_array)!=0:
            #     pass
            # else:
            #     hour_min=hour_min_array[hour_min_array_count]
            #ここまでテスト用

            # #テスト用パラメーター
            # hour_min=hour_min+1

        print("該当時刻ではないので待機します。現在の時刻は"+str(hour_min)+"です。" )
        sleep(20)

        #本番は以下のコメントアウトを外す
        hour_min=get_day_and_config.hour_min
        
        # #テスト用パラメーター
        # hour_min=hour_min+1
        continue 

    print("競馬の終了時刻となったので待機を終了します")

main()

