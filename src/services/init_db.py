"""Initialize database with parquet data."""
import pandas as pd
import psycopg2
import os
import sys


def main():
    print("=== Initializing DineLike Database ===")
    
    # Connect to database
    print("Connecting to database...")
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST', 'postgres'),
        database=os.getenv('DB_NAME', 'dinelike'),
        user=os.getenv('DB_USER', 'dinelike'),
        password=os.getenv('DB_PASSWORD', 'dinelike123')
    )
    cursor = conn.cursor()
    
    # Check if data already loaded
    cursor.execute("SELECT COUNT(*) FROM businesses")
    if cursor.fetchone()[0] > 0:
        print("⚠️  Data already exists, skipping load")
        conn.close()
        sys.exit(0)
    
    print("\n1. Loading businesses...")
    df_businesses = pd.read_parquet('data/final/businesses_final.parquet')
    for _, row in df_businesses.iterrows():
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
    df_users = pd.read_parquet('data/final/users_final.parquet')
    df_tags = pd.read_parquet('data/final/reviewer_profiles_llm.parquet')
    df_users = df_users.merge(df_tags[['user_id', 'tags']], on='user_id', how='left')
    
    for _, row in df_users.iterrows():
        cursor.execute("""
            INSERT INTO users (user_id, name, review_count, yelping_since, useful, funny, cool,
                              elite, friends, fans, average_stars, tags)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s::jsonb)
        """, (
            row['user_id'], row.get('name'), row.get('review_count'), 
            str(row.get('yelping_since')), row.get('useful'), row.get('funny'), 
            row.get('cool'), row.get('elite'), row.get('friends'), 
            row.get('fans'), row.get('average_stars'), row.get('tags')
        ))
    conn.commit()
    print(f"✓ Loaded {len(df_users):,} users")
    
    print("\n3. Loading reviews...")
    df_reviews = pd.read_parquet('data/final/reviews_final.parquet')
    for _, row in df_reviews.iterrows():
        cursor.execute("""
            INSERT INTO reviews (review_id, user_id, business_id, stars, useful, funny, cool, text, date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            row['review_id'], row['user_id'], row['business_id'], row['stars'],
            row.get('useful'), row.get('funny'), row.get('cool'), row['text'], str(row.get('date'))
        ))
    conn.commit()
    print(f"✓ Loaded {len(df_reviews):,} reviews")
    
    cursor.close()
    conn.close()
    print("\n✓ Database initialization complete!")


if __name__ == "__main__":
    main()
