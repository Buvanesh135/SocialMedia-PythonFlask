import boto3

from config import Config


def send_queue_message(*args, **kwargs):
    pass
def upload_to_aws(user_file, bucket_name, s3_file_name, ContentType, Metadata={}):
    try:
        # s3 = boto3.resource(
        #     's3',
        #     #region_name=Config.AWS_REGION_S3,
        #     aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
        #     aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY
        # )
        # s3.Object(bucket_name, s3_file_name).put(Body=user_file, ACL='public-read', Metadata=Metadata)
        client = boto3.client('s3',
                              region_name=Config.AWS_REGION_S3,
                              aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY
                              )

        client.put_object(Bucket=bucket_name, Key=s3_file_name, Body=user_file, ACL='public-read',
                          ContentType=ContentType)
        file_path = f"https://{bucket_name}.s3.amazonaws.com/{s3_file_name}"
        print("Upload Successful, file path", file_path)
        return True, file_path
    except Exception as e:
        print("S3 bucket exception", e)
        return False, ""


def generate_presigned_url(bucket_name, object_key, expiry=int(Config.AWS_S3_EXPIRY)):
    client = boto3.client("s3", region_name=Config.AWS_REGION_S3,
                          aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
                          )
    try:
        response = client.generate_presigned_url('get_object',
                                                 Params={'Bucket': bucket_name, 'Key': object_key},
                                                 ExpiresIn=expiry)
        print(response, "signed url================")
        return response
    except Exception as e:
        print("generate_presigned_url", e)
        return None


def delete_s3_file(bucket_name, s3_file_name):
    try:
        s3 = boto3.resource(
            's3',
            region_name=Config.AWS_REGION_S3,
            aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY
        )
        s3.Object(bucket_name, s3_file_name).delete()
        return True
    except Exception as e:
        print("delete_s3_file exception", e)
        return False


def get_metadata(bucket_name, file_name):
    client = boto3.client("s3", region_name=Config.AWS_REGION_S3,
                          aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
                          )
    try:

        response = client.head_object(Bucket=bucket_name, Key=file_name)
        return response["Metadata"]
    except Exception as e:
        print("get_metadata", e)
        return None


def upload_to_aws_without_contenttype(user_file, bucket_name, s3_file_name):
    try:
        # s3 = boto3.resource(
        #     's3',
        #     #region_name=Config.AWS_REGION_S3,
        #     aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
        #     aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY
        # )
        # s3.Object(bucket_name, s3_file_name).put(Body=user_file, ACL='public-read', Metadata=Metadata)
        client = boto3.client('s3',
                              region_name=Config.AWS_REGION_S3,
                              aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY
                              )

        client.put_object(Bucket=bucket_name, Key=s3_file_name, Body=user_file
                         )
        file_path = f"https://{bucket_name}.s3.amazonaws.com/{s3_file_name}"
        print("Upload Successful, file path", file_path)
        return True, file_path
    except Exception as e:
        print("S3 bucket exception", e)
        return False, ""
