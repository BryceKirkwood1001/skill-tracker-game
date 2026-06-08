import sqlite3

connection = sqlite3.connect("skills.db")
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS skills
    (
        name TEXT PRIMARY KEY,
        goal INTEGER,
        hours INTEGER,
        xp_value INTEGER
    )
""")

connection.commit()
connection.close()

print("database created")