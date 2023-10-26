from flask import Flask, render_template, request, redirect, url_for
import pyodbc

    
app = Flask(__name__)


# Database Configuration
server = 'assignment2.cpxppv3byklb.us-east-2.rds.amazonaws.com'
database = 'assignment2'
username = 'admin'
password = 'Greenplanet1!'
conn = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}')
cursor = conn.cursor()
print("connected")

@app.route('/')
def index():
    return render_template('enter.html')

@app.route('/enter', methods=['GET', 'POST'])
def enter_grade():
    if request.method == 'POST':
        student_id = request.form['student_id']
        grade = request.form['grade']
        cursor.execute("INSERT INTO StudentsGrades (ID, Grade) VALUES (?, ?);", student_id, grade)
        conn.commit()
    return render_template('enter.html')

@app.route('/display')
def display_grades():
    cursor.execute("SELECT ID, Grade FROM StudentsGrades")
    data = cursor.fetchall()
    print(data)  # Add this line to check the data in the console
    average_grade = sum(float(row.Grade) for row in data) / len(data) if data else 0
    return render_template('display.html', data=data, average_grade=average_grade)

if __name__ == '__main__':
    app.run(debug=True)
