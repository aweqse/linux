# coding: UTF-8
# 24時間稼働FXプログラム(linux)
# 仮想化環境で動作するには解像度に注意
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#linux・mac用(ラズパイで実行する場合はヘッドレスモードをオフにしないと正常に動作しないので注意)
options = webdriver.ChromeOptions()
#options.add_argument("--headless=new")
options.add_argument('--disable-gpu')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')
options.add_argument('--disable-web-security')
options.add_argument('--blink-settings=imagesEnabled=false')
options.add_argument('--ignore-certificate-errors')
driver = webdriver.Chrome(options=options)

#各種パス
yahoo_path="https://finance.yahoo.co.jp/quote/USDJPY=FX"
SBI_path="https://www.sbifxt.co.jp/"
wait_xpath="/html/body/div/main/div/div[2]/div[1]/div[2]/section[1]/div[3]/div/div[1]/dl/dd/span"
now_value_path="/html/body/div/main/div/section/div[2]/div/div[1]/div[2]/dl/dd/span"
SBI_element="/html/body/section/div[2]/div/div/form/div[1]/p[2]/input"

#URLにアクセスしする
driver.get(yahoo_path)
print(driver.current_url)
driver.maximize_window() #全画面表示でないと証拠金維持率が取得できないので注意 解像度もフルHDにする
print(driver.current_url)

#要素が表示されるまで待機する
WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.XPATH, now_value_path))
)

#now_valueを取得する
now_value = driver.find_element(By.XPATH, now_value_path)
#now_value, buy_valueを確定させる
now_value = now_value.text.replace('\n', '')
now_value = float(now_value)
l_buy_value = now_value-0.3
print("次の買い価格は"+str(l_buy_value)+"です")
sleep(2)
relod_count=0

# 以下テスト
now_value = 130
l_buy_value = 152
relod_count = 240

#現在の曜日・時刻を取得する。
today = datetime.date.today()
dt_now=datetime.datetime.now()
weekday=today.weekday()
hour=dt_now.hour

