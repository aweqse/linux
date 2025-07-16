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

insert_index=0
insert_list=["中山ダ1200m","中山ダ1800m","中山ダ2400m","中山ダ2500m",
             "中山芝1200m","中山芝1600m","中山芝1800m","中山芝2000m","中山芝2200m","中山芝2500m","中山芝3600m",
             "東京芝1400m","東京芝1600m","東京芝1800m","東京芝2000m","東京芝2300m","東京芝2400m","東京芝2500m","東京芝3400m",
             "東京ダ1300m","東京ダ1400m","東京ダ1600m","東京ダ2100m",
             "京都芝1200m","京都芝1400m内","京都芝1400m外","京都芝1600m内","京都芝1600m外","京都芝1800m","京都芝2000m","京都芝2200m","京都芝2400m","京都芝3000m","京都芝3200m",
             "京都ダ1200m","京都ダ1400m","京都ダ1800m","京都ダ1900m",
             "阪神芝1200m","阪神芝1400m","阪神芝1600m","阪神芝1800m","阪神芝2000m","阪神芝2200m","阪神芝2400m","阪神芝2600m","阪神芝3000m","阪神芝3200m",
             "阪神ダ1200m","阪神ダ1400m","阪神ダ1800m","阪神ダ2000m",
             "中京芝1200m","中京芝1400m","中京芝1600m","中京芝2000m","中京芝2200m",
             "中京ダ1200m","中京ダ1400m","中京ダ1800m","中京ダ1900m",
             "札幌芝1200m","札幌芝1500m","札幌芝1800m","札幌芝2000m","札幌芝2600m",
             "札幌ダ1000m","札幌ダ1700m","札幌ダ2400m",
             "函館芝1000m","函館芝1200m","函館芝1800m","函館芝2000m","函館芝2600m",
             "函館ダ1000m","函館ダ1700m","函館ダ2400m",
             "福島芝1200m","福島芝1800m","福島芝2000m","福島芝2600m",
             "福島ダ1150m","福島ダ1700m","福島ダ2400m",
             "新潟芝1000m","新潟芝1200m","新潟芝1400m","新潟芝1600m","新潟芝1800m","新潟芝2000m内","新潟芝2000m外","新潟芝2200m","新潟芝2400m",
             "新潟ダ1200m","新潟ダ1800m","新潟ダ2500m",
             "小倉芝1200m","小倉芝1800m","小倉芝2000m","小倉芝2600m",
             "小倉ダ1000m","小倉ダ1700m","小倉ダ2400m",
             "東京障3000m","東京障3100m","東京障3110m","中山障2880m","中山障3200m","中山障3210m","中山障3350m","中山障3570m","中山障4100m","中山障4250m","京都障2910m","京都障3170m","京都障3930m","阪神障2970m","阪神障3110m","阪神障3140m","阪神障3900m","小倉障2860m","小倉障3390m","小倉障2900m","新潟障2850m","新潟障2890m","新潟障3250m","新潟障3290m","福島障2750m","福島障2770m","福島障3350m","福島障3380m","中京障3000m","中京障3300m","中京障3330m","中京障3900m"]

