"""
Upload chunks to S3
"""
import boto3
from dotenv import load_dotenv
import os
from tqdm import tqdm

load_dotenv()

s3 = boto3.client('s3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

raw_bucket = os.getenv('S3_RAW_BUCKET')

chunk_files = [f for f in os.listdir('data/chunks') if f.endswith('.parquet')]

for chunk_file in tqdm(chunk_files, desc="Uploading"):
    s3.upload_file(f'data/chunks/{chunk_file}', raw_bucket, f'chunks/{chunk_file}')

print(f"\n✓ Uploaded {len(chunk_files)} chunks")
