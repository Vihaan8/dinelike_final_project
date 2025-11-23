"""
Upload final processed data (with LLM tags) to S3
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

processed_bucket = os.getenv('S3_PROCESSED_BUCKET')

print("=== UPLOADING FINAL PROCESSED DATA TO S3 ===\n")

files = [
    ('data/final/businesses_final.parquet', 'final/businesses_final.parquet'),
    ('data/final/users_final.parquet', 'final/users_final.parquet'),
    ('data/final/reviews_final.parquet', 'final/reviews_final.parquet'),
    ('data/final/reviewer_profiles_llm.parquet', 'final/reviewer_profiles_llm.parquet')
]

for local_path, s3_key in files:
    print(f"Uploading {s3_key}...")
    s3.upload_file(local_path, processed_bucket, s3_key)
    file_size = os.path.getsize(local_path) / (1024 * 1024)
    print(f"  ✓ {file_size:.1f} MB uploaded")

print("\n" + "="*50)
print("FINAL S3 STRUCTURE")
print("="*50)
print(f"s3://{processed_bucket}/")
print("  └── final/")
print("      ├── businesses_final.parquet (3,829 businesses)")
print("      ├── users_final.parquet (10,263 users)")
print("      ├── reviews_final.parquet (42,687 reviews)")
print("      └── reviewer_profiles_llm.parquet (10,263 tagged profiles)")
print("="*50)
