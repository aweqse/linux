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
    url_array=read_csv()
    get_header_data(url_array)


def read_csv():
    #csvファイルを読み取りレースIDを抽出しURLを生成する
    path_1="/home/aweqse/working/keiba/output/pre_odds_csv/20250705_racetime.csv" #テスト用
    df = pd.read_csv(path_1,index_col=False)
    race_id=df["レースID"]
    print(race_id)
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
    while len(url_array)>load_count:
        load_url=url_array[load_count]
        #テスト用パラメーター
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
        load_url="https://race.netkeiba.com/race/result.html?race_id=202505010511"

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

        elements_1 = driver.find_elements(By.XPATH, xpath_1)
        elements_2 = driver.find_elements(By.XPATH, xpath_2)

        #headerを取得
        for elem_1 in elements_1:
            hearder=elem_1.text.split()

        header_colmes=["G1","G2","G3","L","OP","JG1","JG2","JG3","","","","","","","","","","",]

        while len(hearder)!=0:
            #変数の初期化
            racegrade_g1=racegrade_g2=racegrade_g3=racegrade_l=racegrade_op=racegrade_jg1=racegrade_jg2=racegrade_jg3=0
            course_turf=course_dirt=course_jump=0
            # class属性の一覧を取得して変数に格納する
            if len(elements_2)!=0:
                for elem_2 in elements_2:
                    class_str = elem_2.get_attribute("class")
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

            check_1=hearder[0]

            if (("芝" in check_1) or ("ダ" in check_1) or ("障" in check_1)) and ("m" in check_1):
                if ("芝" in check_1):
                    course_turf=1
                    distance=check_1.replace("芝","")
                    del hearder[0]
                    continue                           
                elif ("ダ" in check_1):
                    course_dirt=1
                    del hearder[0]
                    continue   
                elif ("障" in check_1):
                    course_jump=1
                    del hearder[0]
                    continue   


            print("dami-")

        









    
    



main()