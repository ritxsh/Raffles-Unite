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

    # today date
    today = datetime.now().strftime("%Y-%m-%d")

    # select games after today
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

def get_posts_by_ccaid(ccaid): #gives dict of posts by ccaid (dict required as the details might have to be changed by user)
    conn = sqlite3.connect('unite.db')  
    conn.row_factory = sqlite3.Row  
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT postid, opp, date, time, venue, caption, riscore, opscore, vid
        FROM posts
        WHERE ccaid = ?
        ORDER BY date DESC
    ''', (ccaid,))
    
    rows = cursor.fetchall()
    posts = [dict(row) for row in rows]
    conn.close()
    return posts

def get_ccas(): #returns dict of ccadeets. output[0] = ccaid, output[1] = ccaname
    conn = sqlite3.connect("unite.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT ccaid, ccaname
        FROM Posts
    """,)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_ccaname_byid(ccaid):
    conn = sqlite3.connect("unite.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT ccaname
        FROM Accounts
        WHERE ccaid = ?
        LIMIT 1
    """, (ccaid,))
    
    result = cursor.fetchone()
    conn.close()

    if result:
        return result[0]
    else:
        return "Unnamed CCA"  # or return None, and handle it in route



#UPDATE
def addposts(ccaid, ccaname, opp, date, time, venue, riscore, opscore, vid, caption):
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


    #insert new post
    cursor.execute('''
        INSERT INTO Posts (ccaid, ccaname, postid, opp, date, time, venue, riscore, opscore, vid, caption)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
