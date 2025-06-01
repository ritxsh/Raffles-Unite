from flask import Flask, render_template, request, redirect, url_for, session
from db import init_db, verify, addposts, updatepost, get_upcoming_games, get_past_games, get_post_by_ccaid, get_post_by_postid, get_ccas

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  #remembers all the login details etc
init_db()

# Home page
@app.route('/')
def home():
    ccas = get_ccas()
    upcoming = get_upcoming_games()
    past = get_past_games()
    return render_template('home.html', upcoming=upcoming, past=past, ccas=ccas)

# Admin login page
@app.route('/admin')
def admin():
    return render_template('admin.html')

# Handle login
@app.route('/auth', methods=['POST'])
def auth():
    userpw = request.form.get('userpw')
    userid = request.form.get('ccaid')

    is_valid = verify(userid, userpw)

    if is_valid:
        session['ccaid'] = userid
        posts = get_post_by_ccaid(userid)
        return render_template('addpost.html', posts=posts)
    else:
        error_msg = "Invalid CCAID or password. Please try again."
        return render_template('admin.html', error=error_msg)

# Add a new post
@app.route('/addpost', methods=['POST'])
def addpost():
    ccaid = session.get('ccaid')
    if not ccaid:
        return redirect(url_for('admin'))

    opp = request.form.get('opp')
    date = request.form.get('date')
    time = request.form.get('time')
    venue = request.form.get('venue')
    caption = request.form.get('caption')
    riscore = request.form.get('rscore')
    opscore = request.form.get('oscore')
    vid = request.form.get('vlink')

    addposts(ccaid, opp, date, time, venue, riscore, opscore, vid, caption)

    return redirect(url_for('home'))

# Update an existing post
@app.route('/updatepost', methods=['POST'])
def update():
    ccaid = session.get('ccaid')
    if not ccaid:
        return redirect(url_for('admin'))

    postid = request.form.get('postid')
    opp = request.form.get('opp')
    date = request.form.get('date')
    time = request.form.get('time')
    venue = request.form.get('venue')
    caption = request.form.get('caption')
    riscore = request.form.get('rscore')
    opscore = request.form.get('oscore')
    vid = request.form.get('vlink')

    updatepost(postid, ccaid, opp, date, time, venue, riscore, opscore, vid, caption)

    return redirect(url_for('home'))

# Show add/update form
@app.route('/addpostform')
def addpost_form():
    ccaid = session.get('ccaid')
    if not ccaid:
        return redirect(url_for('admin'))

    posts = get_post_by_ccaid(ccaid)
    return render_template('addpost.html', posts=posts)

#CCA pages (ccaid in url itself)
@app.route('/cca/<ccaid>')
def cca_page(ccaid):
    posts = get_post_by_ccaid(ccaid)
    return render_template('cca.html', posts=posts)

if __name__ == '__main__':
    app.run(debug=True)
