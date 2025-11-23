"""
Extract Santa Barbara data from raw Yelp dataset
Output: Unfiltered Santa Barbara businesses, reviews, users
"""
import pandas as pd
import json
from tqdm import tqdm
import os

print("=== STEP 1: FILTER SANTA BARBARA DATA ===\n")

os.makedirs('data/santa_barbara', exist_ok=True)

# Load raw Yelp data
print("Loading Yelp business data...")
businesses = []
with open('data/raw/yelp_academic_dataset_business.json', 'r') as f:
    for line in tqdm(f):
        businesses.append(json.loads(line))
df_businesses = pd.DataFrame(businesses)

# Filter Santa Barbara businesses
print("\nFiltering Santa Barbara businesses...")
df_sb_businesses = df_businesses[df_businesses['city'] == 'Santa Barbara'].copy()
print(f"Santa Barbara businesses: {len(df_sb_businesses):,}")

sb_business_ids = set(df_sb_businesses['business_id'])

# Load and filter reviews
print("\nLoading and filtering reviews...")
reviews = []
with open('data/raw/yelp_academic_dataset_review.json', 'r') as f:
    for line in tqdm(f):
        review = json.loads(line)
        if review['business_id'] in sb_business_ids:
            reviews.append(review)
df_sb_reviews = pd.DataFrame(reviews)
print(f"Santa Barbara reviews: {len(df_sb_reviews):,}")

# Get user IDs from Santa Barbara reviews
sb_user_ids = set(df_sb_reviews['user_id'])

# Load and filter users
print("\nLoading and filtering users...")
users = []
with open('data/raw/yelp_academic_dataset_user.json', 'r') as f:
    for line in tqdm(f):
        user = json.loads(line)
        if user['user_id'] in sb_user_ids:
            users.append(user)
df_sb_users = pd.DataFrame(users)
print(f"Santa Barbara users: {len(df_sb_users):,}")

# Save to parquet
print("\nSaving to parquet...")
df_sb_businesses.to_parquet('data/santa_barbara/sb_businesses_raw.parquet', index=False)
df_sb_reviews.to_parquet('data/santa_barbara/sb_reviews_raw.parquet', index=False)
df_sb_users.to_parquet('data/santa_barbara/sb_users_raw.parquet', index=False)

print("\n" + "="*50)
print("SANTA BARBARA RAW DATA EXTRACTED")
print("="*50)
print(f"Businesses: {len(df_sb_businesses):,}")
print(f"Reviews: {len(df_sb_reviews):,}")
print(f"Users: {len(df_sb_users):,}")
print("="*50)
