"""
Unit tests for TasteTwinMatcher
"""
import pytest
from unittest.mock import Mock, patch
from src.matching.matcher import TasteTwinMatcher

@pytest.fixture
def mock_db_connection():
    """Mock database connection for unit tests"""
    with patch('psycopg2.connect') as mock_conn:
        mock_conn.return_value = Mock()
        yield mock_conn

# Original 5 tests
def test_calculate_similarity_exact_match(mock_db_connection):
    """Test that identical preferences give high score"""
    matcher = TasteTwinMatcher()
    
    quiz_tags = {
        'cuisines': ['italian', 'mexican'],
        'priorities': ['food_quality', 'atmosphere'],
        'dining_style': ['casual', 'cozy'],
        'meal_timing': ['dinner'],
        'adventure_level': 'moderate',
        'price_sensitivity': 'moderate'
    }
    
    reviewer_tags = {
        'cuisine_preferences': ['italian', 'mexican'],
        'priorities': ['food_quality', 'atmosphere'],
        'dining_style': ['casual', 'cozy'],
        'meal_timing': ['dinner'],
        'adventure_level': 'moderate',
        'price_sensitivity': 'moderate'
    }
    
    score = matcher._calculate_match_score(quiz_tags, reviewer_tags)
    
    assert score >= 95.0, f"Expected high match (>=95), got {score}"
    assert score <= 100.0, f"Score should not exceed 100, got {score}"

def test_calculate_similarity_no_match(mock_db_connection):
    """Test that completely different preferences give low score"""
    matcher = TasteTwinMatcher()
    
    quiz_tags = {
        'cuisines': ['italian'],
        'priorities': ['food_quality'],
        'dining_style': ['upscale'],
        'meal_timing': ['dinner'],
        'adventure_level': 'traditional',
        'price_sensitivity': 'fine_dining'
    }
    
    reviewer_tags = {
        'cuisine_preferences': ['chinese'],
        'priorities': ['value'],
        'dining_style': ['casual'],
        'meal_timing': ['breakfast'],
        'adventure_level': 'very_adventurous',
        'price_sensitivity': 'budget'
    }
    
    score = matcher._calculate_match_score(quiz_tags, reviewer_tags)
    
    assert score < 30.0, f"Expected low match (<30), got {score}"

def test_calculate_similarity_partial_match(mock_db_connection):
    """Test partial overlap gives medium score"""
    matcher = TasteTwinMatcher()
    
    quiz_tags = {
        'cuisines': ['italian', 'mexican'],
        'priorities': ['food_quality'],
        'dining_style': ['casual'],
        'meal_timing': ['dinner'],
        'adventure_level': 'moderate',
        'price_sensitivity': 'moderate'
    }
    
    reviewer_tags = {
        'cuisine_preferences': ['italian'],
        'priorities': ['food_quality'],
        'dining_style': ['upscale'],
        'meal_timing': ['dinner'],
        'adventure_level': 'moderate',
        'price_sensitivity': 'upscale'
    }
    
    score = matcher._calculate_match_score(quiz_tags, reviewer_tags)
    
    assert 40 < score < 80, f"Expected medium match (40-80), got {score}"

def test_better_cuisine_match_scores_higher(mock_db_connection):
    """Test that more cuisine overlap increases score"""
    matcher = TasteTwinMatcher()
    
    quiz = {
        'cuisines': ['italian', 'mexican', 'japanese'],
        'priorities': ['food_quality'],
        'dining_style': ['casual'],
        'meal_timing': ['dinner'],
        'adventure_level': 'moderate',
        'price_sensitivity': 'moderate'
    }
    
    reviewer_high = {
        'cuisine_preferences': ['italian', 'mexican', 'japanese'],
        'priorities': ['food_quality'],
        'dining_style': ['casual'],
        'meal_timing': ['dinner'],
        'adventure_level': 'moderate',
        'price_sensitivity': 'moderate'
    }
    
    reviewer_low = {
        'cuisine_preferences': ['italian'],
        'priorities': ['food_quality'],
        'dining_style': ['casual'],
        'meal_timing': ['dinner'],
        'adventure_level': 'moderate',
        'price_sensitivity': 'moderate'
    }
    
    score_high = matcher._calculate_match_score(quiz, reviewer_high)
    score_low = matcher._calculate_match_score(quiz, reviewer_low)
    
    assert score_high > score_low, f"More cuisine matches ({score_high}) should score higher than fewer ({score_low})"

def test_empty_arrays_dont_crash(mock_db_connection):
    """Test that empty preference arrays are handled gracefully"""
    matcher = TasteTwinMatcher()
    
    quiz_tags = {
        'cuisines': [],
        'priorities': [],
        'dining_style': [],
        'meal_timing': [],
        'adventure_level': 'moderate',
        'price_sensitivity': 'moderate'
    }
    
    reviewer_tags = {
        'cuisine_preferences': ['italian'],
        'priorities': ['food_quality'],
        'dining_style': ['casual'],
        'meal_timing': ['dinner'],
        'adventure_level': 'moderate',
        'price_sensitivity': 'moderate'
    }
    
    score = matcher._calculate_match_score(quiz_tags, reviewer_tags)
    
    assert isinstance(score, (int, float))
    assert 0 <= score <= 100

