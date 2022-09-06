import boto3
import time
ec2 = boto3.client('ec2')
file = open('server','w')
def get_state_info():
    ec2 = boto3.resource('ec2')
    running_instances = ec2.instances.filter(Filters=[{
    'Name': 'instance-state-name',
    'Values': ['running','stopped']}])
    return running_instances

def public_ip_save():
    running_instances = get_state_info()
    for instance in running_instances:
        for tag in instance.tags:
            if 'Name'in tag['Key'] and tag['Value']=='ansible-ubuntu':
                print("public ip of ",tag['Value'],":-", end="") 
                data ="server1 ansible_host="+instance.public_ip_address+" ansible_user=ubuntu ansible_ssh_private_key_file=./ansible_key.pem ansble_connection=ssh"
                file.write(data)
                file.close()
                print(instance.public_ip_address)

def public_ip_addr():
    running_instances = get_state_info()
    for instance in running_instances:
        for tag in instance.tags:
            if 'Name'in tag['Key'] and tag['Value']=='ansible-ubuntu' and instance.state['Name'] == 'stopped':
                start_ec2_instance(instance.id)
    public_ip_save()

def start_ec2_instance(id):
    try:
        print("starting a EC2 instance.....\n")
        ec2.start_instances(InstanceIds=[id])
        time.sleep(30)
        print("instance started successfully\n")
        return 1
    except Exception as e:
        print(e)

public_ip_addr()