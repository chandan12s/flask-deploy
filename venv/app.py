# This is a sample Python script.
from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import socket
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crm.db'
db = SQLAlchemy(app)

def fetchDetails():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return str(hostname), str(ip)


@app.route("/health")
def health():
    return jsonify(status='UP')

@app.route("/details")
def details():
    hostname, ip = fetchDetails()
    return render_template('details.html', hostname=hostname,ip=ip)


# Customer model
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    phone = db.Column(db.String(15))
    address = db.Column(db.String(15))
    city = db.Column(db.String(15))
    state = db.Column(db.String(15))
    zip = db.Column(db.String(15))

    def __init__(self, name, email, phone, address, city, state, zip):
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip

# Routes
@app.route('/')
def index():
    customers = Customer.query.all()
    return render_template('index.html', customers=customers)

@app.route('/add', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        zip = request.form['zip']

        customer = Customer(name, email, phone, address, city, state, zip)
        db.session.add(customer)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_customer(id):
    customer = Customer.query.get(id)
    if request.method == 'POST':
        customer.name = request.form['name']
        customer.email = request.form['email']
        customer.phone = request.form['phone']
        customer.address = request.form['address']
        customer.city = request.form['city']
        customer.state = request.form['state']
        customer.zip = request.form['zip']

        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', customer=customer)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_customer(id):
    customer = Customer.query.get(id)
    db.session.delete(customer)
    db.session.commit()
    return redirect(url_for('index'))



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0',port=5050)