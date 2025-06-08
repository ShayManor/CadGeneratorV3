from typing import Tuple
from urllib.parse import quote_plus

import boto3

from src.helpers.constants import BUCKET


def upload(key: str, file_path_1: str) -> Tuple[str, str]:
    file_path_2: str = file_path_1.replace('scad', 'stl')
    s3 = boto3.client('s3', region_name="us-east-2")
    key1 = key + "_scad"
    key2 = key + "_stl"
    s3.upload_file(file_path_1, BUCKET, key1)
    s3.upload_file(file_path_2, BUCKET, key2)
    base_url = f"https://{BUCKET}.s3.us-east-2.amazonaws.com"
    url1 = f"{base_url}/{quote_plus(key1)}"
    url2 = f"{base_url}/{quote_plus(key2)}"
    return url1, url2


