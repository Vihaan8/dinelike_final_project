"""
Split reviews into chunks for Lambda processing
"""
import pandas as pd
import os

print("Chunking Santa Barbara reviews...")

df_reviews = pd.read_parquet('data/santa_barbara/sb_reviews_raw.parquet')
chunk_size = 10000  # Smaller chunks for Santa Barbara

os.makedirs('data/chunks', exist_ok=True)

num_chunks = len(df_reviews) // chunk_size + 1

for i in range(num_chunks):
    start = i * chunk_size
    end = start + chunk_size
    chunk = df_reviews[start:end]
    chunk.to_parquet(f'data/chunks/reviews_chunk_{i:03d}.parquet', index=False)
    print(f"Created chunk {i+1}/{num_chunks}: {len(chunk)} reviews")

print(f"\n✓ Created {num_chunks} chunks")
