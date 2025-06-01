from flask import Flask, render_template, request, redirect, url_for
from db import init_db, verify, addposts, get_upcoming_games, get_past_games

app = Flask(__name__)
init_db()

# home page  
@app.route('/')
def home():
    upcoming = get_upcoming_games()
    past = get_past_games()
    return render_template('home.html', upcoming=upcoming, past=past)

# admin login
@app.route('/admin')
def admin():
    return render_template('admin.html')

# authentication
@app.route('/auth', methods=['POST'])
def auth():
    userpw = request.form.get('userpw')
    userid = request.form.get('ccaid')
    is_valid = verify(userid, userpw)

    if is_valid:
        return render_template('addpost.html')
    else:
        error_msg = "Invalid CCAID or password. Please try again."
        return render_template('admin.html', error=error_msg)

@app.route('/addpost', methods = ['POST'])
def addpost():
    ccaid = request.form.get('ccaid')
    opp = request.form.get('opp')
    date = request.form.get('date')
    time = request.form.get('time')
    venue = request.form.get('venue')
    caption = request.form.get('caption')
    riscore = request.form.get('rscore')
    opscore = request.form.get('oscore')
    vid = request.form.get('vlink')

    addposts(ccaid, opp, date, time, venue, riscore, opscore, vid, caption)

    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)