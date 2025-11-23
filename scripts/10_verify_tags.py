"""
Check strict LLM tags (v2)
"""
import pandas as pd
import json
from collections import Counter

print("=== STRICT LLM TAGS ANALYSIS (V2) ===\n")

df = pd.read_parquet('data/final/reviewer_profiles_llm_v2.parquet')

print(f"Total users tagged: {len(df):,}")
print(f"Average reviews per user: {df['reviews_analyzed'].mean():.1f}")

print("\n=== Sample Tags (first 5 users) ===\n")

for idx, row in df.head(5).iterrows():
    tags = json.loads(row['tags'])
    print(f"User {idx+1}:")
    print(f"  Reviews: {row['reviews_analyzed']}")
    print(f"  Priorities: {tags.get('priorities', [])} (type: {type(tags.get('priorities')).__name__})")
    print(f"  Dining style: {tags.get('dining_style', [])} (type: {type(tags.get('dining_style')).__name__})")
    print(f"  Meal timing: {tags.get('meal_timing', [])} (type: {type(tags.get('meal_timing')).__name__})")
    print(f"  Cuisines: {tags.get('cuisine_preferences', [])} (type: {type(tags.get('cuisine_preferences')).__name__})")
    print(f"  Adventure: {tags.get('adventure_level')} (type: {type(tags.get('adventure_level')).__name__})")
    print(f"  Price: {tags.get('price_sensitivity')} (type: {type(tags.get('price_sensitivity')).__name__})")
    print()

# Aggregate
all_priorities = []
all_styles = []
all_meals = []
all_cuisines = []
all_adventure = []
all_price = []

for _, row in df.iterrows():
    tags = json.loads(row['tags'])
    all_priorities.extend(tags.get('priorities', []))
    all_styles.extend(tags.get('dining_style', []))
    all_meals.extend(tags.get('meal_timing', []))
    all_cuisines.extend(tags.get('cuisine_preferences', []))
    
    if tags.get('adventure_level'):
        all_adventure.append(tags['adventure_level'])
    if tags.get('price_sensitivity'):
        all_price.append(tags['price_sensitivity'])

print("=== TAG DISTRIBUTION ===\n")

print("Priorities (should be 4 only):")
for item, count in Counter(all_priorities).most_common():
    print(f"  {item}: {count} ({count/len(df)*100:.1f}%)")

print("\nDining Styles (should be 4 only):")
for item, count in Counter(all_styles).most_common():
    print(f"  {item}: {count} ({count/len(df)*100:.1f}%)")

print("\nMeal Timings (should be 4 only):")
for item, count in Counter(all_meals).most_common():
    print(f"  {item}: {count} ({count/len(df)*100:.1f}%)")

print("\nTop 15 Cuisines:")
for item, count in Counter(all_cuisines).most_common(15):
    print(f"  {item}: {count} ({count/len(df)*100:.1f}%)")

print("\nAdventure Levels (should be 4 only):")
for item, count in Counter(all_adventure).most_common():
    print(f"  {item}: {count} ({count/len(df)*100:.1f}%)")

print("\nPrice Sensitivity (should be 4 only):")
for item, count in Counter(all_price).most_common():
    print(f"  {item}: {count} ({count/len(df)*100:.1f}%)")

# Check for issues
empty_priorities = sum(1 for _, row in df.iterrows() if len(json.loads(row['tags']).get('priorities', [])) == 0)
string_meal_timing = sum(1 for _, row in df.iterrows() if isinstance(json.loads(row['tags']).get('meal_timing'), str))

print(f"\n=== VALIDATION ===")
print(f"Users with empty priorities: {empty_priorities}")
print(f"Users with string meal_timing (should be 0): {string_meal_timing}")

print("\n" + "="*50)
if string_meal_timing == 0 and len(Counter(all_priorities)) <= 4 and len(Counter(all_styles)) <= 4:
    print("✅ TAGS LOOK CLEAN!")
else:
    print("⚠️  Still some issues detected")
print("="*50)
