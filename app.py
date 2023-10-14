from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'Secret Key'


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myuser.db'
app.config['SQALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)

    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone


with app.app_context():
    db.create_all()


# Retrieve data and show it on the page
@app.route('/')
def index():
    employees = User.query.all()
    return render_template('index.html', **locals())


# Create a new employee
@app.route('/create', methods=['POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        new_user = User(name=name, email=email, phone=phone)
        db.session.add(new_user)
        db.session.commit()

        flash(f"Employee added successfully!")

        return redirect(url_for('index'))


# Update employee data
@app.route('/update', methods=["GET", "POST"])
def update():
    print(request.method)
    if request.method == "POST":
        
        data_emp = User.query.get(request.form.get('id'))
        data_emp.name = request.form['name']
        data_emp.email = request.form['email']
        data_emp.phone = request.form['phone']

        db.session.commit()

        flash(f"Employee updated succesfully!")

        return redirect(url_for('index'))

# Delete employee data
@app.route('/delete/<id>')
def delete(id):
    data_emp = User.query.get(id)
    db.session.delete(data_emp)
    db.session.commit()

    flash(f"Employee deleted successfully!")

    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)