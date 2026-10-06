from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Todo(db.Model):
    ticket = db.Column(db.Integer, primary_key=True)
    completionstatus = db.Column(db.Boolean, default=False)
    username = db.Column(db.String(100), nullable=False)
    priority = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    issuetype = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Task {self.ticket}>"


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        print(request.form)

        new_task = Todo(
            # completionstatus=request.form.get("completionstatus") == "on",
            username=request.form.get("username"),
            priority=request.form.get("priority"),
            description=request.form.get("description"),
            issuetype=request.form.get("issuetype")
        )

        db.session.add(new_task)
        db.session.commit()
    tasks = Todo.query.all()
    return render_template("index.html", tasks=tasks)

@app.route("/removetask/<int:ticket>", methods=["GET","POST"])
def remove_task(ticket):
    task = db.session.get(Todo, ticket)
    if task is not None:
        db.session.delete(task)
        db.session.commit()
    return redirect("/")
        

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)