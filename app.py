import flask
from flask import Flask, request, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), nullable=False)
	age = db.Column(db.Integer, nullable=True)
	description = db.Column(db.String(200), nullable=False)

db.create_all()

current_user = "x"

@app.route('/')
def about():
    return render_template('about.html')

@app.route('/school')
def school():
	all_posts = User.query.all()
	return render_template('school.html', all_posts=all_posts)

@app.route('/info')
def info():
	all_posts = User.query.all()
	return render_template('info.html', all_posts=all_posts)

@app.route('/post',methods=['GET','POST'])
def post():
	if request.method == 'POST':
		user = User()
		user.name = request.form['name']
		user.age = request.form['age']
		user.description = request.form['description']
		db.session.add(user)
		db.session.commit()
		global current_user
		current_user = user
		return redirect(url_for('school', user=current_user))

	elif request.method == 'GET':
		return render_template('post.html')
    
if __name__ == "__main__":
    app.run(debug=True)