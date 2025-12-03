"""
Clean Santa Barbara data + filter to 150+ review users
"""
import json
import boto3
import pandas as pd
from io import BytesIO

s3 = boto3.client('s3')

def lambda_handler(event, context):
    raw_bucket = event['raw_bucket']
    processed_bucket = event['processed_bucket']
    chunk_key = event['chunk_key']
    user_threshold = event.get('user_threshold', 150)
    
    print(f"Processing: {chunk_key}")
    
    # Download chunk
    obj = s3.get_object(Bucket=raw_bucket, Key=chunk_key)
    df = pd.read_parquet(BytesIO(obj['Body'].read()))
    print(f"Loaded {len(df)} reviews")
    
    # Download user list (to filter by review count)
    users_obj = s3.get_object(Bucket=raw_bucket, Key='sb_users_raw.parquet')
    df_users = pd.read_parquet(BytesIO(users_obj['Body'].read()))
    
    # Filter to users with threshold+ reviews
    power_users = df_users[df_users['review_count'] >= user_threshold]['user_id'].tolist()
    print(f"Power users (150+): {len(power_users)}")
    
    # Clean reviews
    df = df.drop_duplicates(subset=['review_id'])
    df = df[df['text'].notna()]
    df = df[df['text'].str.strip() != '']
    df = df[df['stars'].between(1, 5)]
    
    # Filter to power users
    df = df[df['user_id'].isin(power_users)]
    
    print(f"Cleaned to {len(df)} reviews")
    
    # Upload
    output_key = chunk_key.replace('chunks/', 'processed/').replace('_raw', '_clean')
    buffer = BytesIO()
    df.to_parquet(buffer, index=False)
    buffer.seek(0)
    
    s3.put_object(Bucket=processed_bucket, Key=output_key, Body=buffer.getvalue())
    
    return {
        'statusCode': 200,
        'body': json.dumps(f'Processed {len(df)} reviews')
    }
