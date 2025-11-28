import sqlite3
from datetime import datetime

class DatabaseManager:
    def __init__(self):
        self.init_db()
    
    def init_db(self):
        conn = sqlite3.connect('sensor_data.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sensor_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id TEXT NOT NULL,
                data_value TEXT NOT NULL, 
                timestamp TEXT NOT NULL,
                processed INTEGER DEFAULT 0
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ База данных инициализирована")

# Базовый функционал для демонстрации