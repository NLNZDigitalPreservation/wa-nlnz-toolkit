import boto3
import pandas as pd
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


def load_cdx_file_from_s3(bucket_name: str, cdx_file: str) -> pd.DataFrame:
    """
    Loads a standard CDX file from an AWS S3 bucket into a pandas DataFrame.

    Args:
        bucket_name (str): The name of the S3 bucket.
        cdx_file (str): The key (path) of the CDX file in the bucket.

    Returns:
        pd.DataFrame: A DataFrame containing the CDX data.
    """
    
    cdx_s3_uri = f"s3://{bucket_name}/{cdx_file}"
    df_cdx = pd.read_csv(cdx_s3_uri, sep=" ", skiprows=0)
    # ignore last two columns
    df_cdx = df_cdx.iloc[:, :-2]
    df_cdx.columns = ['N', 'b', 'a', 'm', 's', 'k', 'r', 'M', 'S', 'V', 'g']

    return df_cdx