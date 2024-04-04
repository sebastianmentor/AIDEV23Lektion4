from flask import Flask, render_template, request, flash, redirect, url_for
from flask_migrate import Migrate, upgrade
from flask_security import Security, login_required, roles_accepted, roles_required
from models import db, Person, seed_data, user_datastore, hash_password, datetime
from dotenv import load_dotenv
from forms import RegisterNewPersonForm, RegisterNewUserForm
import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URI_LOCAL")
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SECURITY_PASSWORD_SALT'] = os.getenv('SECURITY_PASSWORD_SALT')
app.config['SECURITY_LOGOUT_URL']= '/logout_2'
app.config['SECURITY_POST_LOGOUT_VIEW']= '/godbye'

db.init_app(app)

migrate = Migrate(app, db)

security = Security(app, user_datastore)

@app.route("/")
@login_required
def home_page():
    return render_template("index.html")

@app.route("/newuser", methods = ["GET", "POST"])
@login_required
def register_new_user():
    form = RegisterNewUserForm()
    if request.method == 'POST' and form.validate_on_submit():
            roles = form.roles.data
            user_datastore.create_user(
                email=form.email.data, 
                password=hash_password(form.password.data),
                confirmed_at=datetime.datetime.now(),
                roles= [roles])
            
            db.session.commit()
            flash(f"Succesfully added new User!")
        
    return render_template('register_new_superuser.html', form=form)

@app.route("/register", methods = ["GET", "POST"])
@login_required
def register_new_person():
    form = RegisterNewPersonForm()
    if request.method == 'POST' and form.validate_on_submit():
            
            new_person = Person(
                            name=form.name.data, 
                            age=form.age.data,
                            email=form.email.data,
                            username=form.username.data,
                            phone=form.phone.data
                            )
            
            db.session.add(new_person)
            db.session.commit()
            flash(f"Succesfully added new user!")
            return redirect(url_for('user_page', user_id = new_person.id))
        
    return render_template('register_user.html', form=form)

@app.route("/allusers")
@login_required
def all_users():
    sorting_column = request.args.get('sort_column', 'name')
    sorting_order = request.args.get('sort_order', 'asc')
    page=request.args.get('page', 1, type=int)
    search_word = request.args.get('q', '')

    serch_users = Person.query.filter(
        Person.name.like("%" + search_word + "%")|
        Person.phone.like("%" + search_word + "%")|
        Person.age.like("%" + search_word + "%")|
        Person.username.like("%" + search_word + "%")
    )

    match sorting_column:
        case 'name':
            sort_by = Person.name
        case 'age':
            sort_by = Person.age
        case 'username':
            sort_by = Person.username
        case 'phone':
            sort_by = Person.phone
        case 'email':
            sort_by = Person.email
        case _:
            sort_by = Person.id
    
    sort_by = sort_by.asc() if sorting_order == 'asc' else sort_by.desc()
    
    all_users = serch_users.order_by(sort_by)

    pa_obj = all_users.paginate(page=page, per_page=20, error_out=True)

    return render_template('users.html',
                        all_users = pa_obj.items,
                        pagination = pa_obj,
                        sort_column = sorting_column,
                        sort_order = sorting_order,
                        q=search_word,
                        page = page,
                        pages = pa_obj.pages, 
                        has_next = pa_obj.has_next,
                        has_prev = pa_obj.has_prev
                    )

@app.route("/user/<int:user_id>")
@login_required
def user_page(user_id):
    user = Person.query.filter_by(id=user_id).first()
    return render_template('user_page.html', user = user)

@app.route("/user/goto", methods=["GET", "POST"])
@login_required
def goto_user():
    if request.method == "POST":
        user_id = request.form.get('user_id',type=int)
        return redirect(url_for('user_page', user_id=user_id))
    return render_template('goto.html')

@app.route("/bosspage")
@roles_required("Admin")
def super_admin_page():
    return "The big boss!"

@app.route("/logout_2")
def logout_2():
    return "Loggar ut!"

@app.route("/godbye")
def godbye():
    return "Godbye"

if __name__ == "__main__":
    with app.app_context():
        upgrade()
        seed_data()
    app.run(debug=True)