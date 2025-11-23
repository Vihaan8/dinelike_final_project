"""
Strict LLM tagging with validated JSON schema
"""
import pandas as pd
import json
from openai import OpenAI
from dotenv import load_dotenv
import os
from tqdm import tqdm
import time
from concurrent.futures import ThreadPoolExecutor
import shutil

load_dotenv()

# AIRFLOW MODE CHECK - Skip LLM tagging if enabled
AIRFLOW_MODE = os.getenv('AIRFLOW_MODE', 'false').lower() == 'true'

if AIRFLOW_MODE:
    print("=" * 60)
    print("⚠️  AIRFLOW MODE: Skipping LLM tagging")
    print("⚠️  Using existing reviewer_profiles_llm.parquet")
    print("=" * 60)
    
    # Just copy existing profiles
    os.makedirs('data/checkpoints', exist_ok=True)
    shutil.copy(
        'data/final/reviewer_profiles_llm.parquet',
        'data/checkpoints/profiles_airflow.parquet'
    )
    
    print("✓ Copied existing profiles to checkpoints/")
    print("✓ Skipping expensive LLM API calls")
    exit(0)

# Continue with normal LLM tagging if not in Airflow mode
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

print("Loading data...")
df_reviews = pd.read_parquet('data/final/reviews_final.parquet')
df_users = pd.read_parquet('data/final/users_final.parquet')

print(f"Users to process: {len(df_users):,}")
print("Using gpt-4o-mini with STRICT validation")
print(f"Estimated cost: ${len(df_users) * 0.00025:.2f}\n")

os.makedirs('data/checkpoints', exist_ok=True)

STRICT_PROMPT_TEMPLATE = """Analyze restaurant reviews and extract preferences. Follow rules EXACTLY.

Reviews: {reviews_text}

CRITICAL RULES:
1. ALL arrays must be arrays [...], NEVER strings
2. Use ONLY the exact values listed - no variations
3. cuisine_preferences = actual cuisine types ONLY (NOT "pizza", "ice cream", "coffee", "wine")
4. meal_timing must be array even if one value: ["dinner"] not "dinner"

Return EXACTLY this JSON structure:
{{
  "priorities": [1-2 values ONLY from: "food_quality", "atmosphere", "service", "value"],
  "dining_style": [1-2 values ONLY from: "casual", "upscale", "cozy", "lively"],
  "meal_timing": [ARRAY of values from: "breakfast", "brunch", "lunch", "dinner"],
  "cuisine_preferences": [ARRAY of cuisine types like "italian", "mexican", "thai", "japanese" - NOT drinks/desserts],
  "adventure_level": EXACTLY ONE OF: "traditional", "moderate", "adventurous", "very_adventurous",
  "price_sensitivity": EXACTLY ONE OF: "budget", "moderate", "upscale", "fine_dining"
}}

EXAMPLES OF CORRECT OUTPUT:
{{
  "priorities": ["food_quality", "atmosphere"],
  "dining_style": ["casual", "cozy"],
  "meal_timing": ["dinner", "lunch"],
  "cuisine_preferences": ["italian", "mexican"],
  "adventure_level": "moderate",
  "price_sensitivity": "moderate"
}}

EXAMPLES OF WRONG OUTPUT (DO NOT DO THIS):
- meal_timing: "dinner" ❌ (should be ["dinner"])
- priorities: ["quality"] ❌ (should be ["food_quality"])
- dining_style: ["intimate"] ❌ (should be ["cozy"])
- cuisine_preferences: ["pizza", "wine"] ❌ (should be actual cuisines)

Return ONLY the JSON object, no markdown, no explanation."""

def extract_tags(user_id, user_reviews, user_avg_rating):
    """Extract tags with strict validation"""
    
    if len(user_reviews) == 0:
        return get_default_tags()
    
    combined_text = " ".join(user_reviews['text'].head(20))[:3000]
    
    prompt = STRICT_PROMPT_TEMPLATE.format(reviews_text=combined_text)
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=300,
            response_format={"type": "json_object"}
        )
        
        response_text = response.choices[0].message.content.strip()
        tags = json.loads(response_text)
        
        tags = validate_tags(tags, user_reviews, user_avg_rating)
        return tags
        
    except Exception as e:
        print(f"\nError for {user_id}: {e}")
        return get_default_tags()

