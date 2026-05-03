import sqlite3
import pandas as pd
from datetime import datetime

class DBManager:
    def __init__(self, db_name='insta_viral.db'):
        self.db_name = db_name
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        # Drafts Table
        c.execute('''CREATE TABLE IF NOT EXISTS drafts 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                      caption TEXT, hashtags TEXT, post_type TEXT, 
                      followers INTEGER, score REAL, date_created TEXT)''')
        # User Profile Table
        c.execute('''CREATE TABLE IF NOT EXISTS user_profile 
                     (id INTEGER PRIMARY KEY, username TEXT, niche TEXT, avg_score REAL)''')
        # Competitors Table
        c.execute('''CREATE TABLE IF NOT EXISTS competitors 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, niche TEXT, viral_score REAL)''')
        conn.commit()
        conn.close()

    def update_profile(self, username, niche):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO user_profile (id, username, niche) VALUES (1, ?, ?)", (username, niche))
        conn.commit()
        conn.close()

    def get_profile(self):
        conn = sqlite3.connect(self.db_name)
        df = pd.read_sql_query("SELECT * FROM user_profile WHERE id = 1", conn)
        conn.close()
        return df.iloc[0] if not df.empty else None

    def save_draft(self, caption, hashtags, post_type, followers, score):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        c.execute("INSERT INTO drafts (caption, hashtags, post_type, followers, score, date_created) VALUES (?,?,?,?,?,?)",
                  (caption, hashtags, post_type, followers, score, now))
        conn.commit()
        conn.close()

    def get_drafts(self):
        conn = sqlite3.connect(self.db_name)
        df = pd.read_sql_query("SELECT * FROM drafts ORDER BY id DESC", conn)
        conn.close()
        return df

    def schedule_post(self, caption, time):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("INSERT INTO schedule (caption, schedule_time, status) VALUES (?,?,?)",
                  (caption, time, 'Scheduled'))
        conn.commit()
        conn.close()

    def get_schedule(self):
        conn = sqlite3.connect(self.db_name)
        df = pd.read_sql_query("SELECT * FROM schedule ORDER BY schedule_time ASC", conn)
        conn.close()
        return df
