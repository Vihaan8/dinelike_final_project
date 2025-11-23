-- Businesses table
CREATE TABLE IF NOT EXISTS businesses (
    business_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(50),
    postal_code VARCHAR(20),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    stars DECIMAL(2, 1),
    review_count INTEGER,
    is_open BOOLEAN,
    categories TEXT
);

-- Users table
CREATE TABLE IF NOT EXISTS users (
    user_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255),
    review_count INTEGER DEFAULT 0,
    yelping_since DATE,
    useful INTEGER DEFAULT 0,
    funny INTEGER DEFAULT 0,
    cool INTEGER DEFAULT 0,
    elite TEXT,
    friends TEXT,
    fans INTEGER DEFAULT 0,
    average_stars DECIMAL(3, 2),
    tags JSONB
);

-- Reviews table
CREATE TABLE IF NOT EXISTS reviews (
    review_id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50) REFERENCES users(user_id),
    business_id VARCHAR(50) REFERENCES businesses(business_id),
    stars INTEGER,
    useful INTEGER DEFAULT 0,
    funny INTEGER DEFAULT 0,
    cool INTEGER DEFAULT 0,
    text TEXT,
    date DATE
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_reviews_user_id ON reviews(user_id);
CREATE INDEX IF NOT EXISTS idx_reviews_business_id ON reviews(business_id);
CREATE INDEX IF NOT EXISTS idx_reviews_stars ON reviews(stars);
CREATE INDEX IF NOT EXISTS idx_businesses_city ON businesses(city);
CREATE INDEX IF NOT EXISTS idx_users_review_count ON users(review_count);
