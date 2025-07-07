
import datetime
import subprocess
from time import sleep
import os

#■注意点
#仮想マシンの制御はフルパス/usr/bin/virshで行う
#SCPやSSHを行う際はローカルユーザーで接続しているのでroot権限が必要な場合は"/usr/bin/virsh", "-c", "qemu:///system", "list", "--all"のように記述する

os.environ["SSH_AUTH_SOCK"] = "/run/user/1000/keyring/ssh" #cronでscpコマンドを実行すするには必須

now = datetime.datetime.now()
day_now=now.day
month_now=now.month
year_now = now.year

if len(str(day_now))==1:
    day_now="0"+str(day_now)

if len(str(month_now))==1:
    month_now="0"+str(month_now)

#今日の日付を定義する
today=str(year_now)+str(month_now)+str(day_now)

#パスワード
password="Fujieda1217/n"

#ファイルパス
mkdir_ubuntu_path="/home/aweqse/copy_temp/"+today+"/ubuntu/"
mkdir_windows_path="/home/aweqse/copy_temp/"+today+"/windows/"
copy_temp_path="/home/aweqse/copy_temp"
ubuntu_VMpath="/home/aweqse/copy_temp/"+today+"/ubuntu/"
keiba_ubuntu_path="/home/aweqse/copy_temp/"+today+"/ubuntu/keiba/"
VM_ubuntu_path="/home/aweqse/copy_temp/"+today+"/ubuntu/VM/"

#テスト用以下２つは排他
#ubuntu_file="/home/aweqse/tmp/main/"
ubuntu_file="/home/aweqse/main/"

#バックアップ対象のIPアドレスとフォルダを指定して配列に格納する将来的にはテキストを読み込む形も検討
FX_path="aweqse@192.168.1.101:/home/aweqse/FX"
credit_path="aweqse@192.168.1.102:/home/aweqse/credit"
NAS_path="aweqse@192.168.1.103:/home/aweqse/NAS"
keiba_path="aweqse@192.168.1.104:/home/aweqse/keiba"
vpn_path="aweqse@192.168.1.100:/home/aweqse/vpn"
backup_array=[FX_path,credit_path,NAS_path,keiba_path,vpn_path]

mkdir_command_1=["mkdir", "-p", mkdir_ubuntu_path]
mkdir_command_2=["mkdir", "-p", mkdir_windows_path]
mkdir_command_3=["mkdir", "-p", keiba_ubuntu_path]
mkdir_command_4=["mkdir", "-p", VM_ubuntu_path]
chmod_command_1=["chmod","-R","777",copy_temp_path]

subprocess.run(mkdir_command_1,text=True)
subprocess.run(mkdir_command_2,text=True)
subprocess.run(mkdir_command_3,text=True)
subprocess.run(mkdir_command_4,text=True)
subprocess.run(chmod_command_1,text=True)

#ubuntuのファイルをコピーする
ubuntu_cp=["cp","-r",ubuntu_file,mkdir_ubuntu_path]
subprocess.run(ubuntu_cp,text=True)
print("ubuntuのファイルコピー完了")

#フォルダごとコピーするので再度権限を設定する
subprocess.run(chmod_command_1,text=True)

#windowsマシンのファイルをコピーする
win_path = "aweqse@192.168.1.5:C:/workspace/"
scp_cammand=["scp","-r",win_path,mkdir_windows_path]
subprocess.run(scp_cammand,text=True)
print("windowsからフォルダのコピー完了")

#仮想マシンの名前を取得するhead_str="sVM_ubuntu_pathcp -r "
vm_name=[]
VM_list=["/usr/bin/virsh", "-c", "qemu:///system", "list", "--all"]
result_1=subprocess.run(VM_list,capture_output=True,text=True)
result=result_1.stdout.splitlines()[2:]

#何もない配列を削除する
delete_count=0
result_count=0
while len(result)>delete_count:
    if len(result[delete_count])==0:
        del result[delete_count]
    delete_count=delete_count+1

