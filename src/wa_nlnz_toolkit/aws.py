import boto3
from botocore import UNSIGNED


def list_s3_files(bucket_name, prefix=''):
    """
    Lists files in an AWS S3 bucket with an optional prefix.

    Args:
        bucket_name (str): The name of the S3 bucket.
        prefix (str): The prefix (folder path) within the bucket (optional).

    Returns:
        list: A list of object keys (file paths) in the specified bucket and prefix.
    """
    s3 = boto3.client('s3', config=boto3.session.Config(signature_version=UNSIGNED))
    file_list = []
    paginator = s3.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=bucket_name, Prefix=prefix):
        if 'Contents' in page:
            for item in page['Contents']:
                file_list.append(item['Key'])
    return file_list


def download_s3_file(bucket_name, object_key, local_path):
    """
    Downloads a file from an AWS S3 bucket.

    Args:
        bucket_name (str): The name of the S3 bucket.
        object_key (str): The key (path) of the object in the bucket.
        local_path (str): The local path to save the downloaded file.
    """
    s3 = boto3.client('s3', config=boto3.session.Config(signature_version=UNSIGNED))
    try:
        s3.download_file(bucket_name, object_key, local_path)
        print(f"Downloaded '{object_key}' from '{bucket_name}' to '{local_path}'")
    except Exception as e:
        print(f"Error downloading file: {e}")