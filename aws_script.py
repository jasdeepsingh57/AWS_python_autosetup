import boto3
import time
import os
from boto.manage.cmdshell import sshclient_from_instance
import boto.ec2
from key_pair_model import pem
from git_txt_write import git_write

os.system('aws configure')   #PLEASE CHECK THE AWS CREDENTIAL

pem_name = input("ENTER THE NAME OF PEM FILE (don't include .pem at the end) :\n")
ec2 = boto3.resource('ec2')
pem(pem_name)


ImageIds = [{'Ubuntu18':"ami-0bbe6b35405ecebdb"}, {"Ubuntu16":"ami-076e276d85f524150"},
          {"Amazon-Linux2":"ami-032509850cf9ee54e"}, {"Redhat-Linux7.6":"ami-036affea69a1101c9"}]
ImageId_input = int(input("SELECT YOUR MACHINE\n1. Ubuntu18 \n2. Ubuntu16  \n3. Amazon-Linux2 \n4. Redhat-Linux7.6  \n"))
ImageId = list(ImageIds[ImageId_input-1].values())[0]
if ImageId_input > 4:
    print("Please Enter Correct Input:\n")
    ImageId_input = int(input("SELECT YOUR MACHINE\n1. Ubuntu18 \n2. Ubuntu16  \n3. Amazon-Linux2 \n4. Redhat-Linux7.6  \n"))
InstanceTypes = ['t2.micro', 't2.small', 't2.medium', 't2.large']
InstanceTypeInput = int(input("1. t2.micro \n2. t2.small \n3. t2.medium  \n4. t2.large \n"))
InstanceType = InstanceTypes[InstanceTypeInput-1]


instances = ec2.create_instances(
     ImageId=ImageId,
     MinCount=1,
     MaxCount=1,
     InstanceType=InstanceType,
     KeyName=pem_name,
     SecurityGroupIds=[
            'sg-0a0258e39126bcc48',
        ],
 )
instance_id = (instances[0].id)
print("WAIT SERVER IS GETTING STARTED")
time.sleep(100)

get_instance = ec2.instances.filter(InstanceIds=[instance_id])
for i in get_instance:
    IP = i.public_ip_address

pem_file_location = input("Please ENTER the .pem file location (don't include name of file)\n")

conn = boto.ec2.connect_to_region('us-west-2')

instance = conn.get_all_instances([instance_id])[0].instances[0]
os.system('chmod 400 %s/%s.pem' % (pem_file_location, pem_name))
server_localuser = input("ENTER THE USER FOR SERVER (FOR EXAMPLE : type 'ubuntu' for UBUNTU machine)\n")
Python_version = input("ENTER THE PYTHON VERSION FOR VIRTUALENV .FOR EXAMPLE: '2' or '3' \n")
Virtualenv_name = input("ENTER VIRTAULENV NAME\n")

ssh_client = sshclient_from_instance(instance,
                                     pem_file_location + "/" + pem_name + ".pem",
                                     user_name=server_localuser)

status, stdout, stderr = ssh_client.run('sudo apt update && sudo apt install -y python3-pip && sudo apt install -y virtualenv && virtualenv -p python%s %s' %
                                        (Python_version, Virtualenv_name))
status, stdout, stderr = ssh_client.run("source %s/bin/activate && sudo apt install -y nginx && pip install gunicorn"%(Virtualenv_name))


os.system('scp -i %s/%s.pem %s/ssh-git.py ubuntu@%s:/home/ubuntu' %
          (pem_file_location, pem_name, pem_file_location, IP))

status, stdout, stderr = ssh_client.run("python3 ssh-git.py")
print("OUTPUT : \n", stdout)
print("ERROR MESSAGE :\n", stderr)
message = input("PLEASE COPY THE SSH AND PASTE IT TO YOUR GIT ACCOUNT AND PLEASE 'ENTER' \n")
status, stdout, stderr = ssh_client.run("rm ssh-git.py")
'''
git_link = input("ENTER THE GIT CLONE URL HERE FROM PROJECT REPO\n")

git_write(git_link)
os.system('scp -i %s/%s.pem %s/git.txt ubuntu@%s:/home/ubuntu' %
          (pem_file_location, pem_name, pem_file_location, IP))
os.system('scp -i %s/%s.pem %s/git_ssh_pull.py ubuntu@%s:/home/ubuntu' %
          (pem_file_location, pem_name, pem_file_location, IP))
'''

print("Process Done ,you can connect server using required pem file with IP: %s \n" % IP)
















