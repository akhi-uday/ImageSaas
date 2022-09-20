import boto3
from botocore.exceptions import ClientError
from ec2_metadata import ec2_metadata
import Util.sqsUtil as sqs
import Util.ec2Util as ec2
from Util.ec2Util import get_my_instance_id
import time

instanceIds=[]
instanceCount=0
myInstanceId=''
max_count=20

def controller():
    que_length = sqs.get_queue_length()
    print('queue length is ', que_length)

    if que_length == 0:
        print('queue is empty, shutting all the instances')
        shut_all_instances()
        return

    upcount = get_total_ec2_upcount()

    if upcount < instanceCount:
        upscale(que_length, upcount)

    # Case-3 -> check if downscale is required
    if upcount == instanceCount:
        if que_length < upcount:

             downscale(que_length,upcount)


def shut_all_instances():
    for instance in instanceIds:
            ec2.update_instance_state(instance,0)

def upscale(que_length,upcount):
    diff=min(que_length,instanceCount-upcount)
    for i in range(instanceCount):
        if(diff==0):
            break
        print(instanceIds)
        print('\n upscaling, adding ', diff,' instances and instance id is ',instanceIds[i],'\n\n\n\n')
        temp=ec2.get_instance_state(instanceIds[i])
        print('instance:',instanceIds[i],'  state- ',temp)
        if temp == 0:
            instance=instanceIds[i]
            ec2.start_instance(instance)                   # starting instance
            ec2.update_instance_state(instance,1)          # updating the state in s3
            diff=diff-1


def downscale(que_length,upcount):
    for i in range(que_length,upcount+1):
        instance=instanceIds[i]
        ec2.stop_instance(instance)
        ec2.update_instance_state(instance,0)
        return


def get_total_ec2_upcount():
    upcount=0;
    for instance in instanceIds:
        temp=ec2.get_instance_state(instance)
        upcount=upcount+temp
    print("total number of instances up ",upcount)
    return upcount


def get_instance_ids():
    ec2 = boto3.resource('ec2',region_name="us-east-1",aws_secret_access_key="A/7+WWgcy/JKJXTRIqOAAEgoUuc9JAjUpniFV1mu",aws_access_key_id="AKIAREJOAPMAH77ZCSUY")
    for instance in ec2.instances.all():
        #print (instance.id)
        #print(str(instance.state))
        myinstanceid=get_my_instance_id()
        if myinstanceid!=instance.id and instance.state['Name']!='terminated':
            instanceIds.append(instance.id)
            print(instance.state)


if __name__ == '__main__':
    get_instance_ids()
    instanceCount = len(instanceIds)
    print(instanceCount)
    print(instanceIds)

    # initialize the state of all the ec2 instances to off in s3
    for instance in instanceIds:
        ec2.update_instance_state(instance, 0)
    #    time.sleep(60)
    while True:
        controller()
        time.sleep(30)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
