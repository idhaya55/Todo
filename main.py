from flask import Flask, redirect, request,render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, DateField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField
from flask_ckeditor import CKEditor
from sqlalchemy.orm import relationship
import os
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
db = SQLAlchemy(app)

Bootstrap(app)
class Todo(db.Model):
    __tablename__ = "todo"
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String, nullable=False)
    des = db.Column(db.String(150), nullable=False)
    done = db.Column(db.Boolean, nullable=False)
    date = db.Column(db.String)
    list = relationship("Lists", back_populates="tot")

class Lists(db.Model):
    __tablename__ = "lists"
    id = db.Column(db.Integer, primary_key = True)
    title_id = db.Column(db.Integer, db.ForeignKey("todo.id"))
    tot = relationship("Todo", back_populates="list")
    done_li = db.Column(db.Boolean,nullable=False)
    lists = db.Column(db.String, nullable=False)
db.create_all()

class CreateForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    des = StringField('Description/Lists', validators=[DataRequired()])
    duedate = StringField('Duedate')
    submit = SubmitField('Submit')

class ListForm(FlaskForm):
    lists = StringField('Lists')
    submit= SubmitField('Submit')

@app.route('/', methods=['POST', 'GET'])
def main():
    todo = Todo.query.all()
    ty = CreateForm()
    if ty.validate_on_submit():
        todo = Todo.query.all()
        ty = CreateForm()
        title = ty.title.data
        descri = ty.des.data
        date = ty.duedate.data
        done = 1
        qwer = Todo(title=title,des=descri,done=done,date=date)
        db.session.add(qwer)
        db.session.commit()
        return render_template('index.html',all=todo,form=ty)

    return render_template('index.html',all=todo, form=ty)

@app.route("/edit/<int:id>", methods=['POST', 'GET'])
def fish(id):
    user = Todo.query.get(id)
    user.done = 0
    db.session.commit()
    return redirect(url_for('main'))


@app.route('/delete/<int:id>', methods=['POST','GET'])
def delete(id):
    dele = Todo.query.get(id)
    db.session.delete(dele)
    db.session.commit()
    return redirect(url_for('main'))


@app.route('/list/<int:id>', methods=['POST', 'GET'])
def list(id):
    qw = Todo.query.get(id)
    list = Lists.query.filter_by(title_id=id).all()
    asp = ListForm()
    if asp.validate_on_submit():
        ui = asp.lists.data
        don = 1
        print(ui)
        tyo = Lists(title_id=id, lists=ui, done_li=don)
        db.session.add(tyo)
        db.session.commit()
        list = Lists.query.filter_by(title_id=id).all()
        return render_template('zoom.html', rim=qw, forms=asp, loot=list)
    return render_template('zoom.html', rim=qw, forms=asp, loot=list)

@app.route("/edit_li/<int:id>", methods=['POST', 'GET'])
def fish_li(id):
    list = Lists.query.get(id)
    list.done_li = 0
    db.session.commit()
    return redirect(url_for('list', id=list.title_id))

@app.route('/delete_li/<int:id>', methods=['POST','GET'])
def delete_li(id):
    list = Lists.query.get(id)
    db.session.delete(list)
    db.session.commit()
    return redirect(url_for('list', id=list.title_id))

@app.route("/add_li/<int:id>", methods=['POST', 'GET'])
def re_li(id):
    list = Lists.query.get(id)
    list.done_li = 1
    db.session.commit()
    return redirect(url_for('list', id=list.title_id))

if '__main__' == __name__:
    app.run(debug=True)
