"""
Load final dataset to PostgreSQL
"""
import pandas as pd
import psycopg2
from dotenv import load_dotenv
import os
from tqdm import tqdm

load_dotenv()

# TEST MODE CHECK - Load to separate tables if enabled
TEST_MODE = os.getenv('AIRFLOW_TEST_MODE', 'false').lower() == 'true'
TABLE_SUFFIX = '_airflow_test' if TEST_MODE else ''

if TEST_MODE:
    print("=" * 60)
    print("⚠️  TEST MODE: Loading to *_airflow_test tables")
    print("⚠️  Production tables will remain unaffected")
    print("=" * 60)
    print()

# Connect to PostgreSQL
conn = psycopg2.connect(
    host='localhost',
    port=5432,
    database='dinelike',
    user='dinelike',
    password='dinelike123'
)
cursor = conn.cursor()

print("=== LOADING DATA TO POSTGRESQL ===\n")

# 1. Load businesses
print(f"Loading businesses to 'businesses{TABLE_SUFFIX}'...")
df_businesses = pd.read_parquet('data/final/businesses_final.parquet')

# Create table with suffix
cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS businesses{TABLE_SUFFIX} (
        business_id VARCHAR(50) PRIMARY KEY,
        name VARCHAR(255),
        address TEXT,
        city VARCHAR(100),
        state VARCHAR(50),
        postal_code VARCHAR(20),
        latitude FLOAT,
        longitude FLOAT,
        stars FLOAT,
        review_count INTEGER,
        categories TEXT
    )
""")

for _, row in tqdm(df_businesses.iterrows(), total=len(df_businesses), desc="Businesses"):
    cursor.execute(f"""
        INSERT INTO businesses{TABLE_SUFFIX} (business_id, name, address, city, state, postal_code, 
                               latitude, longitude, stars, review_count, categories)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (business_id) DO NOTHING
    """, (
        row['business_id'], row['name'], row.get('address'), row['city'], 
        row.get('state'), row.get('postal_code'), row.get('latitude'), 
        row.get('longitude'), row.get('stars'), row.get('review_count'), 
        row.get('categories')
    ))

conn.commit()
print(f"✓ Loaded {len(df_businesses):,} businesses")

# 2. Load users (with tags)
print(f"\nLoading users to 'users{TABLE_SUFFIX}'...")
df_users = pd.read_parquet('data/final/users_final.parquet')
df_tags = pd.read_parquet('data/final/reviewer_profiles_llm.parquet')

df_users = df_users.merge(df_tags[['user_id', 'tags']], on='user_id', how='left')

# Create table with suffix
cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS users{TABLE_SUFFIX} (
        user_id VARCHAR(50) PRIMARY KEY,
        name VARCHAR(255),
        review_count INTEGER,
        yelping_since VARCHAR(50),
        useful INTEGER,
        funny INTEGER,
        cool INTEGER,
        elite TEXT,
        friends TEXT,
        fans INTEGER,
        average_stars FLOAT,
        tags JSONB
    )
""")

for _, row in tqdm(df_users.iterrows(), total=len(df_users), desc="Users"):
    cursor.execute(f"""
        INSERT INTO users{TABLE_SUFFIX} (user_id, name, review_count, yelping_since, useful, funny, cool,
                          elite, friends, fans, average_stars, tags)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s::jsonb)
        ON CONFLICT (user_id) DO UPDATE SET tags = EXCLUDED.tags
    """, (
        row['user_id'], row.get('name'), row.get('review_count'), 
        row.get('yelping_since'), row.get('useful'), row.get('funny'), 
        row.get('cool'), row.get('elite'), row.get('friends'), 
        row.get('fans'), row.get('average_stars'), row.get('tags')
    ))

conn.commit()
print(f"✓ Loaded {len(df_users):,} users with tags")

# 3. Load reviews
print(f"\nLoading reviews to 'reviews{TABLE_SUFFIX}'...")
df_reviews = pd.read_parquet('data/final/reviews_final.parquet')

# Create table with suffix
cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS reviews{TABLE_SUFFIX} (
        review_id VARCHAR(50) PRIMARY KEY,
        user_id VARCHAR(50),
        business_id VARCHAR(50),
        stars FLOAT,
        useful INTEGER,
        funny INTEGER,
        cool INTEGER,
        text TEXT,
        date VARCHAR(50)
    )
""")

for _, row in tqdm(df_reviews.iterrows(), total=len(df_reviews), desc="Reviews"):
    cursor.execute(f"""
        INSERT INTO reviews{TABLE_SUFFIX} (review_id, user_id, business_id, stars, useful, funny, cool, text, date)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (review_id) DO NOTHING
    """, (
        row['review_id'], row['user_id'], row['business_id'], row['stars'],
        row.get('useful'), row.get('funny'), row.get('cool'), row['text'], row.get('date')
    ))

conn.commit()
print(f"✓ Loaded {len(df_reviews):,} reviews")

cursor.close()
conn.close()

print("\n" + "="*50)
print("DATABASE LOAD COMPLETE")
print("="*50)
print(f"Tables created with suffix: '{TABLE_SUFFIX}'")
print(f"Businesses: {len(df_businesses):,}")
print(f"Users: {len(df_users):,}")
print(f"Reviews: {len(df_reviews):,}")
print("="*50)
