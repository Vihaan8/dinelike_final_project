-- DineLike Database Schema
CREATE TABLE IF NOT EXISTS businesses (
    business_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(10),
    postal_code VARCHAR(20),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    stars DECIMAL(2, 1),
    review_count INTEGER,
    categories TEXT
);

CREATE TABLE IF NOT EXISTS users (
    user_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100),
    review_count INTEGER,
    yelping_since VARCHAR(50),
    useful INTEGER,
    funny INTEGER,
    cool INTEGER,
    elite TEXT,
    friends TEXT,
    fans INTEGER,
    average_stars DECIMAL(3, 2),
    tags JSONB
);

CREATE TABLE IF NOT EXISTS reviews (
    review_id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50) REFERENCES users(user_id),
    business_id VARCHAR(50) REFERENCES businesses(business_id),
    stars INTEGER,
    useful INTEGER,
    funny INTEGER,
    cool INTEGER,
    text TEXT,
    date VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS quiz_submissions (
    submission_id SERIAL PRIMARY KEY,
    display_name VARCHAR(100),
    city VARCHAR(100),
    state VARCHAR(10),
    tags JSONB,
    top_twin_user_id VARCHAR(50),
    top_twin_name VARCHAR(100),
    match_score DECIMAL(5, 2),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_reviews_user_id ON reviews(user_id);
CREATE INDEX IF NOT EXISTS idx_reviews_business_id ON reviews(business_id);
CREATE INDEX IF NOT EXISTS idx_businesses_city ON businesses(city);
CREATE INDEX IF NOT EXISTS idx_users_tags ON users USING GIN(tags);
CREATE INDEX IF NOT EXISTS idx_quiz_submissions_created ON quiz_submissions(created_at DESC);
