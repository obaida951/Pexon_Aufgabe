import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO certifications (title, content) VALUES (?, ?)",
            ('First Certification', 'Content for the first certification')
            )

connection.commit()
connection.close()