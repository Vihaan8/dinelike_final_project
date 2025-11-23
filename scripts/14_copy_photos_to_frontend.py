"""
Copy Santa Barbara business photos to frontend public folder
"""
import json
import shutil
from pathlib import Path

# Load the mapping
with open('data/photos/sb_business_photos.json', 'r') as f:
    photo_mapping = json.load(f)

# Create frontend photos directory
frontend_photos_dir = Path('frontend/public/photos')
frontend_photos_dir.mkdir(parents=True, exist_ok=True)

# Source photos directory
source_dir = Path('data/photos/yelp_photos/photos')

print(f"Copying {len(photo_mapping)} photos to frontend...")
copied = 0
missing = 0

for business_id, photo_data in photo_mapping.items():
    photo_id = photo_data['photo_id']
    
    # Source path
    source_file = source_dir / f'{photo_id}.jpg'
    
    if source_file.exists():
        # Copy to frontend (use business_id as filename for easy lookup)
        dest_file = frontend_photos_dir / f'{business_id}.jpg'
        shutil.copy2(source_file, dest_file)
        copied += 1
        
        if copied % 100 == 0:
            print(f"Copied {copied} photos...")
    else:
        missing += 1

print(f"\n✓ Copied {copied} photos")
print(f"✗ Missing {missing} photos")

# Create photo mapping JSON in frontend
frontend_mapping_file = frontend_photos_dir / 'photo_mapping.json'
with open(frontend_mapping_file, 'w') as f:
    json.dump(photo_mapping, f, indent=2)

print(f"✓ Saved mapping to {frontend_mapping_file}")
