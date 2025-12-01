"""
Restaurant endpoints
"""
from fastapi import APIRouter, HTTPException
from typing import List, Optional
import psycopg2
import os

router = APIRouter(prefix="/api/restaurants", tags=["restaurants"])

@router.get("/")
async def get_restaurants(limit: int = 20):
    """Get list of restaurants"""
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='dinelike',
            user='dinelike',
            password='dinelike123'
        )
        
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT restaurant_id, name, address, city, state, 
                       cuisine_type, price_range, rating, tags
                FROM restaurants
                LIMIT %s
            """, (limit,))
            
            results = cursor.fetchall()
            
        conn.close()
        
        return [{
            "restaurant_id": row[0],
            "name": row[1],
            "address": row[2],
            "city": row[3],
            "state": row[4],
            "cuisine_type": row[5],
            "price_range": row[6],
            "rating": float(row[7]) if row[7] else None,
            "tags": row[8]
        } for row in results]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def restaurants_health():
    """Health check"""
    return {"status": "healthy", "service": "restaurants"}
