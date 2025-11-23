-- Add indexes for tag-based queries
CREATE INDEX IF NOT EXISTS idx_users_tags ON users USING GIN (tags);
CREATE INDEX IF NOT EXISTS idx_businesses_categories ON businesses(categories);

-- Function to extract user preferences from reviews (run this later with Python)
-- This is a placeholder - actual extraction happens in Python scripts
