import datetime
import subprocess
from time import sleep

program_1="python3 /home/aweqse/keiba/script/dynamic/datebase_update.py"
program_2="python3 /home/aweqse/keiba/script/dynamic/duplication_check.py"
program_3="python3 /home/aweqse/keiba/script/dynamic/insert.py"
program_4="python3 /home/aweqse/keiba/script/dynamic/jra_time.py"

#プログラムを起動するかどうかの判定をする
#プログラムを起動した日を取得する
now = datetime.datetime.now()
weekday_now=now.weekday()

if weekday_now==1:
    sleep(15)
    subprocess.run([program_1],shell=True)
    subprocess.run([program_2],shell=True)
    subprocess.run([program_3],shell=True)
    subprocess.run([program_4],shell=True)
else:
    print("更新日でないため処理をスキップします。")