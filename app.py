from flask import Flask, render_template, request, redirect, session
from db_config import get_database_connection

app = Flask(__name__)
app.secret_key = "secret123"


# =========================
# LOGIN
# =========================
@app.route('/login', methods=['GET', 'POST'])
def login():

    print("LOGIN FUNCTION CALLED")

    if request.method == 'POST':

        print("POST REQUEST RECEIVED")

        username = request.form['username']
        password = request.form['password']

        print("Username:", username)
        print("Password:", password)

        try:
            connection = get_database_connection()
            cursor = connection.cursor(dictionary=True)

            cursor.execute("""
                SELECT *
                FROM users
                WHERE username = %s AND password = %s
            """, (username, password))

            user = cursor.fetchone()

            cursor.close()
            connection.close()

            if user:
                session['user_id'] = user['user_id']
                session['full_name'] = user['full_name']
                return redirect('/')
            else:
                return render_template('login.html', error="Invalid Username or Password")

        except Exception as e:
            return f"ERROR: {e}"

    return render_template('login.html', error=None)


# =========================
# LOGOUT (FIXED)
# =========================
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


# =========================
# DASHBOARD
# =========================
@app.route('/')
def home():

    if 'user_id' not in session:
        return redirect('/login')

    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM attendance")
    total_attendance = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tasks")
    total_tasks = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM student_tasks")
    total_assignments = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return render_template(
        'index.html',
        total_students=total_students,
        total_attendance=total_attendance,
        total_tasks=total_tasks,
        total_assignments=total_assignments
    )


# =========================
# ADD STUDENT
# =========================
@app.route('/add_student/', methods=['GET', 'POST'])
def add_student():

    if 'user_id' not in session:
        return redirect('/login')

    if request.method == 'POST':

        connection = get_database_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO students (
                first_name, last_name, gender,
                mobile_number, email, course_name,
                admission_date
            )
            VALUES (%s, %s, %s, %s, %s, %s, CURDATE())
        """, (
            request.form['first_name'],
            request.form['last_name'],
            request.form['gender'],
            request.form['mobile_number'],
            request.form['email'],
            request.form['course_name']
        ))

        connection.commit()
        cursor.close()
        connection.close()

        return redirect('/students')

    return render_template('add_student.html')


# =========================
# STUDENTS
# =========================
@app.route('/students')
def students():

    if 'user_id' not in session:
        return redirect('/login')

    connection = get_database_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('students.html', students=data)


# =========================
# ATTENDANCE
# =========================
@app.route('/attendance')
def attendance():

    if 'user_id' not in session:
        return redirect('/login')

    connection = get_database_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('attendance.html', students=students)


@app.route('/save_attendance', methods=['POST'])
def save_attendance():

    if 'user_id' not in session:
        return redirect('/login')

    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO attendance (student_id, attendance_date, attendance_status)
        VALUES (%s, CURDATE(), %s)
    """, (
        request.form['student_id'],
        request.form['attendance_status']
    ))

    connection.commit()
    cursor.close()
    connection.close()

    return redirect('/attendance_report')


@app.route('/attendance_report')
def attendance_report():

    if 'user_id' not in session:
        return redirect('/login')

    connection = get_database_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT a.*, s.first_name, s.last_name, s.course_name
        FROM attendance a
        INNER JOIN students s ON a.student_id = s.student_id
        ORDER BY a.attendance_id DESC
    """)

    data = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('attendance_report.html', attendance_records=data)


# =========================
# TASKS
# =========================
@app.route('/add_task', methods=['GET', 'POST'])
def add_task():

    if 'user_id' not in session:
        return redirect('/login')

    if request.method == 'POST':

        connection = get_database_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO tasks (task_name, task_description, maximum_marks)
            VALUES (%s, %s, %s)
        """, (
            request.form['task_name'],
            request.form['task_description'],
            request.form['maximum_marks']
        ))

        connection.commit()
        cursor.close()
        connection.close()

        return redirect('/tasks')

    return render_template('add_task.html')


@app.route('/tasks')
def tasks():

    if 'user_id' not in session:
        return redirect('/login')

    connection = get_database_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM tasks ORDER BY task_id DESC")
    data = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('tasks.html', tasks=data)


# =========================
# LOGIC END
# =========================

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)