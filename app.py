from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    data_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    
    alltodos = Todo.query.all()
    return render_template('index.html',alltodos=alltodos)

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def updateUser(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    return render_template('update.html',todo=todo)

@app.route('/delete/<int:sno>')
def deleteUser(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    print("user deleted")
    return redirect('/')

@app.route("/show")
def products():
    alltodos = Todo.query.all()
    print(alltodos) # this prints according to __repr__
    return render_template('this is products page')

