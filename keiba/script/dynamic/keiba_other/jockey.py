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

#year=input("算出したい年を入力してください:")

#subprocess.run(["mkdir /home/aweqse/keiba/output/"+year],shell=True)

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
alphabet=["A","B","C","D","E","F","G","H","J","K","L","M","N","O","P","Q"]

tables_dict_index=0


#クエリとシート名を生成する
#while len(tables_dict)>tables_dict_index:
    #クエリ文を生成する
    