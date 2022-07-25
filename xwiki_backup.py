import os
from datetime import date
import paramiko
from scp import SCPClient
today = date.today()
d1 = today.strftime("%Y-%m-%d")
parent_dir = "/home/maplelabs/xwiki_backup"
path = os.path.join(parent_dir,"backup."+d1)
#os.mkdir(path)
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('<ip>', username='<username>', password='<password>')
os.system('mkdir ' + path)
with SCPClient(ssh.get_transport()) as scp:
    scp.put("/home/maplelabs/XWiki Enterprise 8.1/data",path,recursive=True)
    scp.put("/home/maplelabs/XWiki Enterprise 8.1/webapps/xwiki/WEB-INF",path,recursive=True)