now_value_list = []
while now_value >= 1:  # continueのためのダミー
    #ロングの場合は現在の価格が低いとき（以下の条件式を満たさない）に買う処理に進む
    while now_value >= l_buy_value: 

        #時刻を判定基準とする処理のため時刻と曜日を取得する
        reboot_flag=0
        today = datetime.date.today()
        dt_now=datetime.datetime.now()
        weekday=today.weekday()
        hour=dt_now.hour
        minute=dt_now.minute
        just_now=str(hour)+":"+str(minute)

        #再起動のため6:00になったらreboot_flagを1にする
        if hour==6:
            reboot_flag=1
        if reboot_flag==1 and hour==7:
            #linuxの場合
            #subprocess.run("reboot")
            #windwsの場合
            pass

        #土曜日の７時を過ぎたら月曜日の７時まで待機する（１時間ごとに判定する）
        weekcount=0
        while (weekday==5 and hour>7) or  weekday==6 or (weekday==0 and hour<6):
            print(str(weekcount)+"/取引時間外なので休止中です")
            sleep(3600)
            today = datetime.date.today()
            dt_now=datetime.datetime.now()
            weekday=today.weekday()
            hour=dt_now.hour
            weekcount=weekcount+1

        #now_valueとl_buy_valueの差が1円開いたらl_buy_valueを更新する
        if now_value>=l_buy_value+0.8:
            l_buy_value=now_value-0.3

        #メモリリソースの枯渇を防ぐため２時間ごとにブラウザを再起動する
        if relod_count==3600:
            driver.quit()
            relod_count=1
            driver = webdriver.Chrome(options=options)
            driver.get(yahoo_path)
            print(driver.current_url)
            driver.maximize_window()
            continue
        
        #8分たったらリロードする（2秒*240=480=5分）
        elif relod_count%240 == 0:
            driver.get(yahoo_path)
            print(driver.current_url)
            print("リロード判定のために要素を検索しています")
            #要素が表示されるまで待機する
            WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, now_value_path))
            )
            judgement=len(driver.find_elements(By.XPATH, now_value_path))
            print(driver.current_url)

            print("要素の検索終了")
            #リロード判定をする
            while judgement==0:
                print("現在の価格が取得できないためリロードを行います")
                driver.get(yahoo_path)
                #要素が表示されるまで待機する
                WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, now_value_path))
                )
                print(driver.current_url)  
                judgement=len(driver.find_elements(By.XPATH, now_value_path))

            now_value = driver.find_element(By.XPATH, now_value_path)
            now_value = now_value.text.replace('\n', '')            
            print("リロード完了")
            print("次の買い価格は"+str(l_buy_value)+"です。 "+just_now)
            
            now_value_list=[]
            relod_count = relod_count+1
            now_value=float(now_value)
            continue

        elif relod_count < 3600:
            #要素が表示されるまで待機する
            WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, now_value_path))
            )
            now_value = driver.find_element(By.XPATH,now_value_path)
            #now_value, buy_valueを確定させる
            now_value = now_value.text.replace("\n", "")
            now_value = float(now_value)
            print(now_value)
            #下記のsleepは現在価格を取得する間隔なので削除しないこと
            relod_count = relod_count+1

            # 10回同じ値の場合リロードする
            #以下テスト
            #now_value_list=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

            if len(now_value_list) == 15:
                del now_value_list[0]
                now_value_list.append(now_value)
                now_value_set = set(now_value_list)
                #同じ価格が続く場合

                #以下テスト
                #now_value_set={1,1,1,1,1,1,1,1,1,1,1,1,1,1,1}

                if len(now_value_set) == 1:
                    today = datetime.date.today()
                    dt_now=datetime.datetime.now()
                    weekday=today.weekday()
                    hour=dt_now.hour

            else:
                now_value_list.append(now_value)
            continue

    else:
        if now_value <= l_buy_value:  # 買い注文(ロング)
            driver.get(SBI_path)
            print(driver.current_url)
            #要素が表示されるまで待機する
            WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, SBI_element))
            )
            print(driver.current_url)

            print("リロード判定のために要素を検索しています")
            judgement_2=len(driver.find_elements(By.XPATH, SBI_element))
            print("要素の検索終了")
            while judgement_2==0:
                print("現在の価格が取得できないためリロードを行います")
                driver.get(SBI_path)
                #要素が表示されるまで待機する
                WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, SBI_element))
                )
                judgement_2=len(driver.find_elements(By.XPATH, SBI_element))
            print("アクセス完了")
            print("購入処理を開始します")
            
            #SBI_FXトップ画面
            print(driver.current_url)
            #読み込み待ちの処理
            input_element_user = WebDriverWait(driver, 180).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div[2]/div/div/form/div[1]/p[2]/input")))
            input_element_user.send_keys("7644016862")
            input_element_pass = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "/html/body/section/div[2]/div/div/form/div[1]/p[3]/input")))
            input_element_pass.send_keys("guxvudfarqy8TarhGj")
            #要素が表示されるまで待機する
            WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/section/div[2]/div/div/form/div[3]/p/a"))
            )
            driver.find_element(By.XPATH, "/html/body/section/div[2]/div/div/form/div[3]/p/a").click()

            #画面遷移する(URLが切り替わる)
            #購入するドル数を計算する
            #要素が表示されるまで待機する
            WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div/div/div[1]/section/div/section/div[1]/div[1]/div/dl/dd/span[1]"))
            )
            doller_value=driver.find_elements(By.XPATH,"/html/body/div[3]/div/div/div[1]/section/div/section/div[1]/div[1]/div/dl/dd/span[1]")
            while len(doller_value)==0:
                print("購入するドル数が取得できなかったのでリロードを行います")
                WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div/div/div[1]/section/div/section/div[1]/div[1]/div/dl/dd/span[1]"))
                )
                doller_value=driver.find_elements(By.XPATH,"/html/body/div[3]/div/div/div[1]/section/div/section/div[1]/div[1]/div/dl/dd/span[1]")
            doller_value=doller_value[0].text
            doller_value=doller_value.replace(",","")
            doller_value=int(doller_value)
            buy_doller=doller_value/1000
            buy_doller=int(buy_doller)

            #テスト用パラメーター
            #buy_doller=1
            WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div/div/div[1]/section/section[1]/div/div/ul/li[1]/p/button[1]/span"))
            )
            driver.find_element(
                By.XPATH, "/html/body/div[3]/div/div/div[1]/section/section[1]/div/div/ul/li[1]/p/button[1]/span").click()

            print("ログインに成功しました。購入処理をはじめます")

            #証拠金維持率を取得する
            WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/nav/div/div/div/section[1]/ul/li[3]/span"))
            )
            marge=driver.find_elements(By.XPATH,"/html/body/div[3]/nav/div/div/div/section[1]/ul/li[3]/span")
            
            #証拠金維持率が取得できなかったための処理
            while len(marge)==0:
                print("証拠金維持率を取得できなかったので再度取得します")
                driver.get("https://trade.sbifxt.co.jp/aweb/home.jsp")
                WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/nav/div/div/div/section[1]/ul/li[4]/span"))
                )
                marge=driver.find_elements(By.XPATH,"/html/body/div[3]/nav/div/div/div/section[1]/ul/li[4]/span")                    
            marge=marge[0].text         
            marge_par=marge.replace("%","").replace(",","")
            
            #買い玉がない場合の処理
            while marge_par=="-":
                print("証拠金維持率が取得できないのでリロードします。")
                driver.get("https://trade.sbifxt.co.jp/aweb/home.jsp")
                WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/nav/div/div/div/section[1]/ul/li[4]/span"))
                )
                marge=driver.find_element(By.XPATH,"/html/body/div[3]/nav/div/div/div/section[1]/ul/li[4]/span") 
                marge=marge.text         
                marge_par=marge.replace("%","").replace(",","")
            print("証拠金維持率は"+marge_par+"です")
            marge_par=float(marge_par)
            
            #テスト用パラメーター
            #marge_par=1500

            #証拠金維持率から購入するかの条件分岐をする
            limt_marge=1000 #初期値は250
            safe_marge=2000
            if marge_par<limt_marge:
                print("証拠金維持率が設定値を下回っているので購入処理をスキップします")
                # buy_valueを確定させる
                driver.get(yahoo_path)
                WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, now_value_path))
                )
                print(driver.current_url)
                print("リロード判定のために要素を検索しています")
                judgement=len(driver.find_elements(By.XPATH, now_value_path))
                print("要素の検索終了")
                #リロード判定をする
                while judgement==0:
                    print("現在の価格が取得できないためリロードを行います")
                    driver.get(yahoo_path)
                    WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, now_value_path))
                    )
                    print(driver.current_url)
                    judgement=len(driver.find_elements(By.XPATH, now_value_path))
                now_value = driver.find_element(By.XPATH, now_value_path)
                now_value = now_value.text.replace('\n', '')            
                print("リロード完了")
                now_value=float(now_value)
                l_buy_value = now_value-0.3
                print("次の買い価格は"+str(l_buy_value)+"です")
                now_value_list=[]
                relod_count = 0
                continue

            else:
                #注文期間を１年に変更する処理
                WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/nav/div/div/div/label"))
                )
                driver.find_element(
                    By.XPATH, "/html/body/div[3]/nav/div/div/div/label").click()
                WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/nav/div/div/div/div[1]/ul/li[10]/div"))
                )
                driver.find_element(
                    By.XPATH, "/html/body/div[3]/nav/div/div/div/div[1]/ul/li[10]/div").click()
                WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/nav/div/div/div/div[1]/ul/li[10]/ul/li[4]/a"))
                )
                WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located)
                driver.find_element(
                    By.XPATH, "/html/body/div[3]/nav/div/div/div/div[1]/ul/li[10]/ul/li[4]/a").click()
                WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/nav/div/div/div/div[3]/div[2]/div[1]/section[1]/div/div/div[1]/dl[1]/dd/button"))
                )
                driver.find_element(
                    By.XPATH, "/html/body/nav/div/div/div/div[3]/div[2]/div[1]/section[1]/div/div/div[1]/dl[1]/dd/button").click()
                WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/nav/div/div/div/div[3]/div[2]/div[2]/div[2]/div/form/div[5]/label[3]"))
                )       
                driver.find_element(
                    By.XPATH, "/html/body/nav/div/div/div/div[3]/div[2]/div[2]/div[2]/div/form/div[5]/label[3]").click()
                WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/nav/div/div/div/div[3]/div[2]/div[2]/div[2]/div/form/div[6]/button[1]"))
                )    
                driver.find_element(
                    By.XPATH, "/html/body/nav/div/div/div/div[3]/div[2]/div[2]/div[2]/div/form/div[6]/button[1]").click()
                WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/nav/div/div/div/div[3]/div[2]/div[7]/div[3]/div/button"))
                )    
                driver.find_element(
                    By.XPATH, "/html/body/nav/div/div/div/div[3]/div[2]/div[7]/div[3]/div/button").click()
                driver.get("https://trade.sbifxt.co.jp/aweb/home.jsp")
                print("設定変更完了")

                buy_doller=int(buy_doller/2)
                # 成行買い
                WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/nav/div/div/div/div[3]/div/div[1]/div[2]/div[1]/section/form/div[1]/input[3]"))
                )   
                driver.find_element(
                    By.XPATH, "/html/body/div[3]/nav/div/div/div/div[3]/div/div[1]/div[2]/div[1]/section/form/div[1]/input[3]").click()
                WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/nav/div/div/div/div[3]/div/div[1]/div[2]/div[1]/section/form/div[2]/div[4]/div/input[2]"))
                )   
                txtbox=driver.find_element(
                    By.XPATH, "/html/body/div[3]/nav/div/div/div/div[3]/div/div[1]/div[2]/div[1]/section/form/div[2]/div[4]/div/input[2]")
                txtbox.clear()
                driver.find_element(
                    By.XPATH, "/html/body/div[3]/nav/div/div/div/div[3]/div/div[1]/div[2]/div[1]/section/form/div[2]/div[4]/div/input[2]").send_keys(str(buy_doller))
                WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/nav/div/div/div/div[3]/div/div[1]/div[2]/div[1]/section/form/div[2]/div[7]/div[1]/label/span/span"))
                )   
                driver.find_element(
                    By.XPATH, "/html/body/div[3]/nav/div/div/div/div[3]/div/div[1]/div[2]/div[1]/section/form/div[2]/div[7]/div[1]/label/span/span").click()
                WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/nav/div/div/div/div[3]/div/div[1]/div[2]/div[1]/section/form/div[2]/div[8]/input"))
                )   
                driver.find_element(
                    By.XPATH, "/html/body/div[3]/nav/div/div/div/div[3]/div/div[1]/div[2]/div[1]/section/form/div[2]/div[8]/input").click()
                WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/nav/div/div/div/div[3]/div/div[1]/div[2]/div[1]/div[5]/div[2]/div/form/div[1]/button[1]"))
                )   
                driver.find_element(
                    By.XPATH, "/html/body/div[3]/nav/div/div/div/div[3]/div/div[1]/div[2]/div[1]/div[5]/div[2]/div/form/div[1]/button[1]").click()
                WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/nav/div/div/div/div[3]/div/div[1]/div[2]/div[1]/section/form/div[2]/div[8]/div/div[1]/input"))
                )   
                driver.find_element(
                    By.XPATH, "/html/body/div[3]/nav/div/div/div/div[3]/div/div[1]/div[2]/div[1]/section/form/div[2]/div[8]/div/div[1]/input").send_keys("50")
                WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/nav/div/div/div/div[3]/div/div[1]/div[2]/div[1]/section/form/div[2]/div[9]/div/div/div[1]/div[2]/p[2]"))
                )   
                driver.find_element(
                    By.XPATH, "/html/body/div[3]/nav/div/div/div/div[3]/div/div[1]/div[2]/div[1]/section/form/div[2]/div[9]/div/div/div[1]/div[2]/p[2]").click()

                print("買い注文が完了しました")

                # buy_valueを確定させる
                driver.get(yahoo_path)
                print("リロード判定のために要素を検索しています")
                #読み込み待ちの処理
                WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, now_value_path))
                )   
                print(driver.current_url)
                judgement=len(driver.find_elements(By.XPATH, now_value_path))
                print("要素の検索終了")
                #リロード判定をする
                while judgement==0:
                    print("現在の価格が取得できないためリロードを行います")
                    sleep(2)
                    driver.get(yahoo_path)
                    sleep(2)
                    #読み込み待ちの処理
                    WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, now_value_path))
                    )  
                    print(driver.current_url)
                    judgement=len(driver.find_elements(By.XPATH, now_value_path))
                now_value = driver.find_element(By.XPATH, now_value_path)
                now_value = now_value.text.replace('\n', '')            
                print("リロード完了")
                now_value=float(now_value)
                l_buy_value = now_value-0.3
                print("次の買い価格は"+str(l_buy_value)+"です")
                now_value_list=[]
                relod_count = 0
                continue
        