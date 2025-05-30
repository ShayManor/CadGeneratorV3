from uuid import uuid4

import boto3
from dotenv import load_dotenv

load_dotenv()


def upload_model(path):
    s3_client = boto3.client('s3')
    bucket_name = 'scad-models'
    object_key = f'{uuid4()}{path.split('/')[-1]}'
    try:
        s3_client.upload_file(path, bucket_name, object_key)
        print(f"File '{path}' uploaded to '{bucket_name}/{object_key}' successfully.")
        return object_key
    except Exception as e:
        print(f"Error uploading file: {e}")


def download_model(key):
    s3_client = boto3.client('s3')
    return s3_client.get_object(Bucket='scad-models', Key=key)
