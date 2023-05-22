from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    present = db.Column(db.Boolean, nullable=False, default=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    rfid = db.Column(db.String, nullable=True)
    vector = db.Column(db.Text(), nullable=True)

    def __repr__(self):
        return '<Student %r>' % self.id

# with app.app_context():
#         db.create_all()

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Student(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        students = Student.query.order_by(Student.date_created).all()
        return render_template('index.html', students=students)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Student.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Student.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)

@app.route('/present/<int:id>')
def present(id):
    student = Student.query.get_or_404(id)
    student.present = not student.present
    try:
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue updating the record'

@app.route('/present_rfid/<int:rfid>')
def present_rfid(rfid):
    student = Student.query.filter_by(rfid=rfid).first()
    student.present = not student.present
    try:
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue updating the record'

@app.route('/valid_rfid/<string:rfid>')
def valid_rfid(rfid):
    valid = str(Student.query.filter_by(rfid=rfid).first())
    try:
        return valid
    except:
        return 'There was an issue retriving the record'

@app.route('/add_rfid/<string:content>/<string:rfid>')
def add_rfid(content, rfid):
    student = Student.query.filter_by(content=content).first()
    student.rfid = rfid
    try:
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue updating the record'
    
@app.route('/set_vector/<string:content>/<string:vector>')
def set_vector(content, vector):
    student = Student.query.filter_by(content=content).first()
    student.vector = vector
    try:
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue updating the record'
    
@app.route('/get_vector/<string:rfid>')
def get_vector(rfid):
    student = Student.query.filter_by(rfid=rfid).first()
    try:
        return student.vector
    except:
        return 'There was an issue retriving the record'

@app.route('/get_content/<string:rfid>')
def get_content(rfid):
    student = Student.query.filter_by(rfid=rfid).first()
    try:
        return student.content
    except:
        return 'There was an issue retriving the record'

if __name__ == "__main__":
    app.run(debug=True)
