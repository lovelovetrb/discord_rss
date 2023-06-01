import sqlite3

class urlDatabase:
    DB_NAME = 'urls.db'

    def __init__(self):
        self.conn = sqlite3.connect(self.DB_NAME)
        self.cursor = self.conn.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS target(id INTEGER PRIMARY KEY, url STRING UNIQUE)')

    def getData(self, query):
        try:
            self.cursor.execute(f'SELECT {query} FROM target')
            return self.cursor.fetchall()
        except sqlite3.OperationalError:
            return "No URL in database"

    def addUrl(self, url):
        try:
            self.cursor.execute(f'INSERT INTO target(url) VALUES(?)', (url,))
            self.conn.commit()
            return "success"
        except sqlite3.IntegrityError:
            return "URL already exists"

    def removeUrl(self, id):
        try:
            self.cursor.execute(f'DELETE FROM target WHERE id = ?', (id,))
            self.cursor.execute('DELETE FROM sqlite_sequence WHERE name = target')
            self.conn.commit()
            return "success"
        except sqlite3.OperationalError:
            return "URL does not exist"
