import subprocess
import re

while True:
    file_path="/home/aweqse/nas/temp"
    result=subprocess.run(["sudo","-S","blkid"],input="Fujieda1217",capture_output=True,text=True) 
    #resultの内容を行単位で配列の格納する
    uuid=result.stdout.splitlines()
    #行のスペースを排除して配列に格納する
    uuid_pattern_1="^/dev"
    uuid_pattern_2="^UUID="
    uuid_pattern_3="^TYPE="
    check_uuid=[]
    uuid_count=0
    temp_count=0
    append_count=0
    delete_count=0
    while len(uuid)>delete_count:
        delete_str=uuid[delete_count]
        if ("loop" in delete_str)==True:
            del uuid[delete_count]
            continue
        else:
            delete_count=delete_count+1

    while len(uuid)>uuid_count:
        temp=uuid[uuid_count].split()
        while len(temp)>temp_count:
            check=temp[temp_count]
            append_0=uuid_count
            if re.search(uuid_pattern_1,check):
                append_1=check.replace(":","")
            if re.search(uuid_pattern_2,check):
                append_2=check.replace('"',"")
            if re.search(uuid_pattern_3,check):
                append_3=check.replace("TYPE=","")
                append_3=append_3.replace('"',"")
                if append_3=="ntfs":
                    subprocess.run(["sudo","ntfsfix",append_1])
                check_uuid.append([append_0,append_1,append_2,append_3])
            temp_count=temp_count+1
        temp_count=0
        uuid_count=uuid_count+1

    #ディスクの容量を配列に追加する
    result_2=subprocess.run(["df","-h"],capture_output=True,text=True)
    df=result_2.stdout.splitlines()
    uuid_count_2=0
    df_count=0
    while len(check_uuid)>uuid_count_2:
        df_pattern="^"+check_uuid[uuid_count_2][1]
        while len(df)>df_count:
            check_1=df[df_count]
            if re.search(df_pattern,check_1):
                df_split=df[df_count].split()
                df_append=df_split[1] #dfコマンドの仕様が変わったらインデックスを変更する
                check_uuid[uuid_count_2].append(df_append)
                df_count=df_count+1
                df_pattern="^"+check_uuid[uuid_count_2][1]
            else:
                df_count=df_count+1
        df_count=0
        uuid_count_2=uuid_count_2+1

    #容量が確認できなかったドライブは削除する
    delete_count=0
    while len(check_uuid)>delete_count:
        check_3=len(check_uuid[delete_count])
        if check_3==2:
            del check_uuid[delete_count]
        delete_count=delete_count+1

    print("以下がドライブの情報となります。\n 項番,      パス,       UUID,                            容量")
    print_number=0
    while len(check_uuid)>print_number:
        print(check_uuid[print_number])
        print_number=print_number+1
    print("以上")

    input_array=[]
    input_number=input("共有したいドライブの左端の数値を入力してください。\n※複数のドライブを選択する場合はカンマ区切りで入力してください：")
    input_array=input_number.split(",")
    print(input_array)
    mkdir_str=input("マウントするドライブのディレクトリ名を入力してください。\n※複数ある場合はカンマで区切りで入力してください。ドライブの区切り順と対応するディレクトリ名となります。\n※ディレクトリのパスは/mnt/~となります\n：")
    mkdir_str=mkdir_str.split(",")
    if len(input_array)==len(mkdir_str):
        #ディレクトリ名の重複チェック
        mkdir_count=0
        result_3_count=0
        result_3=subprocess.run(["sudo","-S","ls","-a","/mnt"],input="Fujieda@1217",capture_output=True,text=True)
        result_3=result_3.stdout.splitlines()
        while len(result_3)>result_3_count:
            if len(mkdir_str)>mkdir_count:
                if result_3[result_3_count]==mkdir_str[mkdir_count]:
                    print("ディレクトリ名が重複しています。ディレクトリ名を確認して最初からやり直してください")
                    exit()
                else: 
                    mkdir_count=mkdir_count+1
            else:
                mkdir_count=0
                result_3_count=result_3_count+1

    else:
        continue_flg=input("入力したドライブ数とディレクトリ数が違います。もう一度やり直す場合は'y'を入力してください。\n:")
        if continue_flg=="y" or continue_flg=="Y":
            continue   
        else:
            exit()

    #ディレクトリを作成する
    mkdir_count_2=0
    mkdir_array=[]
    while len(mkdir_str)>mkdir_count_2:
        mkdir_name="/mnt/"+mkdir_str[mkdir_count_2]
        subprocess.run(["sudo","-S","mkdir",mkdir_name],input="Fujieda@1217",capture_output=True,text=True)
        subprocess.run(["sudo","chmod","777",mkdir_name])
        mkdir_array.append(mkdir_name)
        mkdir_count_2=mkdir_count_2+1
    print("ディレクトリ作成成功") 

    #mマウントを実行する
    input_count=0
    uuid_array=[]
    type_array=[]

    while len(input_array)>input_count:
        mkdir_name=mkdir_array[input_count]
        sorce_number=int(input_array[input_count])
        sorce_path=check_uuid[sorce_number][1]
        uuid_str=check_uuid[sorce_number][2]
        type=check_uuid[sorce_number][3]
        type_array.append(type)
        uuid_array.append(uuid_str)
        subprocess.run(["sudo","-S","mount",sorce_path,mkdir_name],input="Fujieda@1217",capture_output=True,text=True)
        input_count=input_count+1
    print("マウント完了")

    #fstabファイルを生成する
    subprocess.run(["sudo","-S","chmod","777","/etc/fstab"])
    fs_count=0
    while len(input_array)>fs_count:
        uuid_str=uuid_array[fs_count]
        path_str=mkdir_array[fs_count]
        type_str=type_array[fs_count]
        defaults="defaults"
        zero="0"

        with open("/etc/fstab", "a") as f:
            subprocess.run(["echo",uuid_str+" "+path_str+" "+type_str+" "+defaults+" "+zero+" "+zero], stdout=f)
        fs_count=fs_count+1
    print("fstabの出力完了しました")

    #sambaのインストール
    subprocess.run(["apt","install" ,"samba","-y"])
    #smb.confを出力する
    subprocess.run(["sudo","-S","chmod","777","/etc/samba/smb.conf"])
    smb_count=0
    while len(input_array)>smb_count:
        smb_1="["+mkdir_array[smb_count].replace("/mnt/","")+"]"+"\n"
        smb_2="writeable = yes\n"
        smb_3="path = "+ mkdir_array[smb_count]+"\n"
        smb_4="browseable = yes\n"
        smb_5="guest ok = yes\n"
        smb_6="guest only = yes\n"
        smb_7="create mod = 0777\n"
        smb_8="directory mode = 0777\n"
        smb_9="read_only = no"
        smb=smb_1+smb_2+smb_3+smb_4+smb_5+smb_6+smb_7+smb_8+smb_9+"\n"
        with open("/etc/samba/smb.conf", "a") as f:
                subprocess.run(["echo",smb], stdout=f)
        smb_count=smb_count+1
    print("sambaの設定完了")
    subprocess.run(["sudo","systemctl", "restart", "smbd"])
    subprocess.run(["sudo","systemctl", "enable", "smbd"])



    exit()





