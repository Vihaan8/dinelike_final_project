"""
Combine processed chunks into final files
"""
import boto3
import pandas as pd
from io import BytesIO
from dotenv import load_dotenv
import os
from tqdm import tqdm

load_dotenv()

s3 = boto3.client('s3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

processed_bucket = os.getenv('S3_PROCESSED_BUCKET')

print("=== COMBINING PROCESSED CHUNKS ===\n")

# List processed chunks
response = s3.list_objects_v2(Bucket=processed_bucket, Prefix='processed/')
chunks = [obj['Key'] for obj in response.get('Contents', [])]

print(f"Found {len(chunks)} processed chunks")

# Download and combine
dfs = []
for chunk_key in tqdm(chunks, desc="Loading chunks"):
    obj = s3.get_object(Bucket=processed_bucket, Key=chunk_key)
    df = pd.read_parquet(BytesIO(obj['Body'].read()))
    dfs.append(df)

df_reviews_final = pd.concat(dfs, ignore_index=True)
print(f"\nCombined into {len(df_reviews_final):,} reviews")

# Upload combined reviews
print("Uploading final reviews...")
buffer = BytesIO()
df_reviews_final.to_parquet(buffer, index=False)
buffer.seek(0)
s3.put_object(Bucket=processed_bucket, Key='reviews_final.parquet', Body=buffer.getvalue())

# Also save locally
df_reviews_final.to_parquet('data/final/reviews_final.parquet', index=False)

print(f"✓ Uploaded to s3://{processed_bucket}/reviews_final.parquet")
print(f"✓ Saved to data/final/reviews_final.parquet")
