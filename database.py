"""Database management for Instagram OSINT"""

import sqlite3
from datetime import datetime
import json

class OsintDatabase:
    """SQLite database for storing OSINT data"""
    
    def __init__(self, db_name="osint_data.db"):
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        """Initialize database with required tables"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Profiles table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                user_id INTEGER,
                full_name TEXT,
                biography TEXT,
                external_url TEXT,
                is_private BOOLEAN,
                is_business BOOLEAN,
                business_category TEXT,
                followers INTEGER,
                following INTEGER,
                posts INTEGER,
                profile_pic_url TEXT,
                first_seen TIMESTAMP,
                last_updated TIMESTAMP
            )
        ''')
        
        # Followers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS followers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                profile_username TEXT,
                follower_username TEXT,
                follower_id INTEGER,
                follower_full_name TEXT,
                recorded_at TIMESTAMP,
                FOREIGN KEY(profile_username) REFERENCES profiles(username)
            )
        ''')
        
        # Historical data table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS profile_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                followers_count INTEGER,
                following_count INTEGER,
                posts_count INTEGER,
                recorded_at TIMESTAMP,
                FOREIGN KEY(username) REFERENCES profiles(username)
            )
        ''')
        
        # Analytics cache table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analytics_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                engagement_rate REAL,
                follower_ratio REAL,
                risk_score INTEGER,
                profile_type TEXT,
                recorded_at TIMESTAMP,
                FOREIGN KEY(username) REFERENCES profiles(username)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_profile(self, profile):
        """Save profile data to database"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO profiles 
                (username, user_id, full_name, biography, external_url, is_private, is_business, 
                 business_category, followers, following, posts, profile_pic_url, last_updated)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                profile.username,
                profile.userid,
                profile.full_name,
                profile.biography,
                profile.external_url,
                profile.is_private,
                profile.is_business_account,
                profile.business_category_name,
                profile.followers,
                profile.followees,
                profile.mediacount,
                profile.profile_pic_url,
                datetime.now()
            ))
            
            # Also record in history
            cursor.execute('''
                INSERT INTO profile_history 
                (username, followers_count, following_count, posts_count, recorded_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                profile.username,
                profile.followers,
                profile.followees,
                profile.mediacount,
                datetime.now()
            ))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error saving profile: {e}")
            return False
        finally:
            conn.close()
    
    def save_followers(self, profile_username, followers_list):
        """Save followers to database"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        try:
            for follower in followers_list:
                cursor.execute('''
                    INSERT INTO followers 
                    (profile_username, follower_username, follower_id, follower_full_name, recorded_at)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    profile_username,
                    follower.get("username"),
                    follower.get("user_id"),
                    follower.get("full_name"),
                    datetime.now()
                ))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error saving followers: {e}")
            return False
        finally:
            conn.close()
    
    def save_analytics(self, username, analytics_data):
        """Save analytics results"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO analytics_cache 
                (username, engagement_rate, follower_ratio, risk_score, profile_type, recorded_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                username,
                analytics_data.get("engagement_rate"),
                analytics_data.get("follower_ratio"),
                analytics_data.get("risk_score"),
                analytics_data.get("profile_type"),
                datetime.now()
            ))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error saving analytics: {e}")
            return False
        finally:
            conn.close()
    
    def get_profile_history(self, username):
        """Get historical data for a profile"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT followers_count, following_count, posts_count, recorded_at 
                FROM profile_history 
                WHERE username = ? 
                ORDER BY recorded_at
            ''', (username,))
            
            results = cursor.fetchall()
            return [
                {
                    "followers": r[0],
                    "following": r[1],
                    "posts": r[2],
                    "recorded_at": r[3]
                }
                for r in results
            ]
        finally:
            conn.close()
    
    def get_growth_stats(self, username):
        """Calculate growth stats from history"""
        history = self.get_profile_history(username)
        
        if len(history) < 2:
            return None
        
        first = history[0]
        last = history[-1]
        
        return {
            "followers_change": last["followers"] - first["followers"],
            "following_change": last["following"] - first["following"],
            "posts_change": last["posts"] - first["posts"],
            "data_points": len(history),
            "first_recorded": first["recorded_at"],
            "last_recorded": last["recorded_at"]
        }
    
    def get_all_profiles(self):
        """Get all stored profiles"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT username FROM profiles')
            return [row[0] for row in cursor.fetchall()]
        finally:
            conn.close()
