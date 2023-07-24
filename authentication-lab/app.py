from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase


config = {"apiKey": "AIzaSyCUzAkwdm04S38pPaWSgN6NW-yk5MfZgVg",
  "authDomain": "guy-s-meet-project1.firebaseapp.com",
  "projectId": "guy-s-meet-project1",
  "storageBucket": "guy-s-meet-project1.appspot.com",
  "messagingSenderId": "591357375724",
  "appId": "1:591357375724:web:3ac93c33bfb6bb5faca1c9",
  "databaseURL": "https://guy-s-meet-project1-default-rtdb.europe-west1.firebasedatabase.app/"}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email,password)
            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed"
            return render_template("signin.html")
    else:
        return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        fullname = request.form['fullname']
        username = request.form['username']
        bio = request.form['bio']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            user_dict = {'email':email, 'fullname':fullname, 'username':username, 'bio':bio}
            UID = login_session['user']['localId']
            db.child("Users").child(UID).set(user_dict)
            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed"
            return render_template("signup.html")
    else:
        return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    try:
        UID = login_session['user']['localId']
        title = request.form['title']
        text = request.form['text']
        tweet = {'title':title, 'text':text, 'uid':UID}
        db.child('Tweets').push(tweet)
    except:
        print("Couldn't add tweet")
    return render_template("add_tweet.html")

@app.route('/all_tweets')
def tweets():
    tweets = db.child('Tweets').get().val()
    return render_template("tweets.html", tweets=tweets)


@app.route('/signout')
def signout():
    auth.current_current = None
    login_session['user'] = None
    return redirect(url_for('signin'))



if __name__ == '__main__':
    app.run(debug=True)