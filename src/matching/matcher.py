"""
Core matching algorithm to find taste twins
"""
import psycopg2
from psycopg2.extras import RealDictCursor
import json
from typing import List, Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

class TasteTwinMatcher:
    """Find taste twins based on quiz responses"""
    
    def __init__(self):
        db_host = os.getenv('DB_HOST', 'localhost')
        self.conn = psycopg2.connect(
            host=db_host,
            port=5432,
            database='dinelike',
            user='dinelike',
            password='dinelike123'
        )
    
    def find_taste_twins(
        self, 
        quiz_tags: Dict[str, Any], 
        top_n: int = 3
    ) -> List[Dict[str, Any]]:
        """Find top N matching reviewers"""
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        
        # Get users with tags
        cursor.execute("""
            SELECT user_id, name, tags
            FROM users
            WHERE tags IS NOT NULL
        """)
        
        users = cursor.fetchall()
        matches = []
        
        for user in users:
            if user['tags']:
                score = self._calculate_match_score(quiz_tags, user['tags'])
                matches.append({
                    'user_id': user['user_id'],
                    'name': user['name'],
                    'match_score': score,
                    'tags': user['tags']
                })
        
        # Sort by score and return top N
        matches.sort(key=lambda x: x['match_score'], reverse=True)
        cursor.close()
        
        return matches[:top_n]
    
    def find_taste_twin(
        self, 
        city: str,
        state: str,
        tags: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Find single best matching reviewer for a city"""
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        
        # Get users who have reviewed in this city
        cursor.execute("""
            SELECT DISTINCT u.user_id, u.name, u.tags
            FROM users u
            JOIN reviews r ON u.user_id = r.user_id
            JOIN businesses b ON r.business_id = b.business_id
            WHERE b.city = %s AND u.tags IS NOT NULL
        """, (city,))
        
        users = cursor.fetchall()
        
        if not users:
            cursor.close()
            return None
        
        best_match = None
        best_score = -1
        
        for user in users:
            if user['tags']:
                score = self._calculate_match_score(tags, user['tags'])
                if score > best_score:
                    best_score = score
                    best_match = {
                        'user_id': user['user_id'],
                        'name': user['name'],
                        'match_score': score,
                        'tags': user['tags']
                    }
        
        cursor.close()
        return best_match
    
    def _calculate_match_score(
        self, 
        quiz_tags: Dict[str, Any], 
        user_tags: Dict[str, Any]
    ) -> float:
        """Calculate match score between quiz and user tags"""
        if not user_tags:
            return 0.0
        
        score = 0.0
        total_weight = 0.0
        
        # Normalize quiz tags - map 'cuisines' to 'cuisine_preferences'
        normalized_quiz = quiz_tags.copy()
        if 'cuisines' in normalized_quiz and 'cuisine_preferences' not in normalized_quiz:
            normalized_quiz['cuisine_preferences'] = normalized_quiz.pop('cuisines')
        
        # Define weights for different tag categories
        weights = {
            'dining_style': 2.0,
            'cuisine_preferences': 2.5,  # Increased weight for cuisines
            'priorities': 2.0,
            'meal_timing': 1.0,
            'adventure_level': 1.5,
            'price_sensitivity': 1.5
        }
        
        for category, weight in weights.items():
            if category in normalized_quiz and category in user_tags:
                quiz_values = set(normalized_quiz[category]) if isinstance(normalized_quiz[category], list) else {normalized_quiz[category]}
                user_values = set(user_tags[category]) if isinstance(user_tags[category], list) else {user_tags[category]}
                
                # Calculate Jaccard similarity
                intersection = len(quiz_values & user_values)
                union = len(quiz_values | user_values)
                
                if union > 0:
                    similarity = intersection / union
                    score += similarity * weight
                    total_weight += weight
        
        return (score / total_weight * 100) if total_weight > 0 else 0.0
    
    def get_recommendations(self, taste_twins: List[Dict[str, Any]], limit: int = 10) -> List[Dict[str, Any]]:
        """Get restaurant recommendations based on taste twins"""
        if not taste_twins:
            return []
        
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        
        # Use top 5 twins
        twin_user_ids = [twin['user_id'] for twin in taste_twins[:5]]
        
        # Find restaurants they loved (4+ stars), prioritize those endorsed by multiple twins
        cursor.execute("""
            SELECT 
                b.business_id,
                b.name,
                b.address,
                b.city,
                b.state,
                b.stars as overall_stars,
                AVG(r.stars) as twin_avg_rating,
                COUNT(DISTINCT r.user_id) as twin_endorsement_count,
                ARRAY_AGG(DISTINCT u.name) as endorsing_twin_names,
                ARRAY_AGG(r.text ORDER BY r.stars DESC) FILTER (WHERE r.text IS NOT NULL AND LENGTH(r.text) > 50) as sample_reviews
            FROM businesses b
            JOIN reviews r ON b.business_id = r.business_id
            JOIN users u ON r.user_id = u.user_id
            WHERE r.user_id = ANY(%s)
              AND r.stars >= 4
            GROUP BY b.business_id, b.name, b.address, b.city, b.state, b.stars
            ORDER BY twin_endorsement_count DESC, twin_avg_rating DESC, b.stars DESC
            LIMIT %s
        """, (twin_user_ids, limit))
        
        recommendations = cursor.fetchall()
        cursor.close()
        
        return [dict(rec) for rec in recommendations]
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
