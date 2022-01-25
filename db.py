import sqlite3

conn = sqlite3.connect('user_db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users
        ([username] TEXT PRIMARY KEY)''')

c.execute('''CREATE TABLE IF NOT EXISTS messages
        ([message] TEXT,
        [id] INTEGER NOT NULL PRIMARY KEY)
        ''')

c.execute('''INSERT INTO users (username)
        VALUES
        ('admin')
    ''')

conn.commit()