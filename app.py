import cv2
import face_recognition
import os
import datetime
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

app = Flask(__name__)

# --- CONFIGURATION ---
app.secret_key = "ExamGuardSecretKey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static'
db = SQLAlchemy(app)

# --- DATABASE MODELS ---
class Student(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    dept = db.Column(db.String(100), nullable=False)
    level = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(50), nullable=False)

class AccessLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(50))
    student_id = db.Column(db.String(50))
    status = db.Column(db.String(50))

# --- LOGGING FUNCTION ---
def log_access(student_id, status):
    """Saves the event to the SQL Database."""
    try:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_log = AccessLog(timestamp=now, student_id=student_id, status=status)
        db.session.add(new_log)
        db.session.commit()
        print(f"📝 Log saved: {student_id} - {status}")
    except Exception as e:
        print(f"⚠️ Error saving log: {e}")

# --- IMPROVED FACE VERIFICATION ---
def verify_face(student_id):
    photo_filename = os.path.join('static', f"{student_id}.jpg")
    
    # 1. Log if Photo Missing
    if not os.path.exists(photo_filename): 
        log_access(student_id, "FAILED - No Photo on File")
        return False

    try:
        student_image = face_recognition.load_image_file(photo_filename)
        student_encodings = face_recognition.face_encodings(student_image)
        if len(student_encodings) == 0: 
            log_access(student_id, "FAILED - Bad ID Photo")
            return False
        known_face_encoding = student_encodings[0]
    except:
        return False

    # LIVE CAMERA
    print("📸 Opening Camera...")
    camera = cv2.VideoCapture(0)
    if not camera.isOpened(): return False
    
    found_face_frame = None
    while True:
        ret, frame = camera.read()
        if not ret: break
        cv2.putText(frame, "Press SPACE to Verify", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Exam Guard Verification", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == 32: 
            found_face_frame = frame
            break
        elif key == ord('q'):
            camera.release()
            cv2.destroyAllWindows()
            log_access(student_id, "CANCELLED by User")
            return False
            
    camera.release()
    cv2.destroyAllWindows()
    
    # 2. Log if No Face in Camera
    if found_face_frame is None: 
        log_access(student_id, "CANCELLED - No Capture")
        return False

    rgb_frame = cv2.cvtColor(found_face_frame, cv2.COLOR_BGR2RGB)
    live_face_encodings = face_recognition.face_encodings(rgb_frame)
    
    if len(live_face_encodings) == 0: 
        log_access(student_id, "DENIED - No Face Detected")
        return False

    match = face_recognition.compare_faces([known_face_encoding], live_face_encodings[0])
    
    # Get Student Name
    student = Student.query.get(student_id)
    student_name = student.name if student else student_id

    if match[0]:
        log_access(student_name, "AUTHORIZED")
        return True
    else:
        log_access(student_name, "DENIED - Face Mismatch")
        return False

# --- ROUTES ---

@app.route('/', methods=['GET', 'POST'])
def home():
    student_info = None
    error_message = None
    if request.method == 'POST':
        search_id = request.form.get('id_number')
        found_student = Student.query.get(search_id)
        
        if found_student:
            if verify_face(search_id):
                student_info = found_student
            else:
                error_message = "❌ ACCESS DENIED: Face did not match."
        else:
            # 3. Log if ID doesn't exist
            log_access(search_id, "DENIED - Invalid ID")
            error_message = "⚠️ ID Not Found in Database."
            
    return render_template('index.html', student=student_info, error=error_message)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] == "admin" and request.form['password'] == "mabel123":
            session['logged_in'] = True
            return redirect(url_for('admin_panel'))
        else:
            error = "❌ Invalid Credentials"
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/admin')
def admin_panel():
    if not session.get('logged_in'): return redirect(url_for('login'))
    
    all_students = Student.query.all()
    # Fetch the logs (Show last 15)
    all_logs = AccessLog.query.order_by(AccessLog.id.desc()).limit(15).all()
    
    return render_template('admin.html', students=all_students, logs=all_logs)

@app.route('/add_student', methods=['POST'])
def add_student():
    if not session.get('logged_in'): return redirect(url_for('login'))
    
    id_num = request.form['id']
    name = request.form['name']
    dept = request.form['dept']
    level = request.form['level']
    
    if Student.query.get(id_num): return "❌ ID exists!"
    
    if 'photo' in request.files:
        file = request.files['photo']
        if file.filename != '':
            filename = f"{id_num}.jpg"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new_student = Student(id=id_num, name=name, dept=dept, level=level, image=filename)
            db.session.add(new_student)
            db.session.commit()
            
    return redirect(url_for('admin_panel'))

@app.route('/delete/<id>')
def delete_student(id):
    if not session.get('logged_in'): return redirect(url_for('login'))
    student = Student.query.get(id)
    if student:
        db.session.delete(student)
        db.session.commit()
        try: os.remove(os.path.join(app.config['UPLOAD_FOLDER'], student.image))
        except: pass
    return redirect(url_for('admin_panel'))

if __name__ == '__main__':
    with app.app_context(): db.create_all()
    app.run(debug=True)