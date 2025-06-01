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

#READ
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

def get_post_by_ccaid(ccaid):#returns posts by a cca
    conn = sqlite3.connect("unite.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT ccaname, opp, date, time, venue, riscore, opscore, vid, caption
        FROM Posts
        WHERE ccaid = ?
        ORDER BY date ASC, time ASC
    """, (ccaid,))

    posts = cursor.fetchall()
    conn.close()

    return posts
    

def get_post_by_postid(postid):
    conn = sqlite3.connect("unite.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT *
        FROM Posts
        WHERE postid = ?
    """, (postid,))
    post = cursor.fetchall()
    conn.close()
    return post

def get_ccas(): #returns dict of ccadeets. output[0] = ccaid, output[1] = ccaname
    conn = sqlite3.connect("unite.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ccaid, ccaname
        FROM Posts
    """,)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


#UPDATE
def addposts(ccaid, opp, date, time, venue, riscore, opscore, vid, caption):
    conn = sqlite3.connect("unite.db")
    cursor = conn.cursor()

    #get latest postid
    cursor.execute('''
        SELECT postid
        FROM Posts
        ORDER BY postid DESC
        LIMIT 1;
    ''')
    row = cursor.fetchone()
    last_postid = int(row[0])
    postid = last_postid + 1 #generate new postid

    #get ccaname
    cursor.execute('''
        SELECT ccaname
        FROM Posts
        WHERE ccaid = ?
    ''', (ccaid,))
    ccaname = cursor.fetchone()

    #insert new post
    cursor.execute('''
        INSERT INTO Posts (ccaid, ccaname, postid, opp, date, time, venue, riscore, opscore, vid, caption)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (ccaid, ccaname, postid, opp, date, time, venue, riscore, opscore, vid, caption))

    conn.commit()
    conn.close()


def updatepost(postid, ccaid, opp, date, time, venue, rscore, oscore, vlink, caption):
    conn = sqlite3.connect('unite.db')
    cur = conn.cursor()
    cur.execute("""
        UPDATE Posts
        SET opp = ?, date = ?, time = ?, venue = ?, riscore = ?, opscore = ?, vid = ?, caption = ?
        WHERE postid = ? AND ccaid = ?
    """, (opp, date, time, venue, rscore, oscore, vlink, caption, postid, ccaid))
    conn.commit()
    conn.close()
