"""
Integration tests for FastAPI endpoints
"""
import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

# Original 6 tests
def test_health_endpoint():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_quiz_submit_valid_data():
    """Test quiz submission with valid data"""
    quiz_data = {
        "display_name": "Test User",
        "tags": {
            "priorities": ["food_quality", "atmosphere"],
            "dining_style": ["casual", "cozy"],
            "meal_timing": ["dinner"],
            "cuisines": ["italian", "mexican"],
            "adventure_level": "moderate",
            "price_sensitivity": "moderate"
        },
        "city": "Santa Barbara",
        "state": "CA"
    }
    
    response = client.post("/api/quiz/submit", json=quiz_data)
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_quiz_submit_missing_fields():
    """Test quiz submission fails with missing required fields"""
    invalid_data = {
        "display_name": "Test User"
    }
    
    response = client.post("/api/quiz/submit", json=invalid_data)
    assert response.status_code == 422

def test_community_feed_endpoint():
    """Test community feed returns data"""
    response = client.get("/api/community/feed")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_community_stats_endpoint():
    """Test community stats returns correct structure"""
    response = client.get("/api/community/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_submissions" in data
    assert "today_submissions" in data
    assert "average_match_score" in data

def test_results_latest_endpoint():
    """Test results endpoint returns data structure"""
    response = client.get("/api/results/latest")
    
    if response.status_code == 200:
        data = response.json()
        assert "taste_twins" in data
        assert "recommendations" in data
        assert "display_name" in data
    else:
        assert response.status_code == 404

# NEW 10 tests
def test_quiz_submit_empty_tags():
    """Test quiz submission with empty tag arrays"""
    quiz_data = {
        "display_name": "Empty Tags User",
        "tags": {
            "priorities": [],
            "dining_style": [],
            "meal_timing": [],
            "cuisines": [],
            "adventure_level": "moderate",
            "price_sensitivity": "moderate"
        },
        "city": "Santa Barbara",
        "state": "CA"
    }
    
    response = client.post("/api/quiz/submit", json=quiz_data)
    assert response.status_code == 200

def test_quiz_submit_minimal_tags():
    """Test quiz submission with minimal required data"""
    quiz_data = {
        "display_name": "Minimal User",
        "tags": {
            "cuisines": ["italian"],
            "adventure_level": "moderate",
            "price_sensitivity": "moderate"
        },
        "city": "Santa Barbara",
        "state": "CA"
    }
    
    response = client.post("/api/quiz/submit", json=quiz_data)
    assert response.status_code == 200

def test_quiz_submit_special_characters():
    """Test quiz submission with special characters in name"""
    quiz_data = {
        "display_name": "Test-User_123!@#",
        "tags": {
            "cuisines": ["italian"],
            "adventure_level": "moderate",
            "price_sensitivity": "moderate"
        },
        "city": "Santa Barbara",
        "state": "CA"
    }
    
    response = client.post("/api/quiz/submit", json=quiz_data)
    assert response.status_code == 200

def test_quiz_submit_different_city():
    """Test quiz submission with different city"""
    quiz_data = {
        "display_name": "LA User",
        "tags": {
            "cuisines": ["italian"],
            "adventure_level": "moderate",
            "price_sensitivity": "moderate"
        },
        "city": "Los Angeles",
        "state": "CA"
    }
    
    response = client.post("/api/quiz/submit", json=quiz_data)
    assert response.status_code == 200

def test_community_feed_with_limit():
    """Test community feed respects limit parameter"""
    response = client.get("/api/community/feed?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 5

def test_community_feed_ordering():
    """Test community feed returns items in descending order"""
    response = client.get("/api/community/feed?limit=10")
    assert response.status_code == 200
    data = response.json()
    
    if len(data) >= 2:
        # Check that created_at timestamps are in descending order
        timestamps = [item['created_at'] for item in data]
        assert timestamps == sorted(timestamps, reverse=True)

def test_community_stats_values_are_numbers():
    """Test that all stats values are numeric"""
    response = client.get("/api/community/stats")
    assert response.status_code == 200
    data = response.json()
    
    assert isinstance(data["total_submissions"], int)
    assert isinstance(data["today_submissions"], int)
    assert isinstance(data["average_match_score"], (int, float))
    assert data["total_submissions"] >= 0
    assert data["today_submissions"] >= 0
    assert 0 <= data["average_match_score"] <= 100

def test_api_cors_headers():
    """Test that CORS headers are present"""
    response = client.get("/health")
    assert response.status_code == 200
    # CORS headers should allow frontend access
    assert "access-control-allow-origin" in [h.lower() for h in response.headers.keys()]

def test_invalid_json_submission():
    """Test API handles invalid JSON gracefully"""
    response = client.post(
        "/api/quiz/submit",
        data="invalid json",
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code in [400, 422]

def test_very_long_display_name():
    """Test handling of very long display names"""
    quiz_data = {
        "display_name": "A" * 500,  # Very long name
        "tags": {
            "cuisines": ["italian"],
            "adventure_level": "moderate",
            "price_sensitivity": "moderate"
        },
        "city": "Santa Barbara",
        "state": "CA"
    }
    
    response = client.post("/api/quiz/submit", json=quiz_data)
    # Should either accept it or return validation error
    assert response.status_code in [200, 422]

def test_quiz_health_check():
    """Test quiz-specific health endpoint"""
    response = client.get("/api/quiz/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "quiz"

def test_root_endpoint_structure():
    """Test root endpoint returns API information"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "endpoints" in data
    assert isinstance(data["endpoints"], dict)

def test_community_feed_empty_database():
    """Test community feed handles empty database gracefully"""
    response = client.get("/api/community/feed?limit=100")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # Should return empty list or existing data, not error

def test_quiz_submission_data_types():
    """Test that quiz validates data types correctly"""
    invalid_quiz = {
        "display_name": 123,  # Should be string
        "tags": {
            "cuisines": "italian",  # Should work as single value
            "adventure_level": 123,  # Should be string
            "price_sensitivity": "moderate"
        },
        "city": "Santa Barbara",
        "state": "CA"
    }
    
    response = client.post("/api/quiz/submit", json=invalid_quiz)
    # Should return validation error
    assert response.status_code == 422

def test_api_handles_concurrent_requests():
    """Test API can handle multiple simultaneous requests"""
    import concurrent.futures
    
    def make_request():
        return client.get("/health")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(make_request) for _ in range(10)]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]
    
    # All requests should succeed
    assert all(r.status_code == 200 for r in results)
