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
cursor.execute("""
    CREATE TABLE IF NOT EXISTS achievements
    (
        id INTEGER PRIMARY KEY,
        name TEXT,
        description TEXT,
        unlocked INTEGER
    )
    """)

# Numbering: 
# 1 = intro
# 2 = active skills based
# 3 = hours based
# 4 = skill mastery based 
# 5 = daily activity based
default_achievements = [
    (1001,"The First Step","Create your first goal",0),
    (1002,"Well on Your Way","Reach 50% progress on a goal for the first time",0),
    (1003,"The Opening Stretch","Log hours 3 days in a row",0),
    (1004,"Already a Pro","Complete your first goal",0),
    (2001,"Multitasker I","Have 3 active goals",0),
    (2002,"Multitasker II","Have 5 active goals",0),
    (2003,"Multitasker III","Have 10 active goals",0),
    (2004,"Unstoppable Force","Have 20 active goals",0),
    (3001,"Dedication I","Log 10 hours total",0),
    (3002,"Dedication II","Log 50 hours total",0),
    (3003,"Dedication III","Log 100 hours total",0),
    (3004,"Dedication IV","Log 500 hours total",0),
    (3005,"Dedication V","Log 1,000 hours total",0),
    (3006,"Lifelong Commitment","Log 10,000 hours total",0),
    (4001,"Masterful I","Master 1 skill",0),
    (4002,"Masterful II","Master 3 skills",0),
    (4003,"Masterful III","Master 5 skills",0),
    (4004,"Masterful IV","Master 10 skills",0),
    (4005,"Masterful V","Master 15 skills",0),
    (4006,"Grandmaster of All","Master 25 skills",0),
    (5001,"Motivation I","Log hours 7 days in a row",0),
    (5002,"Motivation II","Log hours 30 days in a row",0),
    (5003,"Motivation III","Log hours 90 days in a row",0),
    (5004,"Motivation IV","Log hours 180 days in a row",0),
    (5005,"Motivation V","Log hours 360 days in a row",0),
    (5006,"Moving Mountains","Log hours 1000 days in a row",0)
    ]

for id, name, desc, unlocked in default_achievements:
    cursor.execute("""
        INSERT OR IGNORE INTO achievements
        (id, name, description, unlocked)
        VALUES (?, ?, ?, ?)
        """, (id, name, desc, unlocked))

connection.commit()
connection.close()

print("database created")