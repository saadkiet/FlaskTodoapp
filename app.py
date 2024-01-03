from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///saad.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()

#with app.app_context():
#    db.create_all()

class Todo(db.Model):
    sno= db.Column(db.Integer, primary_key=True)
    title= db.Column(db.String(200), nullable=False)
    desc= db.Column(db.String(500), nullable=False)
    date_created= db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route('/',methods=["GET","POST"])
def hello_world():
    if request.method=="POST":
        #print(request.form['title'])
        title=request.form['title']
        desc=request.form['desc']

        #todo=Todo(title="First Todo",desc="start investing in crypto")
        todo=Todo(title=title,desc=desc)

        db.session.add(todo)
        db.session.commit()
    alltodo=Todo.query.all()
    return render_template("index.html",alltodo=alltodo)


@app.route('/update/<int:sno>',methods=["GET","POST"])
def update(sno):
    if request.method=="POST":
        title=request.form['title']
        desc=request.form['desc']    
        todo=Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")

    todo=Todo.query.filter_by(sno=sno).first()
    return render_template("update.html",todo=todo)


@app.route('/delete/<int:sno>')
def delete(sno):
    todo=Todo.query.filter_by(sno=sno).first() #delete the first record that I select
    db.session.delete(todo)
    db.session.commit()
    #print(alltodo)
    return redirect("/")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/home")
def home():
    return render_template("home.html")

#@app.route('/show')
#def show():
#    alltodo=Todo.query.all()
#    print(alltodo)
#    return "This is a product page"
#
#
#@app.route('/products')
#def products():
#    return "This is a product page"

if __name__=="__main__":
    app.run(debug=True)