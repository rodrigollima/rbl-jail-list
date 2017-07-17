# 01_create_db.py
import sqlite3

conn = sqlite3.connect('./database/rbl.db')
conn.close()