#配列から仮想マシンの名前のみ配列に格納する
while len(result)>result_count:
    temp=result[result_count].split()
    temp=temp[1] #現状ではここの位置で固定されている
    vm_name.append(temp)
    result_count=result_count+1

#仮想マシンを起動する
shutdown_count=0
while len(vm_name)>shutdown_count:
    shut_name=vm_name[shutdown_count]
    NM_start=["/usr/bin/virsh", "-c", "qemu:///system","start",shut_name]
    subprocess.run(NM_start,text=True)
    shutdown_count=shutdown_count+1
sleep(30)#shutdown待ち

#仮想マシンからファイルをコピーする
VM_count=0
while len(backup_array)>VM_count:
    VMcopy_path=backup_array[VM_count]
    VM_command=["scp","-r",VMcopy_path,ubuntu_VMpath]
    subprocess.run(VM_command)
    VM_count=VM_count+1
print("keibaからのファイルのコピー完了!")

#古いフォルダを削除する
rm_setup_script=["rm","-r","/home/aweqse/setup_script"]
subprocess.run(rm_setup_script,text=True)

#各VMのセットアップスクリプトをローカルにコピーする
local_copy=["cp","-r",ubuntu_VMpath,"/home/aweqse/setup_script"]
subprocess.run(local_copy,text=True)

#仮想マシンを停止する
shutdown_count=0
while len(vm_name)>shutdown_count:
    shut_name=vm_name[shutdown_count]
    VM_stop=["/usr/bin/virsh", "-c", "qemu:///system","shutdown",shut_name]
    subprocess.run(VM_stop,text=True)
    shutdown_count=shutdown_count+1
sleep(30)#shutdown待ち
delete_count

#バックアップする仮想マシンのディスクイメージをコピーする
copy_count=0
while len(vm_name)>copy_count:
    copy_name=vm_name[copy_count]
    command_3="/var/lib/libvirt/images/"+copy_name+".raw"
    command_8=["chmod", "777",VM_ubuntu_path+copy_name+".raw"]
    command_5=["/usr/bin/virsh", "-c", "qemu:///system", "dumpxml",copy_name]
    copy_cammand=["cp",command_3,VM_ubuntu_path]  
    
    print(copy_name+"のコピー中")
    subprocess.run(copy_cammand,text=True)
    subprocess.run(command_8,text=True)
    #/usr/bin/virsh dumpxml > をsubprocess.runで使うとエラーが出るのでwithで書き込む
    with open(VM_ubuntu_path+copy_name+".xml", "w") as f:
        subprocess.run(command_5,text=True,stdout=f)
    print(copy_name+"のコピー完了")
    copy_count=copy_count+1
print("仮想マシンのバックアップ完了")

#7zipで圧縮する
#※注意点　パスはすべて文字列とするため""でくくる
#command_1 command_2 [圧縮した後の名前] [圧縮したいものの名前]
s_zip_path="/home/aweqse/copy_temp/"+today#圧縮するファイル（フォルダ）のパス
d_zip_path="/home/aweqse/copy_temp/"+today##出力先のファイル
chmod_command_2=["chmod", "777",d_zip_path+".7z"]
command_exe=["7z","a",d_zip_path,s_zip_path]
print("圧縮中")
subprocess.run(command_exe,text=True)
subprocess.run(chmod_command_2,text=True)

#nasの仮想マシンを起動する
run_command=["/usr/bin/virsh","-c", "qemu:///system","start", "NAS"]
subprocess.run(run_command,text=True)
sleep(30)

#バックアップを転送する
SSD_path="aweqse@192.168.1.103:/mnt/SSD/backup/"
scp_cammand=["scp", d_zip_path+".7z" ,SSD_path]
subprocess.run(scp_cammand,text=True)
sleep(10)

#使用済みファイルを削除する
rm_command=["rm","-r","/home/aweqse/copy_temp"]
subprocess.run(rm_command,text=True)

sleep(10)

#再起動する
subprocess.run(['sudo','-S', '/sbin/reboot'],input=password,text=True) 