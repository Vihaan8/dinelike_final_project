"""
Create final users and businesses datasets
"""
import boto3
import pandas as pd
from io import BytesIO
from dotenv import load_dotenv
import os

load_dotenv()

s3 = boto3.client('s3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

raw_bucket = os.getenv('S3_RAW_BUCKET')
processed_bucket = os.getenv('S3_PROCESSED_BUCKET')

print("=== CREATING FINAL DATASET ===\n")

# Load final reviews
print("Loading final reviews...")
obj = s3.get_object(Bucket=processed_bucket, Key='reviews_final.parquet')
df_reviews = pd.read_parquet(BytesIO(obj['Body'].read()))
print(f"Reviews: {len(df_reviews):,}")

# Load raw users
print("Loading users...")
obj = s3.get_object(Bucket=raw_bucket, Key='sb_users_raw.parquet')
df_users_raw = pd.read_parquet(BytesIO(obj['Body'].read()))

# Filter users to those in final reviews + 150+ threshold
final_user_ids = df_reviews['user_id'].unique()
df_users_final = df_users_raw[
    (df_users_raw['user_id'].isin(final_user_ids)) & 
    (df_users_raw['review_count'] >= 150)
].copy()
print(f"Users: {len(df_users_final):,}")

# Load raw businesses
print("Loading businesses...")
obj = s3.get_object(Bucket=raw_bucket, Key='sb_businesses_raw.parquet')
df_businesses_raw = pd.read_parquet(BytesIO(obj['Body'].read()))

# Clean businesses
df_businesses_raw['city'] = df_businesses_raw['city'].str.title().str.strip()
df_businesses_final = df_businesses_raw.copy()
print(f"Businesses: {len(df_businesses_final):,}")

# Save locally
os.makedirs('data/final', exist_ok=True)
df_users_final.to_parquet('data/final/users_final.parquet', index=False)
df_businesses_final.to_parquet('data/final/businesses_final.parquet', index=False)

# Upload to S3
print("\nUploading to S3...")
for filename, df in [
    ('users_final.parquet', df_users_final),
    ('businesses_final.parquet', df_businesses_final)
]:
    buffer = BytesIO()
    df.to_parquet(buffer, index=False)
    buffer.seek(0)
    s3.put_object(Bucket=processed_bucket, Key=filename, Body=buffer.getvalue())
    print(f"✓ Uploaded {filename}")

print("\n" + "="*50)
print("FINAL SANTA BARBARA DATASET")
print("="*50)
print(f"Location: Santa Barbara")
print(f"User Threshold: 150+ reviews")
print(f"Businesses: {len(df_businesses_final):,}")
print(f"Users: {len(df_users_final):,}")
print(f"Reviews: {len(df_reviews):,}")
print("="*50)
