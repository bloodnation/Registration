from flask import Flask, request, jsonify, send_file
import sqlite3
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime
import re
from flask import Flask, request, jsonify, send_file, render_template  # Add render_template here

app = Flask(__name__)

# Route for the root URL
@app.route('/')
def index():
    return render_template('index.html')  # Serve the index.html file

# Database setup
def get_db_connection():
    conn = sqlite3.connect('student_registration.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

# Create the students table if it doesn't exist
def initialize_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            mobile TEXT NOT NULL UNIQUE,
            id_number TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            gender TEXT NOT NULL,
            residence TEXT NOT NULL,
            emergency_contact1 TEXT NOT NULL,
            emergency_contact2 TEXT NOT NULL,
            course TEXT NOT NULL,
            registration_number TEXT NOT NULL UNIQUE,
            UNIQUE(id_number, course)
        )
    ''')
    conn.commit()
    conn.close()

# Validate mobile number
def validate_mobile(mobile):
    return re.match(r'^\+?[0-9]{10,15}$', mobile)

# Validate email
def validate_email(email):
    return re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email)

# Generate a unique registration number
def generate_registration_number(course):
    prefix = "IYFT4"
    course_mapping = {
        "Computer Programming": "CP",
        "Welding": "WD",
        "Computer Packages": "PK",
        "Chinese": "CH",
        "Mind Education": "ME",
        "Hair Dressing": "HD",
        "Beauty": "BT",
        "Barbering": "BB",
        "Theology": "TH",
        "Dance": "DN",
        "Sign Language": "SL",
        "Electrical Installation": "EI",
        "Videography": "VG",
        "Photography": "PH"
    }
    course_code = course_mapping.get(course, "OT")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM students WHERE course = ?', (course,))
    count = cursor.fetchone()[0] + 1
    conn.close()
    unique_number = str(count).zfill(4)
    return f"{prefix}{course_code}{unique_number}"

# Check if a student is already registered
def is_student_registered(id_number, email, mobile, course=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = '''
    SELECT COUNT(*) FROM students 
    WHERE id_number = ? OR email = ? OR mobile = ?
    '''
    params = (id_number, email, mobile)
    if course:
        query += ' OR (id_number = ? AND course = ?)'
        params = (id_number, email, mobile, id_number, course)
    cursor.execute(query, params)
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0

# Register a new student
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('name')
    mobile = data.get('mobile')
    id_number = data.get('id_number')
    email = data.get('email')
    gender = data.get('gender')
    residence = data.get('residence')
    emergency1 = data.get('emergency1')
    emergency2 = data.get('emergency2')
    course = data.get('course')

    if not all([name, mobile, id_number, email, gender, residence, emergency1, emergency2, course]):
        return jsonify({"success": False, "message": "Please fill all fields"}), 400

    if not validate_mobile(mobile):
        return jsonify({"success": False, "message": "Invalid mobile number"}), 400

    if not validate_email(email):
        return jsonify({"success": False, "message": "Invalid email address"}), 400

    if is_student_registered(id_number, email, mobile, course):
        return jsonify({"success": False, "message": "Student is already registered!"}), 400

    registration_number = generate_registration_number(course)
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
        INSERT INTO students (name, mobile, id_number, email, gender, residence, emergency_contact1, emergency_contact2, course, registration_number)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, mobile, id_number, email, gender, residence, emergency1, emergency2, course, registration_number))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": f"Student registered successfully! Registration Number: {registration_number}"}), 200
    except sqlite3.IntegrityError as e:
        conn.close()
        if "UNIQUE constraint failed: students.id_number" in str(e):
            return jsonify({"success": False, "message": "A student with this ID number is already registered!"}), 400
        elif "UNIQUE constraint failed: students.email" in str(e):
            return jsonify({"success": False, "message": "This email is already associated with another student!"}), 400
        elif "UNIQUE constraint failed: students.mobile" in str(e):
            return jsonify({"success": False, "message": "This mobile number is already registered!"}), 400
        elif "UNIQUE constraint failed: students.id_number, students.course" in str(e):
            return jsonify({"success": False, "message": "This student is already registered!"}), 400
        else:
            return jsonify({"success": False, "message": "An error occurred during registration."}), 500

# Check registration status
@app.route('/check-registration', methods=['POST'])
def check_registration():
    data = request.json
    id_number = data.get('id_number')
    email = data.get('email')
    mobile = data.get('mobile')

    if not any([id_number, email, mobile]):
        return jsonify({"success": False, "message": "Please provide an ID number, email, or mobile number to check."}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT name, course, registration_number FROM students 
    WHERE id_number = ? OR email = ? OR mobile = ?
    ''', (id_number, email, mobile))
    result = cursor.fetchone()
    conn.close()

    if result:
        return jsonify({"success": True, "message": f"Student is already registered! Name: {result['name']}, Course: {result['course']}, Reg No: {result['registration_number']}"}), 200
    else:
        return jsonify({"success": True, "message": "Student is not registered."}), 200

# Export data to JSON
@app.route('/export-json', methods=['GET'])
def export_json():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT name, mobile, course, registration_number FROM students", conn)
    conn.close()
    output = BytesIO()
    df.to_json(output, orient="records")
    output.seek(0)
    return send_file(output, as_attachment=True, download_name='students.json', mimetype='application/json')

# Export data to Excel
@app.route('/export-excel', methods=['GET'])
def export_excel():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT name, mobile, course, registration_number FROM students", conn)
    conn.close()
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)
    return send_file(output, as_attachment=True, download_name='students.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

# Export data to PDF
@app.route('/export-pdf', methods=['GET'])
def export_pdf():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT name, mobile, course, registration_number FROM students", conn)
    conn.close()
    output = BytesIO()
    c = canvas.Canvas(output, pagesize=letter)
    c.setFont("Helvetica", 12)
    y = 750
    c.drawString(50, y, "Student Registration Data")
    y -= 30
    for index, row in df.iterrows():
        c.drawString(50, y, f"Name: {row['name']}, Mobile: {row['mobile']}, Course: {row['course']}, Reg No: {row['registration_number']}")
        y -= 20
        if y < 50:
            c.showPage()
            y = 750
    c.save()
    output.seek(0)
    return send_file(output, as_attachment=True, download_name='students.pdf', mimetype='application/pdf')

# Initialize the database when the app starts
initialize_db()

# if __name__ == '__main__':
#     app.run(debug=True)