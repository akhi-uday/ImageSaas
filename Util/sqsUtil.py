import boto3

SQS_NAME = 'inputQueue'

def get_queue_length():
    sqs = boto3.resource('sqs', region_name="us-east-1",
                           aws_secret_access_key="tM48E1xrB2Ufyf3mPM2XBPT7y6AerSip9ChcCubj",
                           aws_access_key_id="AKIAREJOAPMAGDJVE5L4")
    queue = sqs.get_queue_by_name(QueueName='inputQueue')
    print("getting queue length")
    return int(queue.attributes.get('ApproximateNumberOfMessages'))