from flask import Flask, request, redirect, url_for, render_template
import sqlite3

app = Flask(__name__)
DB_NAME = "employee.db"

# Setup table
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            salary REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Connect db
def query_db(query, args=(), one=False):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, args)
    rv = cursor.fetchall()
    conn.commit()
    conn.close()
    return (rv[0] if rv else None) if one else rv

# Routes
@app.route("/")
def index():
    employees = query_db("SELECT * FROM employees")
    return render_template("index.html", employees=employees)

@app.route("/add", methods=["POST"])
def add_employee():
    name = request.form["name"]
    role = request.form["role"]
    salary = request.form["salary"]
    query_db("INSERT INTO employees (name, role, salary) VALUES (?, ?, ?)", (name, role, salary))
    return redirect(url_for("index"))

@app.route("/update/<int:emp_id>", methods=["POST"])
def update_employee(emp_id):
    name = request.form["name"]
    role = request.form["role"]
    salary = request.form["salary"]
    query_db("UPDATE employees SET name=?, role=?, salary=? WHERE id=?", (name, role, salary, emp_id))
    return redirect(url_for("index"))

@app.route("/delete/<int:emp_id>", methods=["POST"])
def delete_employee(emp_id):
    query_db("DELETE FROM employees WHERE id=?", (emp_id,))
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
