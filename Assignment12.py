from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect
import sqlite3 as lite

app = Flask(__name__)

USER = "admin"
PASSWORD = "password"

def get_db_connection():
    """ Connect to SQLite database """
    conn = lite.connect('studentquizzes.db')
    conn.row_factory = lite.Row
    return conn


@app.route('/')
def root():
    return render_template("login.html", message=None)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form["user"]
        password = request.form["password"]
        
        if username == USER and password == PASSWORD:
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", message = "Incorrect username or password")
    else:
        return render_template("login.html", message=None)



@app.route('/dashboard')
def dashboard():
    quizzes_qry = "select quizid, subject, num_questions, quiz_date from quizzes"
    results_qry = "select studentid, quizid, score from results"
    
    conn = get_db_connection()
    students = conn.execute("select id, first_name, last_name from students").fetchall()
    quizzes_dataset = conn.execute(quizzes_qry).fetchall()
    
    quizresults = conn.execute(results_qry).fetchall()
    
    return render_template("dashboard.html", students = students, quizzes = quizzes_dataset, results = quizresults)


@app.route('/addstudent', methods=['POST', 'GET'])
def add_student():
    if request.method == 'POST':
        firstname = request.form["first_name"]
        lastname = request.form["last_name"]

        conn = get_db_connection()
        conn.execute("INSERT INTO students(first_name, last_name) VALUES(?, ?);", (firstname, lastname))
        conn.commit()

        return redirect(url_for("dashboard"))
    else:
        return render_template("add_student.html")
    
    
@app.route('/deletestudent/<student_id>')
def delete_student(student_id):
    conn = get_db_connection()
    conn.execute("DELETE from students where id = (?);", (student_id,))
    conn.commit()
    return redirect(url_for("dashboard"))



@app.route('/addquiz', methods=['POST', 'GET'])
def add_quiz():
    if request.method == 'POST':
        subject = request.form["subject"]
        questions = request.form["num_questions"]
        date = request.form["quiz_date"]

        conn = get_db_connection()
        conn.execute("INSERT INTO quizzes(subject, num_questions, quiz_date) VALUES(?, ?, ?);", (subject, questions, date))
        conn.commit()

        return redirect(url_for("dashboard"))
    else:
        return render_template("add_quiz.html")
    
    
@app.route('/deletequiz/<quiz_id>')
def delete_quiz(quiz_id):
    conn = get_db_connection()
    conn.execute("DELETE from quizzes where quizid = (?);", (quiz_id,))
    conn.commit()
    return redirect(url_for("dashboard"))


@app.route('/viewresults/<quiz_id>')
def view_quiz_results(quiz_id):

    conn = get_db_connection()
    quiz = conn.execute("select subject, num_questions, quiz_date from quizzes WHERE quizid = (?);", (quiz_id,)).fetchone()
    quiz_results = conn.execute(
        "SELECT s.first_name, s.last_name, score FROM results r join students s "
        "on r.studentid = s.id where r.quizid = (?);", (quiz_id,)).fetchall()

    return render_template("quiz_results.html", quiz=quiz, results=quiz_results)


@app.route('/addresults', methods=['POST', 'GET'])
def add_quiz_results():
    if request.method == 'POST':
        student_id = request.form["studentid"]
        quiz_id = request.form["quizid"]
        score = request.form["score"]

        conn = get_db_connection()
        conn.execute("INSERT INTO results(studentid, quizid, score) VALUES(?, ?, ?);", (student_id, quiz_id, score))
        conn.commit()

        return redirect(url_for("dashboard"))
    else:
        return render_template("add_results.html")
    
@app.route('/deleteresult/<quiz_id>')
def delete_quiz_results(quiz_id):
    conn = get_db_connection()
    conn.execute("DELETE from results where quizid = (?);", (quiz_id,))
    conn.commit()
    return redirect(url_for("dashboard"))





if __name__ == '__main__':
    app.run(debug=True)