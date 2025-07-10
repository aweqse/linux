import mysql.connector

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

#重複チェック
check_query="SELECT * FROM keiba.all_race WHERE id IN (SELECT id FROM keiba.all_race GROUP BY id HAVING COUNT(*) > 1);"
cursor.execute(check_query)
result = cursor.fetchall() # コミットしてトランザクション実行
if len(result)==0:
    #メール本文
    main_str="データベースの更新が完了しました。重複はありません。"
else:
    main_str="データベースの更新が完了しました。重複がありましたので重複日時を確認してロールバック等を実施し重複状態を解消してください。"

print("重複チェック完了")