"""
Test the matching algorithm with sample quiz responses
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.matching.matcher import TasteTwinMatcher
import json

print("=== TESTING TASTE TWIN MATCHER ===\n")

# Sample quiz response
quiz_tags = {
    'priorities': ['food_quality', 'atmosphere'],
    'dining_style': ['casual', 'cozy'],
    'meal_timing': ['dinner', 'brunch'],
    'cuisines': ['mexican', 'italian', 'seafood'],
    'adventure_level': 'moderate',
    'price_sensitivity': 'moderate'
}

print("Quiz Responses:")
print(json.dumps(quiz_tags, indent=2))
print()

# Initialize matcher
matcher = TasteTwinMatcher()

# Find taste twins
print("Finding taste twins...")
taste_twins = matcher.find_taste_twins(quiz_tags, top_n=5)

print("\n=== YOUR TASTE TWINS ===\n")

for i, twin in enumerate(taste_twins, 1):
    print(f"{i}. {twin['name']} (Match Score: {twin['score']}/100)")
    print(f"   Reviews: {twin['review_count']}")
    print(f"   Matching tags:")
    
    # Show what matched
    twin_tags = twin['tags']
    
    matching_priorities = set(quiz_tags['priorities']) & set(twin_tags.get('priorities', []))
    if matching_priorities:
        print(f"     Priorities: {', '.join(matching_priorities)}")
    
    matching_style = set(quiz_tags['dining_style']) & set(twin_tags.get('dining_style', []))
    if matching_style:
        print(f"     Dining style: {', '.join(matching_style)}")
    
    matching_cuisines = set(quiz_tags['cuisines']) & set(twin_tags.get('cuisine_preferences', []))
    if matching_cuisines:
        print(f"     Cuisines: {', '.join(matching_cuisines)}")
    
    print()

# Get recommendations
print("=== RECOMMENDED RESTAURANTS ===\n")
recommendations = matcher.get_recommendations(taste_twins, limit=10)

for i, restaurant in enumerate(recommendations, 1):
    print(f"{i}. {restaurant['name']}")
    print(f"   Address: {restaurant['address']}")
    print(f"   Overall: {restaurant['overall_stars']}⭐")
    print(f"   Your twins rated it: {restaurant['twin_avg_rating']:.1f}⭐")
    print(f"   Endorsed by: {', '.join(restaurant['endorsing_twin_names'])}")
    print(f"   Sample review: \"{restaurant['sample_reviews'][0][:100]}...\"")
    print()

matcher.close()

print("✅ Matching algorithm working!")
