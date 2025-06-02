from flask import Flask, render_template, request, redirect, url_for, session
from db import init_db, verify, addposts, updatepost, get_upcoming_games, get_past_games, get_posts_by_ccaid, get_ccas, get_ccaname_byid

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  #remembers all the login details etc
init_db()

# Home page WORKS
@app.route('/')
def home():
    ccas = get_ccas()
    upcoming = get_upcoming_games()
    past = get_past_games()
    return render_template('home.html', upcoming=upcoming, past=past, ccas=ccas)

#CCA pages (ccaid in url itself) WORKS
@app.route('/cca/<ccaid>')
def cca_page(ccaid):
    posts = get_posts_by_ccaid(ccaid)
    ccaname = get_ccaname_byid(ccaid)
    return render_template('cca.html', posts=posts, ccaname=ccaname)

# Admin login page WORKS
@app.route('/admin')
def admin():
    return render_template('admin.html')

# Handle login WORKS
@app.route('/auth', methods=['POST'])
def auth():
    userpw = request.form.get('userpw')
    userid = request.form.get('ccaid')

    is_valid = verify(userid, userpw)

    if is_valid:
        session['ccaid'] = userid
        return redirect(url_for('addpost_form')) 


    else:
        error_msg = "Invalid CCAID or password. Please try again."
        return render_template('admin.html', error=error_msg)


# Show add/update form
@app.route('/addpostform')
def addpost_form():
    ccaid = session.get('ccaid')
    ccaname = get_ccaname_byid(ccaid)

    posts = get_posts_by_ccaid(ccaid)
    return render_template('addpost.html', posts=posts, ccaname=ccaname)


# Add post WORKS
@app.route('/addpost', methods=['POST'])
def addpost():
    ccaid = session.get('ccaid')
    if not ccaid:
        return redirect(url_for('admin'))
    
    ccaname = get_ccaname_byid(ccaid)

    #get data from form
    opp = request.form.get('opp')
    date = request.form.get('date')
    time = request.form.get('time')
    venue = request.form.get('venue')
    caption = request.form.get('caption')
    riscore = request.form.get('rscore')
    opscore = request.form.get('oscore')
    vid = request.form.get('vlink')

    addposts(ccaid, ccaname, opp, date, time, venue, riscore, opscore, vid, caption)

    return redirect(url_for('home'))

# Update post BUGGY
@app.route('/updatepost', methods=['POST'])
def update():
    ccaid = session.get('ccaid')
    if not ccaid:
        return redirect(url_for('admin'))

    #get data from form
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

if __name__ == '__main__':
    app.run(debug=True)
