"""
Simple Airflow DAG for daily statistics aggregation
This demonstrates orchestration capabilities without interfering with the main pipeline
"""
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import psycopg2
import os

default_args = {
    'owner': 'dinelike',
    'depends_on_past': False,
    'start_date': datetime(2024, 11, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def aggregate_daily_stats(**context):
    """Aggregate daily quiz submission statistics"""
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'postgres'),
            port=os.getenv('DB_PORT', '5432'),
            database=os.getenv('DB_NAME', 'dinelike'),
            user=os.getenv('DB_USER', 'dinelike'),
            password=os.getenv('DB_PASSWORD', 'dinelike123')
        )
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                COUNT(*) as total_submissions,
                AVG(match_score) as avg_match_score,
                COUNT(DISTINCT city) as unique_cities
            FROM quiz_submissions
            WHERE created_at >= CURRENT_DATE;
        """)
        
        result = cursor.fetchone()
        print(f"Daily Stats: {result[0]} submissions, {result[1]:.2f} avg score, {result[2]} cities")
        
        cursor.close()
        conn.close()
        return "Daily stats aggregated successfully"
    except Exception as e:
        print(f"Error: {e}")
        return "Stats aggregation failed (expected if no data yet)"

def check_database_health(**context):
    """Simple database health check"""
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'postgres'),
            port=os.getenv('DB_PORT', '5432'),
            database=os.getenv('DB_NAME', 'dinelike'),
            user=os.getenv('DB_USER', 'dinelike'),
            password=os.getenv('DB_PASSWORD', 'dinelike123')
        )
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users;")
        user_count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        print(f"Database healthy: {user_count} users")
        return "Database health check passed"
    except Exception as e:
        print(f"Health check failed: {e}")
        raise

dag = DAG(
    'daily_community_stats',
    default_args=default_args,
    description='Daily aggregation of community statistics',
    schedule_interval='@daily',
    catchup=False,
)

health_check = PythonOperator(
    task_id='check_database_health',
    python_callable=check_database_health,
    dag=dag,
)

aggregate_stats = PythonOperator(
    task_id='aggregate_daily_stats',
    python_callable=aggregate_daily_stats,
    dag=dag,
)

health_check >> aggregate_stats