tables_dict={"中山ダ1200m":"nakayama_d1200m","中山ダ1800m":"nakayama_d1800m","中山ダ2400m":"nakayama_d2400m","中山ダ2500m":"nakayama_d2500m",
             "中山芝1200m":"nakayama_t1200m","中山芝1600m":"nakayama_t1600m","中山芝1800m":"nakayama_t1800m","中山芝2000m":"nakayama_t2000m","中山芝2200m":"nakayama_t2200m","中山芝2500m":"nakayama_t2500m","中山芝3600m":"nakayama_t3600m",
             "東京芝1400m":"tokyo_t1400m","東京芝1600m":"tokyo_t1600m","東京芝1800m":"tokyo_t1800m","東京芝2000m":"tokyo_t2000m","東京芝2300m":"tokyo_t2300m","東京芝2400m":"tokyo_t2400m","東京芝2500m":"tokyo_t2500m","東京芝3400m":"tokyo_t3400m",
             "東京ダ1300m":"tokyo_d1300m","東京ダ1400m":"tokyo_d1400m","東京ダ1600m":"tokyo_d1600m","東京ダ2100m":"tokyo_d2100m",
             "京都芝1200m":"kyoto_t1200m","京都芝1400m内":"kyoto_t1400m_in","京都芝1400m外":"kyoto_t1400m_out","京都芝1600m内":"kyoto_t1600m_in","京都芝1600m外":"kyoto_t1600m_out","京都芝1800m":"kyoto_t1800m","京都芝2000m":"kyoto_t2000m","京都芝2200m":"kyoto_t2200m","京都芝2400m":"kyoto_t2400m","京都芝3000m":"kyoto_t3000m","京都芝3200m":"kyoto_t3200m",
             "京都ダ1200m":"kyoto_d1200m","京都ダ1400m":"kyoto_d1400m","京都ダ1800m":"kyoto_d1800m","京都ダ1900m":"kyoto_d1900m",
             "阪神芝1200m":"hanshin_t1200m","阪神芝1400m":"hanshin_t1400m","阪神芝1600m":"hanshin_t1600m","阪神芝1800m":"hanshin_t1800m","阪神芝2000m":"hanshin_t2000m","阪神芝2200m":"hanshin_t2200m","阪神芝2400m":"hanshin_t2400m","阪神芝2600m":"hanshin_t2600m","阪神芝3000m":"hanshin_t3000m","阪神芝3200m":"hanshin_t3200m",
             "阪神ダ1200m":"hanshin_d1200m","阪神ダ1400m":"hanshin_d1400m","阪神ダ1800m":"hanshin_d1800m","阪神ダ2000m":"hanshin_d2000m",
             "中京芝1200m":"chukyo_t1200m","中京芝1400m":"chukyo_t1400m","中京芝1600m":"chukyo_t1600m","中京芝2000m":"chukyo_t2000m","中京芝2200m":"chukyo_t2200m",
             "中京ダ1200m":"chukyo_d1200m","中京ダ1400m":"chukyo_d1400m","中京ダ1800m":"chukyo_d1800m","中京ダ1900m":"chukyo_d1900m",
             "札幌芝1200m":"sapporo_t1200m","札幌芝1500m":"sapporo_t1500m","札幌芝1800m":"sapporo_t1800m","札幌芝2000m":"sapporo_t2000m","札幌芝2600m":"sapporo_t2600m",
             "札幌ダ1000m":"sapporo_d1000m","札幌ダ1700m":"sapporo_d1700m","札幌ダ2400m":"sapporo_d2400m",
             "函館芝1000m":"hakodate_t1000m","函館芝1200m":"hakodate_t1200m","函館芝1800m":"hakodate_t1800m","函館芝2000m":"hakodate_t2000m","函館芝2600m":"hakodate_t2600m",
             "函館ダ1000m":"hakodate_d1000m","函館ダ1700m":"hakodate_d1700m","函館ダ2400m":"hakodate_d2400m",
             "福島芝1200m":"fukushima_t1200m","福島芝1800m":"fukushima_t1800m","福島芝2000m":"fukushima_t2000m","福島芝2600m":"fukushima_t2600m",
             "福島ダ1150m":"fukushima_d1150m","福島ダ1700m":"fukushima_d1700m","福島ダ2400m":"fukushima_d2400m",
             "新潟芝1000m":"niigata_t1000m","新潟芝1200m":"niigata_t1200m","新潟芝1400m":"niigata_t1400m","新潟芝1600m":"niigata_t1600m","新潟芝1800m":"niigata_t1800m","新潟芝2000m内":"niigata_t2000m_in","新潟芝2000m外":"niigata_t2000m_out","新潟芝2200m":"niigata_t2200m","新潟芝2400m":"niigata_t2400m",
             "新潟ダ1200m":"niigata_d1200m","新潟ダ1800m":"niigata_d1800m","新潟ダ2500m":"niigata_d2500m",
             "小倉芝1200m":"kokura_t1200m","小倉芝1800m":"kokura_t1800m","小倉芝2000m":"kokura_t2000m","小倉芝2600m":"kokura_t2600m","小倉ダ1000m":"kokura_d1000m","小倉ダ1700m":"kokura_d1700m","小倉ダ2400m":"kokura_d2400m",
             "東京障3000m":"tokyo_s3000m","東京障3100m":"tokyo_s3100m","東京障3110m":"tokyo_s3110m","中山障2880m":"nakayama_s2880m","中山障3200m":"nakayama_s3200m","中山障3210m":"nakayama_s3210m","中山障3350m":"nakayama_s3350m","中山障3570m":"nakayama_s3570m","中山障4100m":"nakayama_s4100m","中山障4250m":"nakayama_s4250m","京都障2910m":"kyoto_s2910m","京都障3170m":"kyoto_s3170m","京都障3930m":"kyoto_s3930m","阪神障2970m":"hanshin_s2970m","阪神障3110m":"hanshin_s3110m","阪神障3140m":"hanshin_s3140m","阪神障3900m":"hanshin_s3900m","小倉障2860m":"kokura_s2860m","小倉障3390m":"kokura_s3390m","小倉障2900m":"kokura_s2900m","新潟障2850m":"niigata_s2850m","新潟障2890m":"niigata_s2890m","新潟障3250m":"niigata_s3250m","新潟障3290m":"niigata_s3290m","福島障2750m":"fukushima_s2750m","福島障2770m":"fukushima_s2770m","福島障3350m":"fukushima_s3350m","福島障3380m":"fukushima_s3380m","中京障3000m":"chukyo_s3000m","中京障3300m":"chukyo_s3300m","中京障3330m":"chukyo_s3330m","中京障3900m":"chukyo_s3900m"}

#差分アップデートの実施
while len(insert_list)>insert_index:
    insert_str=insert_list[insert_index]
    keibajou=insert_str[0]+insert_str[1]
    kosu=insert_str[2:]
    tables=tables_dict[insert_list[insert_index]]
    print(tables+"の処理開始!!")
    insert="INSERT INTO "+tables+" SELECT * FROM all_race WHERE kaisaijou="+"'"+keibajou+"'"+" and cource="+"'"+kosu+"'"+" AND NOT EXISTS (SELECT 'X' FROM "+tables+" WHERE keiba."+tables+".id = all_race.id);"
    cursor.execute(insert)
    conn.commit() # コミットしてトランザクション実行
    insert
    insert_index=insert_index+1
    print(tables+"の処理完了!!")
    
print("処理完了!!")