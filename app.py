from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def connect():
    return sqlite3.connect("database/students.db")

@app.route("/")
def home():
    conn = connect()
    students = conn.execute("SELECT * FROM students").fetchall()
    conn.close()
    return render_template("index.html", students=students)

@app.route("/add", methods=["GET","POST"])
def add():
    if request.method == "POST":
        name = request.form["name"]
        dept = request.form["dept"]

        conn = connect()
        conn.execute(
            "INSERT INTO students(name,dept) VALUES (?,?)",
            (name,dept)
        )
        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("add.html")

@app.route("/delete/<int:id>")
def delete(id):
    conn = connect()
    conn.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect("/")

if __name__ == "__main__":
    conn = connect()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        dept TEXT
    )
    """)

    conn.commit()
    conn.close()

    app.run(debug=True)
