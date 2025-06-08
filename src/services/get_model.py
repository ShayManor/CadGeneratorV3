import io

import boto3

from src.helpers.constants import BUCKET


def get_model_from_bucket(key: str):
    s3 = boto3.client('s3', region_name="us-east-2")
    response = s3.get_object(Bucket=BUCKET, Key=key + "_stl")
    data = response['Body'].read()
    buf = io.BytesIO(data)
    buf.seek(0)
    return buf
