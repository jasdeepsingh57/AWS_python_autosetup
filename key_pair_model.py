import boto3


def pem(pem_name):
    ec2 = boto3.resource('ec2')


    outfile = open(pem_name + ".pem", 'w')

    # call the boto ec2 function to create a key pair
    key_pair = ec2.create_key_pair(KeyName=pem_name)

    # capture the key and store it in a file
    KeyPairOut = str(key_pair.key_material)
    outfile.write(KeyPairOut)

