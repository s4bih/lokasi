from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from datetime import*
import json

app = Flask(__name__)

with open('config.json', 'r') as c:
    params = json.load(c)["parameters"]




if params["local_server"]:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_url']

else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_url']

SECRET_KEY = params['secret_key']

app.config['SECRET_KEY']
db=SQLAlchemy(app)
class Contact(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    email = db.Column(db.String(50), nullable=False)
    massage = db.Column(db.String(150), nullable=False)
    date = db.Column(db.String(20), nullable=True)
class Posts(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    title = db.column(db.String(300))
    sub_title = db.column(db.String(500))
    location = db.column(db.String(300))
    author = db.column(db.String(100))
    date_posted = db.column(db.Date)
    image = db.column(db.String(100))
    content_1 = db.column(db.String(db.Text))
    content_2 = db.column(db.String(db.Text))

@app.route('/')
def home():
    db.session.commit()
    post_data = Posts.query.all()
    return render_template('index.html',posts=post_data,params=params)


@app.route('/post')
def post():
    return render_template('post.html',params=params)
@app.route('/about')
def about():
    return render_template('about.html',params=params)

@app.route('/login')
def login():
    return render_template('login.html',params=params)
@app.route('/contact',methods=['GET','POST'])



def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        msg = request.form['message']
        entry = Contact(name=name, email=email, massage=msg, date=datetime.today().date())
        db.session.add(entry)
        db.session.commit()
        print(name, email, msg)
    return render_template('contact.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8080)












































































































































































































































































































































































































































