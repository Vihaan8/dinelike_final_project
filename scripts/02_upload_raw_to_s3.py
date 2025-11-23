"""
Upload Santa Barbara raw data to S3
"""
import boto3
from dotenv import load_dotenv
import os

load_dotenv()

s3 = boto3.client('s3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

raw_bucket = os.getenv('S3_RAW_BUCKET')

files = [
    'sb_businesses_raw.parquet',
    'sb_reviews_raw.parquet',
    'sb_users_raw.parquet'
]

for file in files:
    print(f"Uploading {file}...")
    s3.upload_file(f'data/santa_barbara/{file}', raw_bucket, file)
    print(f"✓ Uploaded to s3://{raw_bucket}/{file}")

print("\n✓ All raw data uploaded to S3")
