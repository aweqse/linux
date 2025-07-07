from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import random
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import base64
import os
from email.mime.text import MIMEText


options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument('--disable-gpu')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')
options.add_argument('--disable-web-security')
options.add_argument('--blink-settings=imagesEnabled=false')
options.add_argument('--ignore-certificate-errors')
options.add_argument("--disable-blink-features=AutomationControlled") 
options.add_argument("--window-size=1920,1080")

#webdriverからのアクセスした情報を削除する
#chromeのプロファイルを使用するオプション
options.add_argument(f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36')
driver = webdriver.Chrome(options=options)
WebDriverWait(driver, 45).until(EC.presence_of_all_elements_located)

#メール処理のための日付を取得する
#if str_value
now = datetime.datetime.now()
day_now=now.day
month_now=now.month
year_now = now.year
weekday=now.weekday()
now=str(year_now)+"年"+str(month_now)+"月"+str(day_now)+"日"

#サイトにアクセスする
login_path="https://moneyforward.com/me"
driver.get(login_path)
WebDriverWait(driver, 45).until(EC.presence_of_all_elements_located)

#ログインの処理
driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div/div[1]/div[1]/p[1]/a").click()
sleep(random.uniform(2, 3))
driver.find_element(By.XPATH,"/html/body/main/div/div/div[2]/div/section/div/form/div/div/input").send_keys("aweqsenotice@gmail.com")
sleep(random.uniform(2, 3))
driver.find_element(By.XPATH,"/html/body/main/div/div/div[2]/div/section/div/form/div/button").click()
sleep(random.uniform(2, 3))
driver.find_element(By.XPATH,"/html/body/main/div/div/div[2]/div/section/div/form/div/div[2]/input").send_keys("Fujieda1217")
sleep(random.uniform(2, 3))
driver.find_element(By.XPATH,"/html/body/main/div/div/div[2]/div/section/div/form/div/button").click()
sleep(10)

# Gmail APIを読み取り権限で使う
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly','https://www.googleapis.com/auth/gmail.send']

#認証で使うjsonのpathを指定する
json_path="C:\\workspace\\プログラム\\クレカ利用金額通知プログラム\\client_secret_764453705025-d2mhtt05ln74s1sgo3dlqfje04nhjd6o.apps.googleusercontent.com.json"
token_path = "C:\\workspace\\プログラム\\クレカ利用金額通知プログラム\\token.json" 

#windows用
#json_path="C:\\workspace\\プログラム\\クレカ利用金額通知プログラム\\client_secret_764453705025-d2mhtt05ln74s1sgo3dlqfje04nhjd6o.apps.googleusercontent.com.json"
#token_path = "C:\\workspace\\プログラム\\クレカ利用金額通知プログラム\\token.json" 

#linux用
json_path="/home/aweqse/credit/script/client_secret_764453705025-d2mhtt05ln74s1sgo3dlqfje04nhjd6o.apps.googleusercontent.com.json"
token_path = "/home/aweqse/credit/script/token.json" 

creds = None
#過去にログイン済みなら認証情報を再利用する
if os.path.exists(token_path):
    creds = Credentials.from_authorized_user_file(token_path, SCOPES)
else: #初回ログイン時の処理
    flow = InstalledAppFlow.from_client_secrets_file(json_path, SCOPES)
    creds = flow.run_local_server(port=8080)
    with open(token_path, 'w') as token:
        token.write(creds.to_json())

# serviceでgmailAPIを操作できるようにする
service = build('gmail', 'v1', credentials=creds)

# 最新のメールを取得（1件）
results = service.users().messages().list(userId='me', maxResults=1, q="is:inbox").execute()
messages = results.get('messages', [])
sleep(5)

if not messages:
    print("メールが見つかりません。")
else:
    msg_id = messages[0]['id']
    message = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
    
    # メール本文を取得
    parts = message['payload'].get('parts')
    if parts:
        for part in parts:
            if part['mimeType'] == 'text/plain':
                data = part['body']['data']
                decoded_bytes = base64.urlsafe_b64decode(data)
                body_text = decoded_bytes.decode('utf-8')
                text_split=body_text.splitlines()
    else:
        # 単一パートのメール
        data = message['payload']['body']['data']
        decoded_bytes = base64.urlsafe_b64decode(data)
        body_text = decoded_bytes.decode('utf-8')
        text_split=body_text.splitlines()
        
#ワンタイムパスの抽出
text_index=0
while len(text_split)>text_index:
    #空の配列を削除する
    check_number=text_split[text_index]
    if len(check_number)==0:
        del text_split[text_index]
    elif len(check_number)==6:
        one_time_pass=check_number
        break
    else:
        text_index=text_index+1

#ログインする
sleep(5)
driver.find_element(By.XPATH,"/html/body/main/div/div/div[2]/div/section/div/form/div/div/input").send_keys(one_time_pass)
driver.find_element(By.XPATH,"/html/body/main/div/div/div[2]/div/section/div/form/div/button").click()
print("ログイン処理成功")
sleep(5)

#更新処理
driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div/section[3]/div/div[2]/a").click()
print("更新中")
sleep(5)

#ページを遷移する
login_path_2="https://moneyforward.com/cf"
driver.get(login_path_2)
value=driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div/div/div/section/section/div[1]/div[2]/table/tbody/tr/td[3]")
sleep(5)
page_state=driver.execute_script("return document.readyState")
print("urlが読み込まれているかをチェックします。")
while page_state!="complete":
    driver.get(login_path_2)
    print("URLの読み込みに失敗したため再読み込みします。")
    sleep(20)
    page_state=driver.execute_script("return document.readyState")
print("url読み込み完了")
value=value.text
sleep(2)

#下記の値は月の利用額の上限で適宜変更する
value=value.replace("円","")
value=value.replace(",","")
value=int(value)

#2025年5月のゴールデンウィークの特別処理
#value=value-189000

mouth_limit=120000
mouth_value=mouth_limit-value
day_now=int(day_now)
if day_now>5:
    rest_day=30-(day_now-5)
else:
    rest_day=30-(day_now+25)
    
rest_value=mouth_value/rest_day

main_str=str(now)+"時点での利用料金は"+str(value)+"円です。今月はあと"+str(mouth_value)+"円まで利用できます。一日当たり"+str(rest_value)+"円使えます"
print("通知する文章の作成完了")

#メールを作成する
sender = "aweqsenotice@gmail.com"
recipient = "aweqsenotice@gmail.com"
subject = "クレカ利用額通知"
to="aweqsenotice@gmail.com"
send_text = main_str

#メールの作成
message = MIMEText(send_text)
message['to'] = to
message['from'] = sender
message['subject'] = subject

#メール文をエンコード
raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
message_body = {'raw': raw_message}

#メール文を送信
response = service.users().messages().send(userId="me", body=message_body).execute()
print("メールの送信完了")
