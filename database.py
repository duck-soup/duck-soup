'''
Database Schema for notes
    id: int
    emoji: string
    title: string
    content: string
    date: string
    last_modified: string
    tags: string
'''

import sqlite3
import datetime

class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY,
            emoji TEXT,
            title TEXT,
            content TEXT,
            date TEXT,
            last_modified TEXT,
            tags TEXT
        )''')
        self.conn.commit()

    def insert(self, emoji, title, content, date, last_modified, tags):
        if date == '':
            # get current time
            date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        if last_modified == '':
            # get current time
            last_modified = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.cursor.execute('''INSERT INTO notes VALUES (
            NULL, ?, ?, ?, ?, ?, ?
        )''', (emoji, title, content, date, last_modified, tags))
        self.conn.commit()

    def update(self, id, emoji, title, content, date, last_modified, tags):
        if last_modified == '':
            # get current time
            last_modified = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.cursor.execute('''UPDATE notes SET
            emoji = ?,
            title = ?,
            content = ?,
            date = ?,
            last_modified = ?,
            tags = ?
            WHERE id = ?
        ''', (emoji, title, content, date, last_modified, tags, id))
        self.conn.commit()

    def delete(self, title):
        self.cursor.execute('''DELETE FROM notes WHERE title = ?''', (title,))
        self.conn.commit()

    def get_all(self):
        self.cursor.execute('''SELECT * FROM notes''')
        return self.cursor.fetchall()
    
    def get_by_id(self, id):
        self.cursor.execute('''SELECT * FROM notes WHERE id = ?''', (id,))
        return self.cursor.fetchone()
    
    def get_by_title(self, title):
        self.cursor.execute('''SELECT * FROM notes WHERE title = ?''', (title,))
        return self.cursor.fetchone()
    
    def get_by_content(self, content):
        self.cursor.execute('''SELECT * FROM notes WHERE content = ?''', (content,))
        return self.cursor.fetchone()
    
    def get_by_date(self, date):
        self.cursor.execute('''SELECT * FROM notes WHERE date = ?''', (date,))
        return self.cursor.fetchone()


'''
Schema for Settings
    summariser: string
    qa: string
    text_gen: string
    openai_api_key: string
'''
class DbSettings:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS settings (
            summariser TEXT,
            qa TEXT,
            text_gen TEXT,
            openai_api_key TEXT
        )''')
        self.conn.commit()

    def insert(self, summariser, qa, text_gen, openai_api_key):
        self.cursor.execute('''INSERT INTO settings VALUES (
            ?, ?, ?, ?
        )''', (summariser, qa, text_gen, openai_api_key))
        self.conn.commit()

    def update(self, summariser, qa, text_gen, openai_api_key):
        self.cursor.execute('''UPDATE settings SET
            summariser = ?,
            qa = ?,
            text_gen = ?,
            openai_api_key = ?
        ''', (summariser, qa, text_gen, openai_api_key))
        self.conn.commit()

    def get_all(self):
        self.cursor.execute('''SELECT * FROM settings''')
        return self.cursor.fetchall()
    
    def update_key(self, key):
        self.cursor.execute('''UPDATE settings SET
            openai_api_key = ?
        ''', (key,))
        self.conn.commit()


# create db for ai assistants
'''
Schema AI assistants
id: int
name: string
temperature: float
role: string
image_path: string
'''

class DbAIAssistants:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.create_table() 


    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS ai_assistants (
            id INTEGER PRIMARY KEY,
            name TEXT,
            temperature REAL,
            role TEXT,
            image_path TEXT
        )''')
        self.conn.commit()

    def insert(self, name, temperature, role, image_path):
        self.cursor.execute('''INSERT INTO ai_assistants VALUES (
            NULL, ?, ?, ?, ?
        )''', (name, temperature, role, image_path))
        self.conn.commit()

    def update(self, id, name, temperature, role, image_path):
        self.cursor.execute('''UPDATE ai_assistants SET
            name = ?,
            temperature = ?,
            role = ?,
            image_path = ?
            WHERE id = ?
        ''', (name, temperature, role, image_path, id))
        self.conn.commit()

    def update_from_name(self, name, temperature, role, image_path):
        self.cursor.execute('''UPDATE ai_assistants SET
            temperature = ?,
            role = ?,
            image_path = ?
            WHERE name = ?
        ''', (temperature, role, image_path, name))
        self.conn.commit()

    def delete(self, id):
        self.cursor.execute('''DELETE FROM ai_assistants WHERE id = ?''', (id,))
        self.conn.commit()

    def delete_from_name(self, name):
        self.cursor.execute('''DELETE FROM ai_assistants WHERE name = ?''', (name,))
        self.conn.commit()

    def get_all(self):
        self.cursor.execute('''SELECT * FROM ai_assistants''')
        return self.cursor.fetchall()
    
    def get_by_id(self, id):
        self.cursor.execute('''SELECT * FROM ai_assistants WHERE id = ?''', (id,))
        return self.cursor.fetchone()
    
    def get_by_name(self, name):
        self.cursor.execute('''SELECT * FROM ai_assistants WHERE name = ?''', (name,))
        return self.cursor.fetchone()
    