# NEW 10 tests
def test_missing_quiz_categories(mock_db_connection):
    """Test handling of missing categories in quiz tags"""
    matcher = TasteTwinMatcher()
    
    quiz_tags = {
        'cuisines': ['italian'],
        'adventure_level': 'moderate'
        # Missing priorities, dining_style, meal_timing, price_sensitivity
    }
    
    reviewer_tags = {
        'cuisine_preferences': ['italian'],
        'priorities': ['food_quality'],
        'dining_style': ['casual'],
        'meal_timing': ['dinner'],
        'adventure_level': 'moderate',
        'price_sensitivity': 'moderate'
    }
    
    score = matcher._calculate_match_score(quiz_tags, reviewer_tags)
    
    assert isinstance(score, (int, float))
    assert 0 <= score <= 100

def test_missing_reviewer_categories(mock_db_connection):
    """Test handling of missing categories in reviewer tags"""
    matcher = TasteTwinMatcher()
    
    quiz_tags = {
        'cuisines': ['italian'],
        'priorities': ['food_quality'],
        'dining_style': ['casual'],
        'meal_timing': ['dinner'],
        'adventure_level': 'moderate',
        'price_sensitivity': 'moderate'
    }
    
    reviewer_tags = {
        'cuisine_preferences': ['italian'],
        'adventure_level': 'moderate'
        # Missing other categories
    }
    
    score = matcher._calculate_match_score(quiz_tags, reviewer_tags)
    
    assert isinstance(score, (int, float))
    assert 0 <= score <= 100

def test_cuisine_normalization(mock_db_connection):
    """Test that 'cuisines' is properly normalized to 'cuisine_preferences'"""
    matcher = TasteTwinMatcher()
    
    quiz_tags = {
        'cuisines': ['italian', 'japanese'],  # Uses 'cuisines'
        'priorities': ['food_quality'],
        'dining_style': ['casual'],
        'meal_timing': ['dinner'],
        'adventure_level': 'moderate',
        'price_sensitivity': 'moderate'
    }
    
    reviewer_tags = {
        'cuisine_preferences': ['italian', 'japanese'],  # Uses 'cuisine_preferences'
        'priorities': ['food_quality'],
        'dining_style': ['casual'],
        'meal_timing': ['dinner'],
        'adventure_level': 'moderate',
        'price_sensitivity': 'moderate'
    }
    
    score = matcher._calculate_match_score(quiz_tags, reviewer_tags)
    
    # Should get high match despite different key names
    assert score >= 95.0, f"Cuisine normalization failed, got {score}"

def test_single_vs_array_values(mock_db_connection):
    """Test that single values and arrays are handled correctly"""
    matcher = TasteTwinMatcher()
    
    quiz_tags = {
        'cuisines': 'italian',  # Single value
        'priorities': ['food_quality'],
        'dining_style': 'casual',  # Single value
        'meal_timing': ['dinner'],
        'adventure_level': 'moderate',
        'price_sensitivity': 'moderate'
    }
    
    reviewer_tags = {
        'cuisine_preferences': ['italian'],  # Array
        'priorities': 'food_quality',  # Single value
        'dining_style': ['casual'],  # Array
        'meal_timing': 'dinner',  # Single value
        'adventure_level': 'moderate',
        'price_sensitivity': 'moderate'
    }
    
    score = matcher._calculate_match_score(quiz_tags, reviewer_tags)
    
    assert score >= 95.0, f"Single value handling failed, got {score}"

def test_all_empty_tags(mock_db_connection):
    """Test scoring when both have empty tags"""
    matcher = TasteTwinMatcher()
    
    quiz_tags = {}
    reviewer_tags = {}
    
    score = matcher._calculate_match_score(quiz_tags, reviewer_tags)
    
    assert score == 0.0, f"Empty tags should give 0 score, got {score}"

def test_large_arrays(mock_db_connection):
    """Test handling of large preference arrays"""
    matcher = TasteTwinMatcher()
    
    all_cuisines = ['italian', 'mexican', 'japanese', 'chinese', 'thai', 
                    'indian', 'vietnamese', 'korean', 'greek', 'french']
    
    quiz_tags = {
        'cuisines': all_cuisines,
        'priorities': ['food_quality', 'atmosphere', 'value', 'service'],
        'dining_style': ['casual', 'upscale', 'cozy', 'lively'],
        'meal_timing': ['breakfast', 'lunch', 'dinner', 'brunch'],
        'adventure_level': 'very_adventurous',
        'price_sensitivity': 'upscale'
    }
    
    reviewer_tags = {
        'cuisine_preferences': all_cuisines,
        'priorities': ['food_quality', 'atmosphere', 'value', 'service'],
        'dining_style': ['casual', 'upscale', 'cozy', 'lively'],
        'meal_timing': ['breakfast', 'lunch', 'dinner', 'brunch'],
        'adventure_level': 'very_adventurous',
        'price_sensitivity': 'upscale'
    }
    
    score = matcher._calculate_match_score(quiz_tags, reviewer_tags)
    
    assert score >= 95.0, f"Large array matching failed, got {score}"
    assert score <= 100.0

