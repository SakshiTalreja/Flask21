from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/Flask21'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Mytodo(db.Model):
    Sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    date = db.Column(db.String(15), nullable=False)

    def __repr__(self) -> str:
        return f"{self.Sno} - {self.title}"


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form.get('title')
        desc = request.form.get('desc')
        entry = Mytodo(title=title, description=desc, date=datetime.now())
        db.session.add(entry)
        db.session.commit()
    return render_template('index.html', allTodo=Mytodo.query.all())
    # return 'Hello, World!'


@app.route('/show')
def products():
    allTodos = Mytodo.query.all()
    print(allTodos)
    return 'This is products page'


@app.route('/delete/<int:Sno>')
def delete(Sno):
    todo = Mytodo.query.filter_by(Sno=Sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")


@app.route('/update/<int:Sno>', methods=['GET', 'POST'])
def update(Sno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Mytodo.query.filter_by(Sno=Sno).first()
        todo.title = title
        todo.description = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo = Mytodo.query.filter_by(Sno=Sno).first()
    return render_template('update.html', todo=todo)


if __name__ == "__main__":
    # production
    # http_server = WSGIServer(('', 5000), app)
    # http_server.serve_forever()
    app.run(debug=True, port=5000)  # development server
