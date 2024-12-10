from flask import Flask, request, jsonify
import sqlite3
import os
from dotenv import load_dotenv  
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            class TEXT NOT NULL,
            average REAL NOT NULL,
            notes TEXT
        )
    """)
    conn.commit()
    conn.close()

@app.route('/add_student', methods=['POST'])
def add_student():
    data = request.json
    first_name = data['first_name']
    last_name = data['last_name']
    student_class = data['class']
    average = data['average']
    notes = data.get('notes', '')

    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO students (first_name, last_name, class, average, notes)
        VALUES (?, ?, ?, ?, ?)
    """, (first_name, last_name, student_class, average, notes))
    conn.commit()
    conn.close()

    return jsonify({'message': 'تمت إضافة الطالب بنجاح'}), 201

@app.route('/search_student', methods=['GET'])
def search_student():
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')

    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT first_name, last_name, class, average, notes
        FROM students WHERE first_name = ? AND last_name = ?
    """, (first_name, last_name))
    student = cursor.fetchone()
    conn.close()

    if student:
        return jsonify({
            'first_name': student[0],
            'last_name': student[1],
            'class': student[2],
            'average': student[3],
            'notes': student[4]
        })
    else:
        return jsonify({'message': 'الطالب غير موجود.'}), 404

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
