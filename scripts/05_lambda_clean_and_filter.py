"""
Invoke Lambda to process each chunk
"""
import boto3
import json
from dotenv import load_dotenv
import os
from tqdm import tqdm

load_dotenv()

lambda_client = boto3.client('lambda',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

s3 = boto3.client('s3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

raw_bucket = os.getenv('S3_RAW_BUCKET')
processed_bucket = os.getenv('S3_PROCESSED_BUCKET')

print("Listing chunks...")
response = s3.list_objects_v2(Bucket=raw_bucket, Prefix='chunks/')
chunks = [obj['Key'] for obj in response.get('Contents', [])]

print(f"Found {len(chunks)} chunks\n")

for chunk_key in tqdm(chunks, desc="Processing"):
    payload = {
        'raw_bucket': raw_bucket,
        'processed_bucket': processed_bucket,
        'chunk_key': chunk_key,
        'user_threshold': 150
    }
    
    response = lambda_client.invoke(
        FunctionName='dinelike-clean-data',
        InvocationType='RequestResponse',
        Payload=json.dumps(payload)
    )
    
    result = json.loads(response['Payload'].read())
    if result.get('statusCode') != 200:
        print(f"\nError: {chunk_key}: {result}")

print("\n✓ All chunks processed")
