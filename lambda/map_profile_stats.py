import json
import boto3
import pandas as pd
from io import BytesIO
from collections import Counter

s3 = boto3.client('s3')

def lambda_handler(event, context):
    bucket = event['bucket']
    chunk_key = event['chunk_key']
    output_bucket = event['output_bucket']
    
    print(f"Processing {chunk_key}")
    
    # Download chunk
    obj = s3.get_object(Bucket=bucket, Key=chunk_key)
    df = pd.read_parquet(BytesIO(obj['Body'].read()))
    
    print(f"Loaded {len(df)} reviews")
    
    # Group by user_id and calculate partial stats
    user_stats = {}
    
    for user_id in df['user_id'].unique():
        user_reviews = df[df['user_id'] == user_id]
        
        # Aggregate text for word counting
        all_text = ' '.join(user_reviews['text'].str.lower())
        words = [w for w in all_text.split() if len(w) > 4]
        word_counts = dict(Counter(words))
        
        user_stats[user_id] = {
            'review_count': len(user_reviews),
            'sum_ratings': int(user_reviews['stars'].sum()),
            'sum_text_lengths': int(user_reviews['text'].str.len().sum()),
            'word_counts': word_counts
        }
    
    print(f"Computed stats for {len(user_stats)} users")
    
    # Upload partial stats
    chunk_name = chunk_key.split('/')[-1].replace('.parquet', '')
    output_key = f"intermediate/partial_stats/{chunk_name}_stats.json"
    
    s3.put_object(
        Bucket=output_bucket,
        Key=output_key,
        Body=json.dumps(user_stats)
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps(f'Processed {len(user_stats)} users')
    }
