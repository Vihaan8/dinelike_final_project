#!/bin/bash
set -e

echo "=== Initializing DineLike Database ==="

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL..."
until PGPASSWORD=dinelike123 psql -h postgres -U dinelike -d dinelike -c '\q' 2>/dev/null; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 2
done

echo "✓ PostgreSQL is ready"

# Create tables
echo "Creating database schema..."
PGPASSWORD=dinelike123 psql -h postgres -U dinelike -d dinelike -f /app/sql/create_tables.sql

echo "✓ Schema created"

# Load data using Python
echo "Loading data from parquet files..."
python3 << 'PYTHON'
import pandas as pd
import psycopg2
from tqdm import tqdm
import sys

print("Connecting to database...")
conn = psycopg2.connect(
    host='postgres',
    database='dinelike',
    user='dinelike',
    password='dinelike123'
)
cursor = conn.cursor()

# Check if data already loaded
cursor.execute("SELECT COUNT(*) FROM businesses")
if cursor.fetchone()[0] > 0:
    print("⚠️  Data already exists, skipping load")
    conn.close()
    sys.exit(0)

print("\n1. Loading businesses...")
df_businesses = pd.read_parquet('/app/data/final/businesses_final.parquet')
for _, row in tqdm(df_businesses.iterrows(), total=len(df_businesses), desc="Businesses"):
    cursor.execute("""
        INSERT INTO businesses (business_id, name, address, city, state, postal_code, 
                               latitude, longitude, stars, review_count, categories)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        row['business_id'], row['name'], row.get('address'), row['city'], 
        row.get('state'), row.get('postal_code'), row.get('latitude'), 
        row.get('longitude'), row.get('stars'), row.get('review_count'), 
        row.get('categories')
    ))
conn.commit()
print(f"✓ Loaded {len(df_businesses):,} businesses")

print("\n2. Loading users with tags...")
df_users = pd.read_parquet('/app/data/final/users_final.parquet')
df_tags = pd.read_parquet('/app/data/final/reviewer_profiles_llm.parquet')
df_users = df_users.merge(df_tags[['user_id', 'tags']], on='user_id', how='left')

for _, row in tqdm(df_users.iterrows(), total=len(df_users), desc="Users"):
    cursor.execute("""
        INSERT INTO users (user_id, name, review_count, yelping_since, useful, funny, cool,
                          elite, friends, fans, average_stars, tags)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s::jsonb)
    """, (
        row['user_id'], row.get('name'), row.get('review_count'), 
        row.get('yelping_since'), row.get('useful'), row.get('funny'), 
        row.get('cool'), row.get('elite'), row.get('friends'), 
        row.get('fans'), row.get('average_stars'), row.get('tags')
    ))
conn.commit()
print(f"✓ Loaded {len(df_users):,} users")

print("\n3. Loading reviews...")
df_reviews = pd.read_parquet('/app/data/final/reviews_final.parquet')
for _, row in tqdm(df_reviews.iterrows(), total=len(df_reviews), desc="Reviews"):
    cursor.execute("""
        INSERT INTO reviews (review_id, user_id, business_id, stars, useful, funny, cool, text, date)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        row['review_id'], row['user_id'], row['business_id'], row['stars'],
        row.get('useful'), row.get('funny'), row.get('cool'), row['text'], row.get('date')
    ))
conn.commit()
print(f"✓ Loaded {len(df_reviews):,} reviews")

cursor.close()
conn.close()
print("\n✓ Database initialization complete!")
PYTHON

echo "=== Database Ready ==="