def validate_tags(tags, user_reviews, user_avg_rating):
    """Strict validation"""
    
    ALLOWED = {
        'priorities': ['food_quality', 'atmosphere', 'service', 'value'],
        'dining_style': ['casual', 'upscale', 'cozy', 'lively'],
        'meal_timing': ['breakfast', 'brunch', 'lunch', 'dinner'],
        'adventure_level': ['traditional', 'moderate', 'adventurous', 'very_adventurous'],
        'price_sensitivity': ['budget', 'moderate', 'upscale', 'fine_dining']
    }
    
    validated = {}
    
    priorities = tags.get('priorities', [])
    if not isinstance(priorities, list):
        priorities = [priorities] if priorities else []
    validated['priorities'] = [p for p in priorities if p in ALLOWED['priorities']][:2]
    
    styles = tags.get('dining_style', [])
    if not isinstance(styles, list):
        styles = [styles] if styles else []
    validated['dining_style'] = [s for s in styles if s in ALLOWED['dining_style']][:2]
    
    meals = tags.get('meal_timing', [])
    if not isinstance(meals, list):
        meals = [meals] if meals else []
    validated['meal_timing'] = [m for m in meals if m in ALLOWED['meal_timing']]
    
    cuisines = tags.get('cuisine_preferences', [])
    if not isinstance(cuisines, list):
        cuisines = []
    invalid_items = ['ice cream', 'coffee', 'wine', 'beer', 'pizza', 'cocktail', 'dessert', 'vegan', 'vegetarian']
    validated['cuisine_preferences'] = [
        c for c in cuisines 
        if len(str(c)) > 2 and not any(inv in str(c).lower() for inv in invalid_items)
    ]
    
    adventure = tags.get('adventure_level')
    if adventure in ALLOWED['adventure_level']:
        validated['adventure_level'] = adventure
    else:
        rating_std = user_reviews['stars'].std()
        validated['adventure_level'] = 'adventurous' if rating_std > 1.5 else 'moderate'
    
    price = tags.get('price_sensitivity')
    if price in ALLOWED['price_sensitivity']:
        validated['price_sensitivity'] = price
    else:
        validated['price_sensitivity'] = 'upscale' if user_avg_rating >= 4.5 else 'moderate'
    
    return validated

def get_default_tags():
    """Safe defaults"""
    return {
        'priorities': ['food_quality'],
        'dining_style': ['casual'],
        'meal_timing': [],
        'cuisine_preferences': [],
        'adventure_level': 'moderate',
        'price_sensitivity': 'moderate'
    }

def process_user(row):
    """Process single user"""
    user_id = row.user_id
    user_avg_rating = row.average_stars
    user_reviews = df_reviews[df_reviews['user_id'] == user_id]
    
    tags = extract_tags(user_id, user_reviews, user_avg_rating)
    
    return {
        'user_id': user_id,
        'tags': json.dumps(tags),
        'reviews_analyzed': len(user_reviews)
    }

# Process in parallel batches
profiles = []
batch_size = 500

for batch_start in tqdm(range(0, len(df_users), batch_size), desc="Batches"):
    batch_end = min(batch_start + batch_size, len(df_users))
    batch = df_users.iloc[batch_start:batch_end]
    
    with ThreadPoolExecutor(max_workers=50) as executor:
        batch_results = list(executor.map(process_user, [row for row in batch.itertuples()]))
    
    profiles.extend(batch_results)
    
    if batch_end % 1000 == 0 or batch_end == len(df_users):
        checkpoint_df = pd.DataFrame(profiles)
        checkpoint_df.to_parquet(f'data/checkpoints/profiles_strict_{batch_end}.parquet', index=False)
        print(f"\n✓ Checkpoint: {batch_end} users")

df_profiles = pd.DataFrame(profiles)
df_profiles.to_parquet('data/final/reviewer_profiles_llm_v2.parquet', index=False)

print(f"\n✓ Tagged {len(df_profiles):,} reviewers with strict validation")
print(f"Saved to: data/final/reviewer_profiles_llm_v2.parquet")
