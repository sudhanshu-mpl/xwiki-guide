import paramiko
from scp import SCPClient
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('<ip>', username='<username>', password='<password>')
with SCPClient(ssh.get_transport()) as scp:
    scp.put("<source_path>","<dest_path>",recursive=True)




