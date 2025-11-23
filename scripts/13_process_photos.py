"""
Extract photo mappings for Santa Barbara restaurants
Creates a lightweight JSON: business_id -> photo_id
"""
import json
import pandas as pd
from pathlib import Path
from collections import defaultdict

print("Loading Santa Barbara businesses...")
df_businesses = pd.read_parquet('data/final/businesses_final.parquet')
sb_business_ids = set(df_businesses['business_id'].values)
print(f"Found {len(sb_business_ids)} Santa Barbara businesses")

print("\nProcessing photos.json...")
business_photos = {}
label_priority = {'food': 1, 'inside': 2, 'outside': 3, 'drink': 4, 'menu': 5}

photo_counts = defaultdict(int)

with open('data/photos/yelp_photos/photos.json', 'r') as f:
    for i, line in enumerate(f):
        if i % 50000 == 0:
            print(f"Processed {i:,} photos... Found {len(business_photos)} SB photos")
        
        photo = json.loads(line)
        business_id = photo.get('business_id')
        
        if business_id in sb_business_ids:
            label = photo.get('label', 'food')
            photo_counts[label] += 1
            
            # Keep best photo per business (prioritize food > inside > outside)
            if business_id not in business_photos:
                business_photos[business_id] = {
                    'photo_id': photo.get('photo_id'),
                    'label': label,
                    'priority': label_priority.get(label, 99)
                }
            else:
                # Replace if this photo has higher priority
                current_priority = business_photos[business_id]['priority']
                new_priority = label_priority.get(label, 99)
                if new_priority < current_priority:
                    business_photos[business_id] = {
                        'photo_id': photo.get('photo_id'),
                        'label': label,
                        'priority': new_priority
                    }

print(f"\n✓ Found photos for {len(business_photos)} / {len(sb_business_ids)} Santa Barbara businesses")
print(f"\nPhoto breakdown:")
for label, count in sorted(photo_counts.items()):
    print(f"  {label}: {count}")

# Remove priority field and create final mapping
final_mapping = {
    bid: {'photo_id': data['photo_id'], 'label': data['label']}
    for bid, data in business_photos.items()
}

# Save lightweight mapping
output_file = 'data/photos/sb_business_photos.json'
with open(output_file, 'w') as f:
    json.dump(final_mapping, f, indent=2)

print(f"\n✓ Saved to {output_file}")
print(f"File size: {Path(output_file).stat().st_size / 1024:.1f} KB")

# Show sample
print("\nSample mappings:")
for bid, data in list(final_mapping.items())[:5]:
    print(f"  {bid}: {data}")
