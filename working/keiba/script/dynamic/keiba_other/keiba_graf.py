#import pandas as pd
import mysql.connector
import datetime
import openpyxl
import numpy as np
import matplotlib.pyplot as plt
import openpyxl
from openpyxl.drawing.image import Image
import subprocess

conn = mysql.connector.connect(
host='192.168.1.104',
port='3306',
user='connect',
password='Fujieda1217', 
database='keiba'
)
cursor = conn.cursor()

year=input("算出したい年を入力してください:")

subprocess.run(["mkdir /home/aweqse/keiba/output/"+year],shell=True)

tables_dict_index=0
weather_index=0
value_index=0
corse_weather_index=3
alphabet_index=0
corse_index=3
loop_index=0

value=["horse_weight","agari3haron"]
weather=["良","稍","重","不"]
tables_dict=["nakayama_d1200m","nakayama_d1800m","nakayama_d2400m","nakayama_d2500m",
             "nakayama_t1200m","nakayama_t1600m","nakayama_t1800m","nakayama_t2000m","nakayama_t2200m","nakayama_t2500m","nakayama_t3600m",
             "tokyo_t1400m","tokyo_t1600m","tokyo_t1800m","tokyo_t2000m","tokyo_t2300m","tokyo_t2400m","tokyo_t2500m","tokyo_t3400m",
             "tokyo_d1300m","tokyo_d1400m","tokyo_d1600m","tokyo_d2100m",
             "kyoto_t1200m","kyoto_t1400m_in","kyoto_t1400m_out","kyoto_t1600m_in","kyoto_t1600m_out","kyoto_t1800m","kyoto_t2000m","kyoto_t2200m","kyoto_t2400m","kyoto_t3000m","kyoto_t3200m",
             "kyoto_d1200m","kyoto_d1400m","kyoto_d1800m","kyoto_d1900m",
             "hanshin_t1200m","hanshin_t1400m","hanshin_t1600m","hanshin_t1800m","hanshin_t2000m","hanshin_t2200m","hanshin_t2400m","hanshin_t2600m","hanshin_t3000m","hanshin_t3200m",
             "hanshin_d1200m","hanshin_d1400m","hanshin_d1800m","hanshin_d2000m",
             "chukyo_t1200m","chukyo_t1400m","chukyo_t1600m","chukyo_t2000m","chukyo_t2200m",
             "chukyo_d1200m","chukyo_d1400m","chukyo_d1800m","chukyo_d1900m",
             "sapporo_t1200m","sapporo_t1500m","sapporo_t1800m","sapporo_t2000m","sapporo_t2600m",
             "sapporo_d1000m","sapporo_d1700m","sapporo_d2400m",
             "hakodate_t1000m","hakodate_t1200m","hakodate_t1800m","hakodate_t2000m","hakodate_t2600m",
             "hakodate_d1000m","hakodate_d1700m","hakodate_d2400m",
             "fukushima_t1200m","fukushima_t1800m","fukushima_t2000m","fukushima_t2600m",
             "fukushima_d1150m","fukushima_d1700m","fukushima_d2400m",
             "niigata_t1000m","niigata_t1200m","niigata_t1400m","niigata_t1600m","niigata_t1800m","niigata_t2000m_in","niigata_t2000m_out","niigata_t2200m","niigata_t2400m",
             "niigata_d1200m","niigata_d1800m","niigata_d2500m",
             "kokura_t1200m","kokura_t1800m","kokura_t2000m","kokura_t2600m","kokura_d1000m","kokura_d1700m","kokura_d2400m",
             "tokyo_s3000m","tokyo_s3100m","tokyo_s3110m","nakayama_s2880m","nakayama_s3200m","nakayama_s3210m","nakayama_s3350m","nakayama_s3570m","nakayama_s4100m","nakayama_s4250m","kyoto_s2910m","kyoto_s3170m","kyoto_s3930m","hanshin_s2970m","hanshin_s3110m","hanshin_s3140m","hanshin_s3900m","kokura_s2860m","kokura_s3390m","kokura_s2900m","niigata_s2850m","niigata_s2890m","niigata_s3250m","niigata_s3290m","fukushima_s2750m","fukushima_s2770m","fukushima_s3350m","fukushima_s3380m","chukyo_s3000m","chukyo_s3300m","chukyo_s3330m","chukyo_s3900m"
             ]
alphabet=["A","B","C","D","E","F","G","H","I"]
query_array=[]
sanpu_array=[]

