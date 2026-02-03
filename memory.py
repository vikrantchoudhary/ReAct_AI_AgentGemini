import sqlite3
import json

#Memory manger using sqlLite database to store every interaction

class MemoryManager:
    def __init__(self, db_path="agent_memory.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS HISTORY
                             (id INTEGER PRIMARY KEY, role TEXT, content TEXT)''')
        #self.cursor.execute('''CREATE TABLE IF NOT EXISTS HISTORY 
        #                    (id INTEGER PRIMARY KEY, role TEXT, content. TEXT)''')
        self.conn.commit()
    
    def save_message(self,role,content):
        self.cursor.execute("INSERT INTO HISTORY (role,content) VALUES(?,?))",
                            (role,json.dump(content)))
        self.conn.commit()
    
    def get_full_history(self):
        self.cursor.execute("SELECT role,content FROM HISTORY")
        rows = self.cursor.fetchall()
        return[{"role" : r , "parts" : [json.loads(c)]} for r,c in rows]