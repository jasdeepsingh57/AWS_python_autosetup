import subprocess
import os

p = subprocess.Popen(["ssh-keygen"],
                     stdin=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf8')
stdout, stderr = p.communicate(input='\nempty for no passphrase\nempty for no passphrase\n')
os.system('eval `ssh-agent')
os.system('ssh-add ~/.ssh/id_rsa.pub')
p = os.system('cat ~/.ssh/id_rsa.pub')
print(p)