def test_price_sensitivity_matching(mock_db_connection):
    """Test that price sensitivity affects score appropriately"""
    matcher = TasteTwinMatcher()
    
    base_tags = {
        'cuisines': ['italian'],
        'priorities': ['food_quality'],
        'dining_style': ['casual'],
        'meal_timing': ['dinner'],
        'adventure_level': 'moderate'
    }
    
    quiz_budget = {**base_tags, 'price_sensitivity': 'budget'}
    quiz_fine = {**base_tags, 'price_sensitivity': 'fine_dining'}
    
    reviewer_budget = {
        'cuisine_preferences': ['italian'],
        'priorities': ['food_quality'],
        'dining_style': ['casual'],
        'meal_timing': ['dinner'],
        'adventure_level': 'moderate',
        'price_sensitivity': 'budget'
    }
    
    score_match = matcher._calculate_match_score(quiz_budget, reviewer_budget)
    score_mismatch = matcher._calculate_match_score(quiz_fine, reviewer_budget)
    
    assert score_match > score_mismatch, "Price sensitivity match should score higher"

def test_adventure_level_matching(mock_db_connection):
    """Test that adventure level affects score"""
    matcher = TasteTwinMatcher()
    
    base_tags = {
        'cuisines': ['italian'],
        'priorities': ['food_quality'],
        'dining_style': ['casual'],
        'meal_timing': ['dinner'],
        'price_sensitivity': 'moderate'
    }
    
    quiz_traditional = {**base_tags, 'adventure_level': 'traditional'}
    quiz_adventurous = {**base_tags, 'adventure_level': 'very_adventurous'}
    
    reviewer_traditional = {
        'cuisine_preferences': ['italian'],
        'priorities': ['food_quality'],
        'dining_style': ['casual'],
        'meal_timing': ['dinner'],
        'adventure_level': 'traditional',
        'price_sensitivity': 'moderate'
    }
    
    score_match = matcher._calculate_match_score(quiz_traditional, reviewer_traditional)
    score_mismatch = matcher._calculate_match_score(quiz_adventurous, reviewer_traditional)
    
    assert score_match > score_mismatch, "Adventure level match should score higher"

def test_meal_timing_overlap(mock_db_connection):
    """Test meal timing preference matching"""
    matcher = TasteTwinMatcher()
    
    quiz_tags = {
        'cuisines': ['italian'],
        'priorities': ['food_quality'],
        'dining_style': ['casual'],
        'meal_timing': ['breakfast', 'brunch', 'lunch'],
        'adventure_level': 'moderate',
        'price_sensitivity': 'moderate'
    }
    
    reviewer_high = {
        'cuisine_preferences': ['italian'],
        'priorities': ['food_quality'],
        'dining_style': ['casual'],
        'meal_timing': ['breakfast', 'brunch', 'lunch'],
        'adventure_level': 'moderate',
        'price_sensitivity': 'moderate'
    }
    
    reviewer_low = {
        'cuisine_preferences': ['italian'],
        'priorities': ['food_quality'],
        'dining_style': ['casual'],
        'meal_timing': ['dinner'],
        'adventure_level': 'moderate',
        'price_sensitivity': 'moderate'
    }
    
    score_high = matcher._calculate_match_score(quiz_tags, reviewer_high)
    score_low = matcher._calculate_match_score(quiz_tags, reviewer_low)
    
    assert score_high > score_low, "More meal timing overlap should score higher"

def test_priorities_influence_score(mock_db_connection):
    """Test that priorities category affects scoring"""
    matcher = TasteTwinMatcher()
    
    quiz_tags = {
        'cuisines': ['italian'],
        'priorities': ['food_quality', 'atmosphere'],
        'dining_style': ['casual'],
        'meal_timing': ['dinner'],
        'adventure_level': 'moderate',
        'price_sensitivity': 'moderate'
    }
    
    reviewer_match = {
        'cuisine_preferences': ['italian'],
        'priorities': ['food_quality', 'atmosphere'],
        'dining_style': ['casual'],
        'meal_timing': ['dinner'],
        'adventure_level': 'moderate',
        'price_sensitivity': 'moderate'
    }
    
    reviewer_mismatch = {
        'cuisine_preferences': ['italian'],
        'priorities': ['value', 'service'],
        'dining_style': ['casual'],
        'meal_timing': ['dinner'],
        'adventure_level': 'moderate',
        'price_sensitivity': 'moderate'
    }
    
    score_match = matcher._calculate_match_score(quiz_tags, reviewer_match)
    score_mismatch = matcher._calculate_match_score(quiz_tags, reviewer_mismatch)
    
    assert score_match > score_mismatch, "Matching priorities should score higher"
