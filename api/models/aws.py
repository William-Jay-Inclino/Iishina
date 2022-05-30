import boto3
from botocore.exceptions import ClientError
from gluon.contrib.appconfig import AppConfig

configuration = AppConfig(reload=False)
#Connect to client
client = boto3.client(
    's3', 
    aws_access_key_id = configuration.get('aws.access_key_id'),
    aws_secret_access_key = configuration.get('aws.secret_access_key'),
)

s3 = boto3.resource(
    's3',
    aws_access_key_id = configuration.get('aws.access_key_id'),
    aws_secret_access_key = configuration.get('aws.secret_access_key')
)

# get Bucket name in appconfig
bucket = s3.Bucket(configuration.get('aws.bucket_name'))



def list_files(key=None):
    
    s3 = boto3.resource(
        's3',
        aws_access_key_id = configuration.get('aws.access_key_id'),
        aws_secret_access_key = configuration.get('aws.secret_access_key')
    )

    # get Bucket name in appconfig
    bucket = s3.Bucket(configuration.get('aws.bucket_name'))

    objects = []

    for obj in bucket.objects.all():
        logger.info('OBJ {0}'.format(obj.key))
        objects.append(dict(key=obj.key))


    return locals()

def get_object(key):

    bucket_name = configuration.get('aws.bucket_name')

    objects = None

    try:
        objects = client.get_object(Bucket=bucket_name,Key=key)
        isExist = True
    except ClientError as e:
        isExist = False
        logging.error(e)    

    return locals()

def get_all_objects():

    try:
        s3_objects = []
        bucket_objects = bucket.objects.all()
        for obj in bucket_objects:
            s3_objects.append(obj.key)
    except ClientError as e:
        if e.response['Error']['Code'] == "404":
            isExist = False
        else:
            isExist = False
    return s3_objects


def upload_file(file_name, key=None):

    # If key was not specified, use file_name
    if key is None:
        key = file_name

    bucket = configuration.get('aws.bucket_name')

    client = boto3.client(
        's3', 
        aws_access_key_id = configuration.get('aws.access_key_id'),
        aws_secret_access_key = configuration.get('aws.secret_access_key'),
    )   

    try:
        client.upload_fileobj(file_name, bucket, key)
        # client.upload_file(file_name, bucket, key)
        isUploaded = True
    except ClientError as e:
        logging.error(e)    
        isUploaded = False
    
    return locals()

def remove_file(key):
    bucket = configuration.get('aws.bucket_name')

    # s3 = boto3.resource(
    s3 = boto3.client(
        's3',
        aws_access_key_id = configuration.get('aws.access_key_id'),
        aws_secret_access_key = configuration.get('aws.secret_access_key')
    )  

    # s3_bucket = s3.Bucket(bucket)
    result = get_object(key)
    logger.info('isExist {0}'.format(result['isExist']))

    if result['isExist'] == True:
        try:
            objects = s3.delete_object(Bucket=bucket,Key=key)
            isDeleted = True
        except ClientError as e:
            logging.error(e)    
            isDeleted = False
    else:
        isExist = False
        isDeleted = False

    
    return locals()

def create_folder(key):
    bucket = configuration.get('aws.bucket_name')

    # s3 = boto3.resource(
    s3 = boto3.client(
        's3',
        aws_access_key_id = configuration.get('aws.access_key_id'),
        aws_secret_access_key = configuration.get('aws.secret_access_key')
    )  

    try:
        objects = s3.put_object(Bucket=bucket,Body='',Key=key)
        isCreated = True
    except ClientError as e:
        logging.error(e)    
        isCreated = False
   

    
    return locals()


def create_presigned_url(key):
    bucket = configuration.get('aws.bucket_name')
    expiry = configuration.get('aws.expiry')

    s3 = boto3.client(
        's3',
        aws_access_key_id = configuration.get('aws.access_key_id'),
        aws_secret_access_key = configuration.get('aws.secret_access_key')
    )  

    result = get_object(key)
    logger.info('isExist {0}'.format(result['isExist']))

    if result['isExist'] == True:
        try:
            url = s3.generate_presigned_url(    'get_object', 
                                                Params={
                                                    'Bucket': bucket,
                                                    'Key' : key,         
                                                },
                                                ExpiresIn= expiry
                                            )
            urlCreated = True
        except ClientError as e:
            logging.error(e)    
            urlCreated = False
    else:
        isExist = False
        urlCreated = False

    
    return locals()



