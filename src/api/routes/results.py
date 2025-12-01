"""
User results endpoints
"""
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any, Optional
import psycopg2
import os
from pydantic import BaseModel

from ...matching.matcher import TasteTwinMatcher

router = APIRouter(tags=["results"])

@router.get("/latest")
async def get_latest_results():
    """Get the most recent submission's results"""
    try:
        db_host = os.getenv('DB_HOST', 'localhost')
        conn = psycopg2.connect(
            host=db_host,
            database='dinelike',
            user='dinelike',
            password='dinelike123'
        )
        
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT submission_id
                FROM quiz_submissions
                ORDER BY created_at DESC
                LIMIT 1
            """)
            
            row = cursor.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="No submissions found")
            
            submission_id = row[0]
        
        conn.close()
        
        return await get_user_results(submission_id)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{submission_id}")
async def get_user_results(submission_id: int):
    """Get detailed results for a quiz submission"""
    try:
        db_host = os.getenv('DB_HOST', 'localhost')
        conn = psycopg2.connect(
            host=db_host,
            database='dinelike',
            user='dinelike',
            password='dinelike123'
        )
        
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT display_name, tags, city, state
                FROM quiz_submissions
                WHERE submission_id = %s
            """, (submission_id,))
            
            row = cursor.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Submission not found")
            
            display_name = row[0]
            quiz_tags = row[1]
            city = row[2]
            state = row[3]
        
        conn.close()
        
        # Find multiple taste twins (not just the one saved in DB)
        matcher = TasteTwinMatcher()
        
        # Find top 5 taste twins for this city
        taste_twins_raw = []
        cursor = matcher.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute("""
            SELECT DISTINCT u.user_id, u.name, u.tags, u.review_count
            FROM users u
            JOIN reviews r ON u.user_id = r.user_id
            JOIN businesses b ON r.business_id = b.business_id
            WHERE b.city = %s AND u.tags IS NOT NULL
        """, (city,))
        
        users = cursor.fetchall()
        cursor.close()
        
        # Calculate match scores
        for user in users:
            score = matcher._calculate_match_score(quiz_tags, user['tags'])
            taste_twins_raw.append({
                'user_id': user['user_id'],
                'name': user['name'],
                'score': score,
                'tags': user['tags'],
                'review_count': user['review_count']
            })
        
        # Sort by score and take top 5
        taste_twins_raw.sort(key=lambda x: x['score'], reverse=True)
        taste_twins = taste_twins_raw[:5]
        
        # Get recommendations from all 5 twins
        recommendations = matcher.get_recommendations(taste_twins, limit=12)
        matcher.close()
        
        return {
            "submission_id": submission_id,
            "display_name": display_name,
            "taste_twins": taste_twins,
            "recommendations": recommendations
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
