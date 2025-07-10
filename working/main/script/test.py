import subprocess

password="Fujieda1217"
subprocess.run(['sudo','-S', '/sbin/reboot'],input=password,text=True) 