#クエリとシート名を生成する
while len(tables_dict)>tables_dict_index:
    
    #配列から値を取り出す
    corse=tables_dict[tables_dict_index]
    corse
    baba=weather[weather_index]
    comparison_element=value[value_index]
    
    #実行ためのクエリと散布図名を生成する
    df_query="select race_time,"+comparison_element+" from "+corse+" where baba='"+baba+"' and year_="+str(year)+";"
    query_array.append(df_query)
    sanpu_array.append(corse+"_"+baba+"_"+comparison_element)
    
    #indexの処理
    alphabet_index=alphabet_index+1    
    if weather_index<3:
        weather_index=weather_index+1
    elif weather_index==3 and value_index==1:
        alphabet_index=0
        value_index=0
        weather_index=0
        tables_dict_index=tables_dict_index+1
        corse_weather_index=corse_weather_index+1
    elif weather_index==3: 
        weather_index=0
        value_index=value_index+1
print("クエリ文と散布図名を配列に格納完了")

#クエリを実行して結果を配列に格納する
query_index=0
result_array=[]
while len(query_array)>query_index:
    query=query_array[query_index]

    #クエリを実行する
    cursor.execute(query)
    result = cursor.fetchall()
    result_array.append(result)

    #インデックスの処理
    query_index=query_index+1

# カーソルとコネクションを閉じる
conn.close()
print("クエリ結果の配列化完了")

#excelファイルを生成する
#excel_path="C:\\workspace\\散布図\\"+str(year)+"\\競馬相関関係表.xlsx"
excel_path="/home/aweqse/keiba/output/"+str(year)+"/"+str(year)+"競馬相関関係表.xlsx"
wb = openpyxl.Workbook()

#シートを作成する
wb["Sheet"].title = str(year)+"年_相関関係表"

#初期値を書き込む
sheet=wb[str(year)+"年_相関関係表"]
sheet["A1"]="相関関係表"
sheet["B1"]="馬体重"
sheet["F1"]="上がり3ハロン"
sheet["B2"]="良"
sheet["C2"]="稍"
sheet["D2"]="重"
sheet["E2"]="不"
sheet["F2"]="良"
sheet["G2"]="稍"
sheet["H2"]="重"
sheet["I2"]="不"

#クエリ結果を加工する
result_index=0
alphabet_index=0
corse_weather_index=3
tables_dict_index=0
while len(result_array)>result_index:
    #加工する配列を取り出す
    procees_result=result_array[result_index]
    result_count=0
    cache_x=[]
    cache_y=[]
    len_result=len(procees_result)
    
    #コースごとにレースタイムが0のデータを削除する
    while len_result>result_count:
        if procees_result[result_count][0]==0.0:
            del procees_result[result_count]
            len_result=len(procees_result)
            continue
        elif procees_result[result_count][0]==0:
            del procees_result[result_count]
            len_result=len(procees_result)
            continue
        cache_x.append(procees_result[result_count][0]) #racetime
        cache_y.append(procees_result[result_count][1]) 
        result_count=result_count+1
    print("クエリ結果の加工完了")
    
    #相関係数を算出する
    date=np.array(procees_result)    
    correlation_matrix =np.corrcoef(date.T)
    print(correlation_matrix)
    print("相関関係の算出完了")

    #データがない場合の処理
    if len(date)==0:
        soukan_value=0 
    else:
        soukan_value=correlation_matrix[0][1]

    #エクセルの書き込む列を指定する
    writte_alpha=alphabet[alphabet_index]
    sheet_index=writte_alpha+str(corse_weather_index)

    #コースを書き込む
    if writte_alpha=="A":
        sheet[sheet_index]=tables_dict[tables_dict_index]
        tables_dict_index=tables_dict_index+1
        alphabet_index=alphabet_index+1 
        continue

    else:
        sheet[sheet_index]=soukan_value   #相関係数を書き込む
    print("相関関係の書き込み完了")
    
    # 散布図の作成
    if soukan_value!=0:
        plt.figure(figsize=(6, 4))
        plt.scatter(cache_x,cache_y, s=10,c='blue', alpha=1)
        plt.xlabel("race_time")
        plt.ylabel(comparison_element)
        plt.title(sanpu_array[result_index])
        plt.grid(True)

        # 画像ファイルとして保存
        scatter_plot_path = "/home/aweqse/keiba/output/"+str(year)+"/"+sanpu_array[result_index]
        #scatter_plot_path = "C:\\workspace\\散布図\\"+str(year)+"\\"+sanpu_array[result_index]
        plt.savefig(scatter_plot_path, dpi=100)
        plt.close()
        print("画像の保存完了")
    
    #indexの処理
    result_index=result_index+1
    alphabet_index=alphabet_index+1 
    if alphabet_index==9:
        alphabet_index=0
        corse_weather_index=corse_weather_index+1
    
    #以下はプログラム完了後マスクか削除
    #wb.save(excel_path)
    continue
#保存する
wb.save(excel_path)
print("すべての処理が終了しました!!")

