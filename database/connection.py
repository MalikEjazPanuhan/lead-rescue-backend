import sqlite3
import json
from datetime import datetime
import os
import re

DB_PATH = os.getenv("DATABASE_PATH", "lead_rescue.db")

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Create tables if they don't exist"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Create leads table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lead_id TEXT UNIQUE NOT NULL,
            source TEXT,
            name TEXT,
            email TEXT,
            phone TEXT,
            message TEXT,
            lead_score INTEGER,
            category TEXT,
            budget TEXT,
            urgency TEXT,
            intent TEXT,
            estimated_value REAL,
            status TEXT DEFAULT 'new',
            first_response_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create email_sequence table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS email_sequence (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lead_id TEXT,
            lead_email TEXT,
            lead_name TEXT,
            step INTEGER,
            subject TEXT,
            content TEXT,
            scheduled_for TIMESTAMP,
            sent BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Database initialized")

async def execute_query(query: str, *args):
    """Execute query and return results"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Convert PostgreSQL style $1, $2 to SQLite style ?
    import re
    sqlite_query = re.sub(r'\$(\d+)', '?', query)
    
    try:
        cursor.execute(sqlite_query, args)
        if query.strip().upper().startswith('SELECT'):
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        else:
            conn.commit()
            return []
    except Exception as e:
        print(f"Database error: {e}")
        return []
    finally:
        conn.close()

        