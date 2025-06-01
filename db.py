import sqlite3
from datetime import datetime


#CREATE
import sqlite3
def init_db():
    conn = sqlite3.connect("unite.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Accounts (
            ccaid TEXT PRIMARY KEY,
            ccaname TEXT,
            pw TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Posts (
            ccaid TEXT,
            postid TEXT PRIMARY KEY,
            ccaname TEXT,
            opp TEXT,
            date TEXT,
            time TEXT,
            venue TEXT,
            riscore INTEGER,
            opscore INTEGER,
            result TEXT,
            vid TEXT,
            caption TEXT,
            FOREIGN KEY (ccaid) REFERENCES Accounts(ccaid)
            FOREIGN KEY (ccaname) REFERENCES Accounts(ccaname)
        )
    """)
    
    conn.commit()
    conn.close()

#UPDATES
import sqlite3

def verify(userid, upw):
    conn = sqlite3.connect("unite.db")
    cursor = conn.cursor()
    
    # Match both ccaid and pw in one query
    cursor.execute("SELECT * FROM Accounts WHERE ccaid = ? AND pw = ?", (userid, upw))
    result = cursor.fetchone()
    
    conn.close()

    if result is not None:
        return True
    else:
        return False
    
    


    
def addposts(ccaid, opp, date, time, venue, riscore, opscore, vid, caption):
    conn = sqlite3.connect("unite.db")
    cursor = conn.cursor()
    postid = ('''
        SELECT postid
        FROM your_table_name
        ORDER BY id DESC
        LIMIT 1;
    ''')
    postid += 1
    cursor.execute('INSERT INTO Posts (ccaid, postid, opp, date, time, venue, riscore, opscore, vid, caption) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (ccaid, postid, opp, date, time, venue, riscore, opscore, vid, caption))
    conn.commit()
    conn.close()


#READ
def get_upcoming_games():
    conn = sqlite3.connect("unite.db")
    cursor = conn.cursor()

    # Get today's date in YYYY-MM-DD format
    today = datetime.now().strftime("%Y-%m-%d")

    # Select games with date today or in the future, ordered by date and time
    cursor.execute("""
        SELECT ccaname, opp, date, time, venue, riscore, opscore, vid, caption
        FROM Posts
        WHERE date >= ?
        ORDER BY date ASC, time ASC
    """, (today,))
    
    games = cursor.fetchall()
    conn.close()
    
    return games

def get_past_games():
    conn = sqlite3.connect("unite.db")
    cursor = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("""
        SELECT ccaname, opp, date, time, venue, riscore, opscore, vid, caption
        FROM Posts
        WHERE date < ?
        ORDER BY date DESC, time DESC
    """, (today,))
    games = cursor.fetchall()
    conn.close()
    return games