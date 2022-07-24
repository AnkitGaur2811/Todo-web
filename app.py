# ------------------------------importing all the libs and function needed------------------------
from email import message
from flask import Flask,render_template,request,session,redirect,url_for
from forms import loginform,signupform,createtaskform,updatetaskform # these imports sre from froms.py
from flask_sqlalchemy import SQLAlchemy

# Creating Flask App
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY']="orange01ankitgaur01"
# ------------------------------ Db related variables ----------------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)


# ------------------------------------- Making Database Models -----------------------------
# Task model
class tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    dese = db.Column(db.String)
    status = db.Column(db.String)
    made_by = db.Column(db.String, db.ForeignKey('user.id'))

    def __repr__(self) -> str:
        return f"{self.id } - {self.title} - {self.status} - {self.dese}"
# User model 
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    phone = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    tasks = db.relationship("tasks", backref="Users")

# Creating Db
db.create_all()

# -------------------------------- Routes -----------------------------------------------
@app.route("/login",methods=["POST", "GET"])
def login():
    form = loginform()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data, password = form.password.data).first()
        if user is None:
            return render_template("login.html", form = form, message = "Wrong Credentials. Please Try Again.")
        else:
            session['user'] = user.id
            return render_template("login.html", message = "Successfully Logged In! Goto Home")
    return render_template("login.html",form=form)

@app.route("/logout")
def logout():
    if 'user' in session:
        session.pop('user',None)
    return redirect(url_for('home'))

@app.route("/signup",methods=["POST", "GET"])
def signup():
    form=signupform()
    if form.validate_on_submit():
        new_user = User(fullname = form.fullname.data, email = form.email.data, phone = form.phone.data, password = form.password.data)
        db.session.add(new_user)
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return render_template("signup.html", form = form, message = "This Email Or Phone already exists in the system! Please Login instead.")
        finally:
            db.session.close()
        return render_template("signup.html", message = "Successfully signed up Now you can login")
    return render_template("signup.html",form=form)

@app.route("/task",methods=["POST", "GET"])
def task():
    userid=session["user"]
    username=User.query.filter_by(id=userid).first()
    alltasks=tasks.query.filter_by(made_by=userid).all()
    return render_template("task.html",user=userid,username=username.fullname,tasks=alltasks)

@app.route("/task/createtask",methods=["POST","GET"])
def createtask():
    userid=session["user"]
    form=createtaskform()
    if form.validate_on_submit():
        new_task=tasks(title = form.title.data, status = form.status.data, dese = form.desc.data, made_by=userid)
        db.session.add(new_task)
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return render_template("createtask.html",form=form)
        finally:
            db.session.close()
        return redirect(url_for('task'))
    return render_template("createtask.html",form=form)

@app.route("/task/update/<int:taskid>",methods=["POST","GET"])
def update_task(taskid):
    form= updatetaskform()
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        status=request.form['status']
        tasku = tasks.query.filter_by(id=taskid).first()
        tasku.title = title
        tasku.dese = desc
        tasku.status=status
        db.session.add(tasku)
        db.session.commit()
        return render_template('updatetask.html', form=form,message="Your task is been updated go to home for confirmation")   
    todo = tasks.query.filter_by(id=taskid).first()
    return render_template('updatetask.html', form=form,todo=todo)

@app.route("/task/delete/<int:taskid>")
def delete_task(taskid):
    todo = tasks.query.filter_by(id=taskid).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('task'))

@app.route("/")
def home():
    if "user" in session:
        return redirect(url_for('task'))
    return render_template("home.html")

@app.route("/about")
def about():
    if "user" in session:
        return render_template("about.html",message="remove")
    return render_template("about.html")

@app.route("/how-to-use")
def how_use():
    if "user" in session:
        return render_template("how-to-use.html",message="remove")
    return render_template("how-to-use.html")


# ----------------------------------- Main code ---------------------------------------
if __name__ =="__main__":
    Port = 80
    app.run(debug = True, port = Port)