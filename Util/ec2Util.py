import boto3
from ec2_metadata import ec2_metadata

INSTANCE_STATE = "Instance_State/{}"


def update_instance_state(instanceid, value):
    key = INSTANCE_STATE.format(instanceid)
    s3_res = boto3.client('s3', region_name="us-east-1",
                          aws_secret_access_key="A/7+WWgcy/JKJXTRIqOAAEgoUuc9JAjUpniFV1mu",
                          aws_access_key_id="AKIAREJOAPMAH77ZCSUY")
    s3_res.put_object(Body=str(value), Bucket='app-instance-input', Key=key)


def get_my_instance_id():
    return ec2_metadata.instance_id
    # print(myInstanceId)


def get_instance_state(instanceid):
    s3 = boto3.resource('s3', region_name="us-east-1",
                          aws_secret_access_key="A/7+WWgcy/JKJXTRIqOAAEgoUuc9JAjUpniFV1mu",
                          aws_access_key_id="AKIAREJOAPMAH77ZCSUY")
    key = INSTANCE_STATE.format(instanceid)
    obj = s3.Object('app-instance-input', key)
    body = obj.get()['Body'].read()
    return int(body)

#def get_running_instances():



def start_instance(instanceid):
    print('starting new instance -', instanceid)
    try:
        ec2 = boto3.client('ec2', region_name="us-east-1",
                           aws_secret_access_key="A/7+WWgcy/JKJXTRIqOAAEgoUuc9JAjUpniFV1mu",
                           aws_access_key_id="AKIAREJOAPMAH77ZCSUY")
        response = ec2.start_instances(InstanceIds=[instanceid])
        print(response)

    except Exception as e:
        print(e)

# def create_instance(client):
#     try:
#         instances = client.run_instances(
#             ImageId="ami-0bb1040fdb5a076bc",
#             MinCount=1,
#             MaxCount=1,
#             InstanceType="t2.micro",
#             KeyName="app"
#         )
#         print("Instance successfully created")
#     except Exception as e:
#         print(e)


def stop_instance(instanceid):
    try:
        ec2 = boto3.client('ec2', region_name="us-east-1",
                           aws_secret_access_key="A/7+WWgcy/JKJXTRIqOAAEgoUuc9JAjUpniFV1mu",
                           aws_access_key_id="AKIAREJOAPMAH77ZCSUY")
        response = ec2.stop_instances(InstanceIds=[instanceid], DryRun=False)
        print(response)
    except Exception as e:
        print(e)
