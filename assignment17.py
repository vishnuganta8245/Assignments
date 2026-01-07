from flask import Flask, render_template, request, redirect, url_for
import sqlite3
 
app = Flask(__name__)
DB_NAME = "employees.db"
 
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            salary REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()
 
init_db()
 
def query_db(query, args=(), fetch=False):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, args)
    data = cursor.fetchall() if fetch else None
    conn.commit()
    conn.close()
    return data
 
@app.route("/")
def home():
    employees = query_db("SELECT * FROM employees", fetch=True)
    roles = ["Engineer", "Designer", "Manager", "HR"]
    return render_template("index1.html", employees=employees, roles=roles)
 
@app.route("/add", methods=["POST"])
def add_employee():
    name = request.form["name"]
    role = request.form["role"]
    salary = request.form["salary"]
    query_db("INSERT INTO employees (name, role, salary) VALUES (?, ?, ?)",
             (name, role, salary))
    return redirect(url_for("home"))
 
@app.route("/update/<int:emp_id>", methods=["POST"])
def update_employee(emp_id):
    name = request.form["name"]
    role = request.form["role"]
    salary = request.form["salary"]
    query_db("UPDATE employees SET name=?, role=?, salary=? WHERE id=?",
             (name, role, salary, emp_id))
    return redirect(url_for("home"))
 
@app.route("/delete/<int:emp_id>", methods=["POST"])
def delete_employee(emp_id):
    query_db("DELETE FROM employees WHERE id=?", (emp_id,))
    return redirect(url_for("home"))
 
if __name__ == "__main__":
    app.run(debug=True)