import os
from form import Addform, Delform, AddOwner
#from models import Puppy
from flask import Flask, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'

####################################################
############# SQL DB SECTION #######################
####################################################

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

Migrate(app,db)


###################################################
################## MODELS #########################
###################################################

class Puppy(db.Model):
    __tablename__ = 'puppies'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.Text)

    owner = db.relationship('Owner',backref='puppy',uselist=False)
    
    def __init__(self,name):
        self.name = name

    def __repr__(self):
        if self.owner:
            return f"Puppy name is {self.name} and the owner is  {self.owner.name}"
        else:
            return f"Puppy name is {self.name} and has no owner yet!"



class Owner(db.Model):

    __tablename__ = 'owners'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.Text)

    puppy_id = db.Column(db.Integer,db.ForeignKey('puppies.id'))

    def __init__(self,name,puppy_id):
        self.name = name
        self.puppy_id = puppy_id
    


###################################################
########## VIEW FUNCTIONS --FORMS #################
###################################################

@app.route('/')
def index():
    return render_template('home.jinja2')

@app.route('/add',methods=['GET','POST'])
def add_pup():

    form = Addform()

    if form.validate_on_submit():
        name = form.name.data

        new_pup = Puppy(name)
        db.session.add(new_pup)
        db.session.commit()

        return redirect(url_for('list_pup'))


    return render_template('add.html', form=form)



@app.route('/list')
def list_pup():

    puppies = Puppy.query.all()
    return render_template('list.html',puppies=puppies)



@app.route('/delete',methods=['GET','POST'])
def del_pup():

    form = Delform()

    if form.validate_on_submit():

        id = form.id.data
        pup = Puppy.query.get(id)
        db.session.delete(pup)
        db.session.commit()

        return redirect(url_for('list_pup'))

    return render_template('delete.html', form=form)



@app.route('/add_owner',methods=['GET','POST'])
def add_owner():

    form = AddOwner()

    if form.validate_on_submit():

        name = form.name.data
        puppy_id = form.id.data

        new_owner = Owner(name,puppy_id)

        db.session.add(new_owner)
        db.session.commit()

        return redirect(url_for('list_pup'))

    return render_template('add_owner.html', form=form)










if __name__ == "__main__":
    app.run(debug=False)