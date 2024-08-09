from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from datetime import*
import json
import math
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
class Post_id(db.Model):
    post_id = db.Column('post_id',db.Integer, primary_key=True)
    title = db.Column(db.String(300))
    sub_title = db.Column(db.String(500))
    location = db.Column(db.String(300))
    author = db.Column(db.String(100))
    date_posted = db.Column(db.Date)
    image = db.Column(db.String(100))
    content_1 = db.Column(db.String(db.Text))
    content_2 = db.Column(db.String(db.Text))
    slug = db.Column(db.String(500),unique=True)

@app.route('/')
def home():
    db.session.commit()
    post_data = Post_id.query.all()
    n=2
    last = math.ceil(len(post_data)/n)
    page=request.args.get('page')
    if (not str(page).isnumeric()):
        page=1
    page=int(page)
    j=(page-1)*n
    postr= post_data[j:j+n]
    if page==1:
        prev="#"
        next="/?page="+str(page+1)
    elif page==last:
        prev="/?page="+str(page-1)
        next="#"
    else:
        prev="/?page="+str(page-1)
        next="/?page="+str(page+1)
    return render_template('index.html', posts=postr, params=params,prev=prev,next=next)



@app.route("/post/<slug>",methods=['GET','POST'])
def post(slug):
    p_data = Post_id.query.filter_by(slug=slug).first()
    return render_template('post.html',post=p_data,params=params)
@app.route('/about')
def about():
    return render_template('about.html',params=params)

@app.route('/login')
def login():
    return render_template('login.html',params=params)
@app.route('/contact',methods=['GET','POST'])



def contact():
    if request.method == 'POST':
        sno = db.column("sno",db.integer, primary_key=True)
        name = request.form['name']
        email = request.form['email']
        msg = request.form['message']
        entry = Contact(name=name, email=email, massage=msg, date=datetime.today().date())
        db.session.add(entry)
        db.session.commit()
        print(name, email, msg)
    return render_template('contact.html',params=params)
@app.route('/admin',methods=['GET','POST'])
def admin():
    post = Post_id.query.filter_by().all()
    contact=Contact.query.filter_by().all()

    return render_template('admin/index.html',params=params,posts=post,contact=contact)
@app.route('/edit/<string:post_id>',methods=['GET','POST'])
def edit(post_id):
    if request.method == 'POST':
        ntitle = request.form.get('title')
        nsub_title = request.form.get('sub_title')
        nlocation = request.form.get('location')
        nauthor = request.form.get('author')
        ndate_posted = request.form.get('date_posted')
        nimage = request.form.get('image')
        ncontent_1 = request.form.get('content_1')
        ncontent_2 = request.form.get('content_2')
        nslug = request.form.get('slug')
        if post_id=='0':
            post=Post_id(title=ntitle,sub_title=nsub_title,location=nlocation,author=nauthor,date_posted=ndate_posted,image=nimage,content_1=ncontent_1,content_2=ncontent_2,slug=nslug)
            db.session.add(post)
            db.session.commit()
        post=Post_id.query.filter_by(post_id=post_id).first()
        return render_template('admin/edit.html', params=params, post=post, post_id=post_id)






if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8080)












































































































































































































































































































































































































































