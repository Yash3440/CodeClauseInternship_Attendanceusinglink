from flask import Flask, render_template, redirect, url_for, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
import random
import string

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

class AttendanceForm(FlaskForm):
    class_name = StringField('Class Name', validators=[DataRequired()])

class Link:
    links = {}

@app.route('/', methods=['GET', 'POST'])
def index():
    form = AttendanceForm()
    if form.validate_on_submit():
        class_name = form.class_name.data
        link = generate_link()
        Link.links[link] = {'class_name': class_name, 'attendance': set()}
        flash(f'Link generated for {class_name}: {link}', 'success')
        return redirect(url_for('index'))
    return render_template('index.html', form=form, links=Link.links)

@app.route('/<link>', methods=['GET', 'POST'])
def attendance(link):
    if link not in Link.links:
        flash('Invalid link', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        student_name = request.form.get('student_name')
        Link.links[link]['attendance'].add(student_name)
        flash(f'Attendance recorded for {student_name} in {Link.links[link]["class_name"]}', 'success')

    return render_template('attendance.html', class_name=Link.links[link]['class_name'])

def generate_link():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

if __name__ == '__main__':
    app.run(debug=True)
