import sqlite3
import pandas as pd
from datetime import datetime

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('data/applications.db', check_same_thread=False)
        self.create_table()
    
    def create_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            position TEXT NOT NULL,
            status TEXT NOT NULL,
            deadline DATE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        '''
        self.conn.execute(query)
        self.conn.commit()
    
    def add_application(self, company, position, status, deadline):
        query = '''
        INSERT INTO applications (company, position, status, deadline)
        VALUES (?, ?, ?, ?)
        '''
        self.conn.execute(query, (company, position, status, deadline))
        self.conn.commit()
    
    def get_all_applications(self):
        query = "SELECT * FROM applications"
        return pd.read_sql_query(query, self.conn)
    
    def update_status(self, app_id, new_status):
        query = "UPDATE applications SET status = ? WHERE id = ?"
        self.conn.execute(query, (new_status, app_id))
        self.conn.commit()
    def delete_application(self, app_id):
      query = "DELETE FROM applications WHERE id = ?"
      self.conn.execute(query, (app_id,))
      self.conn.commit()
