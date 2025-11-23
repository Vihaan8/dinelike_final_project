-- Quiz submissions table (populated by Kafka consumer)
CREATE TABLE IF NOT EXISTS quiz_submissions (
    submission_id SERIAL PRIMARY KEY,
    display_name VARCHAR(100) DEFAULT 'Anonymous',
    quiz_tags JSONB NOT NULL,
    top_twin_user_id VARCHAR(50) NOT NULL,
    top_twin_name VARCHAR(100) NOT NULL,
    match_score DECIMAL(5,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    city VARCHAR(100) DEFAULT 'Santa Barbara',
    state VARCHAR(50) DEFAULT 'CA',
    processing_status VARCHAR(20) DEFAULT 'completed'
);

CREATE INDEX idx_quiz_submissions_created_at ON quiz_submissions(created_at DESC);
CREATE INDEX idx_quiz_submissions_twin ON quiz_submissions(top_twin_user_id);

-- User activity log (for analytics)
CREATE TABLE IF NOT EXISTS user_activity_log (
    activity_id SERIAL PRIMARY KEY,
    event_type VARCHAR(50) NOT NULL,
    user_identifier VARCHAR(100),
    event_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_user_activity_created_at ON user_activity_log(created_at DESC);
CREATE INDEX idx_user_activity_type ON user_activity_log(event_type);
