from flask import Flask, request, redirect, url_for, render_template, jsonify
import sqlite3

app = Flask(__name__)
DB_NAME = "employee.db"


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

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employee_role (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role_name TEXT NOT NULL UNIQUE
        )
    ''')

    conn.commit()
    conn.close()

init_db()


def query_db(query, args=(), one=False):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, args)
    data = cursor.fetchall()
    conn.commit()
    conn.close()
    return (data[0] if data else None) if one else data



@app.route("/")
def index():
    employees = query_db("SELECT * FROM employees")
    roles = query_db("SELECT * FROM employee_role")
    return render_template("index3.html", employees=employees, roles=roles)


@app.route("/edit/<int:emp_id>")
def edit_employee(emp_id):
    employee = query_db("SELECT * FROM employees WHERE id=?", (emp_id,), one=True)
    roles = query_db("SELECT * FROM employee_role")
    return render_template("update.html", employee=employee, roles=roles)



@app.route("/api/employees", methods=["GET"])
def api_get_employees():
    rows = query_db("SELECT * FROM employees")
    return jsonify([dict(r) for r in rows])


# Add employee
@app.route("/api/employees", methods=["POST"])
def api_add_employee():
    data = request.json
    query_db("INSERT INTO employees (name, role, salary) VALUES (?, ?, ?)",
             (data["name"], data["role"], data["salary"]))
    return jsonify({"message": "Employee added"}), 201


# Update employee
@app.route("/api/employees/<int:emp_id>", methods=["PUT"])
def api_update_employee(emp_id):
    data = request.json
    query_db("UPDATE employees SET name=?, role=?, salary=? WHERE id=?",
             (data["name"], data["role"], data["salary"], emp_id))
    return jsonify({"message": "Employee updated"})


# Delete employee
@app.route("/api/employees/<int:emp_id>", methods=["DELETE"])
def api_delete_employee(emp_id):
    query_db("DELETE FROM employees WHERE id=?", (emp_id,))
    return jsonify({"message": "Employee deleted"})



@app.route("/api/roles", methods=["GET"])
def api_get_roles():
    rows = query_db("SELECT * FROM employee_role")
    return jsonify([dict(r) for r in rows])


@app.route("/api/roles", methods=["POST"])
def api_add_role():
    data = request.json
    query_db("INSERT INTO employee_role (role_name) VALUES (?)", (data["role_name"],))
    return jsonify({"message": "Role added"}), 201


if __name__ == "__main__":
    app.run(debug=True)
