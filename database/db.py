import sqlite3
from pathlib import Path

db_path = Path('.') / 'database' / 'main.db'

conn = sqlite3.connect(db_path)

c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS users (
            username text
        
)""")

c.execute("""CREATE TABLE IF NOT EXISTS friends (
            username text,
            friendservicealias text,
            friendserviceidentifier text

            
)""")

c.execute("""CREATE TABLE IF NOT EXISTS services (
            friendservicealias text,
            friendserviceidentifier text,
            friendservice text,
            friendservicestatus text
            
)""")

conn.commit()

conn.close()

