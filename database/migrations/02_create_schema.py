# 02_create_schema.py
import sqlite3

conn = sqlite3.connect('./database/rbl.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE rbl (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        ip varchar(255) NOT NULL,
        rbl varchar(255) NOT NULL,
        text TEXT,
        created_at DATE NOT NULL
);
""")

conn.close()
