from flask import Flask, render_template, Response, request, redirect, url_for, session, flash
import cv2
import face_recognition
import mysql.connector
import pickle
import numpy as np
from scipy.spatial import distance as dist
app = Flask(__name__)
app.secret_key = "super_secret_key" 

# --- CONFIGURATION ---
db_config = {
    'host': "localhost",
    'user': "root",
    'password': "1234",  
    'database': "exam_guard"
}

ADMIN_USER = "admin"
ADMIN_PASS = "12345"
current_user_name = "Unknown"

def get_db():
    try: return mysql.connector.connect(**db_config)
    except: return None

def get_all_students():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT student_id, name FROM students")
        data = cursor.fetchall()
        conn.close()
        return data
    except: return []

def get_ear(eye):
    # Calculate the vertical distances (between eyelids)
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])

    # Calculate the horizontal distance (width of eye)
    C = dist.euclidean(eye[0], eye[3])

    # Calculate the Eye Aspect Ratio (EAR)
    ear = (A + B) / (2.0 * C)
    return ear
    
    

def gen_frames(target_encoding):
    camera = cv2.VideoCapture(0)
    blink_detected = False # Flag to track if user has blinked
    
    while True:
        success, frame = camera.read()
        if not success:
            break
            
        # Resize for speed
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # 1. Find Face Locations & Landmarks
        face_locations = face_recognition.face_locations(rgb_small_frame)
        
        # Only process if a face is found
        if face_locations:
            # We assume the main face is the user
            face_landmarks_list = face_recognition.face_landmarks(rgb_small_frame, face_locations)
            
            # Check for Blink (Liveness)
            if not blink_detected:
                for face_landmark in face_landmarks_list:
                    left_eye = face_landmark['left_eye']
                    right_eye = face_landmark['right_eye']

                    # Calculate EAR for both eyes
                    leftEAR = get_ear(left_eye)
                    rightEAR = get_ear(right_eye)
                    
                    # Average the two eyes
                    ear = (leftEAR + rightEAR) / 2.0

                    # IF EAR is below 0.2, the eyes are closed (Blink!)
                    if ear < 0.2:
                        blink_detected = True
                
                # Draw "Please Blink" message
                cv2.putText(frame, "PLEASE BLINK TO VERIFY", (50, 50), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            else:
                # 2. Blink Confirmed! Now we check identity
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                
                match_found = False
                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces([target_encoding], face_encoding)
                    if True in matches:
                        match_found = True
                        break
                
                if match_found:
                    # Draw Green Box & Success
                    top, right, bottom, left = face_locations[0]
                    # Scale back up (since we resized by 0.25)
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4
                    
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    cv2.putText(frame, "LIVENESS CONFIRMED: Verified", (50, 50), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                    
                    # OPTIONAL: You can auto-redirect here if you want
                    # return redirect(url_for('exam')) 
                else:
                    cv2.putText(frame, "Face Not Recognized", (50, 50), 
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        else:
            # No face detected at all
            blink_detected = False # Reset if they look away

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
# --- ROUTES ---
@app.route('/')
def home(): return render_template('login.html')

@app.route('/verify', methods=['POST'])
def verify():
    global current_user_name
    student_id = request.form['student_id']
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name, face_encoding FROM students WHERE student_id=%s", (student_id,))
    res = cursor.fetchone()
    conn.close()
    if res:
        current_user_name = res[0]
        app.config['TARGET'] = pickle.loads(res[1])
        return render_template('verify.html', name=res[0])
    return "<h3>❌ ID Not Found</h3>"

@app.route('/video_feed')
def video_feed(): return Response(gen_frames(app.config.get('TARGET')), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/exam')
def exam(): return render_template('exam.html', name=current_user_name)

@app.route('/admin')
def admin(): return render_template('admin_login.html')

# FIX 1: Add the comma between 'GET' and 'POST'
@app.route('/admin_login', methods=['GET', 'POST']) 
def admin_login():
    # FIX 2: Remove 'pass' and put the logic INSIDE the if block
    if request.method == 'POST':
        # Now this only happens when you click "Login"
        if request.form.get('username') == 'admin' and request.form.get('password') == '1234':
            session['admin'] = True
            return redirect(url_for('dashboard'))
        else:
            return "<h3>❌ Wrong Password</h3>"
    
    # This runs if it's a GET request (Showing the form)
    return render_template('admin_login.html')

@app.route('/dashboard')
def dashboard():
    # We removed the login check so you can access it easily for now.
    
    # IMPORTANT: Ensure this matches the filename in your VS Code folder!
    # In your screenshot, you named it "my_dashboard.html"
    return render_template('my_dashboard.html', students=get_all_students())
    
@app.route('/delete_student/<string:sid>', methods=['GET'])
def delete_student(sid):
    # 1. Open the connection with the name 'conn'
    conn = get_db()
    cursor = conn.cursor()

    # 2. Run the Delete
    cursor.execute("DELETE FROM students WHERE student_id=%s", (sid,))
    
    # 3. Check if it worked (Debugging)
    deleted_count = cursor.rowcount
    print(f"------------")
    print(f"ATTEMPTING TO DELETE: {sid}")
    print(f"ROWS DELETED: {deleted_count}")
    
    # 4. SAVE THE CHANGE (Use 'conn' here!)
    conn.commit() 
    conn.close()

    # 5. Report back
    if deleted_count > 0:
        flash("Student Deleted Successfully!", "success")
    else:
        flash("Error: Student ID not found.", "danger")

    return redirect(url_for('dashboard'))

# --- THE FIX: SMART UPLOAD HANDLER ---
@app.route('/add_new_student', methods=['GET', 'POST'])
@app.route('/add_student', methods=['GET', 'POST']) 
def add_new_student():
    # 1. REMOVED LOGIN CHECK FOR TESTING
    
    if request.method == 'POST':
        print("---DEBUGGING FORM DATA---")
        print(request.form)
        print("--------------------------------")
        student_id = request.form.get('student_id') 
        name = request.form.get('full_name')
        if not student_id or not name:
            return "Error: Please provide both student ID and name", 404
        
        # --- THE FIX: FIND ANY FILE ---
        # We don't care if it's named 'file', 'photo', or 'banana'. 
        # We just grab the first file we find.
        file = None
        if len(request.files) > 0:
            # Get the first available file key
            first_key = next(iter(request.files))
            file = request.files[first_key]
            print(f"✅ FOUND FILE! The HTML named it: '{first_key}'")
        else:
            print("❌ ERROR: Request.files is EMPTY. This means HTML 'enctype' is definitely missing or browser cached.")
            return "Error: No file found. Please Hard Refresh (Ctrl+Shift+R)."

        if file.filename == '': return "Error: No selected file"

        try:
            image = face_recognition.load_image_file(file)
            encodings = face_recognition.face_encodings(image)
            print("-----------------------------")
            print(f"FACE FOUND: {len(encodings)}")
            print("--------------------------------")
            if len(encodings) > 0:
                blob = pickle.dumps(encodings[0])
                conn = get_db()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO students (student_id, name, face_encoding) VALUES (%s, %s, %s)", (student_id, name, blob))
                conn.commit()
                conn.close()
                return redirect(url_for('dashboard'))
            else:
                return "<h3>❌ No face detected! <a href='/add_new_student'>Try Again</a></h3>"
        except Exception as e:
            return f"Error: {e}"

    # Try to load the new file name first, if not found, load the old one
    try:
        return render_template('register_student.html')
    except:
        return render_template('add_student.html')

if __name__ == '__main__':
    app.run(debug=True,)