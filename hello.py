from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail,Message
import json

with open('templates/config.json','r') as c:
    params=json.load(c)["parameter"]

app = Flask(__name__)
mail = Mail(app)

######################################################
# configuration of mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'liaqatali.developer@gmail.com'
app.config['MAIL_PASSWORD'] = 'dvqulclztvjxfuae'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
#######################################################


if(params["local_server"]):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['depo_uri']

db = SQLAlchemy(app)


class Contact(db.Model):
    '''
    sno, name phone_num, msg, date, email
    '''
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone= db.Column(db.String(12), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    message = db.Column(db.String(120), nullable=False)


class Post(db.Model):
    
    '''
    sno, title, sub_title, content,img_file,slug,post_date,
    '''
    
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    sub_title= db.Column(db.String(20), nullable=False)
    content = db.Column(db.String(20), nullable=False)
    img_file = db.Column(db.String(120), nullable=False)
    slug=db.Column(db.String(200),nullable=False)
    post_date=db.Column(db.String(20),nullable=False)


@app.route("/")
def home():
    return render_template('index.html', params=params)


@app.route("/about")
def about():
    return render_template('about.html', params=params)


@app.route("/post/<string:post_slug>", methods=['GET'])
def post_route(post_slug):
    post=Post.query.filter_by(slug=post_slug).first()
    return render_template('post.html',params=params,post=post)

@app.route("/contact", methods = ['GET', 'POST'])
def contact():
    if(request.method=='POST'):
        '''Add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        entry = Contact(name=name, phone= phone, email = email , message = message)
        mail.send_message("Send by:"+name,sender="liaqataliengr11842@gmail.com",
                            recipients=["liaqataliengr11842@gmail.com"],
                            body=message+email)
        
        db.session.add(entry)
        db.session.commit()
    return render_template('contact.html',params=params)





