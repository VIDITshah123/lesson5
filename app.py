from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///form_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class FormData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    mobile = db.Column(db.String(15), nullable=False)
    address = db.Column(db.Text, nullable=False)
    country = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<FormData {self.name}>"

# Create tables
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']
            mobile = request.form['mobile']
            address = request.form['address']
            country = request.form['country']

            new_entry = FormData(
                name=name,
                email=email,
                mobile=mobile,
                address=address,
                country=country
            )

            db.session.add(new_entry)
            db.session.commit()
            flash('Form submitted successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'danger')
            print(f"Error: {str(e)}")
    
    return render_template('index.html')

@app.route('/view')
def view_data():
    all_entries = FormData.query.order_by(FormData.created_at.desc()).all()
    return render_template('view.html', entries=all_entries)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
