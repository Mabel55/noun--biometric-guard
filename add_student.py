import cv2
import face_recognition
import mysql.connector
import pickle
import sys

# --- CONFIGURATION ---
DB_HOST = "localhost"
DB_USER = "root"
DB_PASS = "1234"  # <--- CHANGE THIS TO YOUR WORKBENCH PASSWORD
DB_NAME = "exam_guard"

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )
        return conn
    except mysql.connector.Error as err:
        print(f"❌ Connection Error: {err}")
        sys.exit()

def create_table_if_not_exists():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Create the table safely if it is missing
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id VARCHAR(50) PRIMARY KEY,
            name VARCHAR(100),
            face_encoding BLOB
        )
    """)
    conn.commit()
    conn.close()
    print("✅ Database check complete (Table 'students' is ready).")

def register_student():
    # 1. Ensure Table Exists
    create_table_if_not_exists()
    
    # 2. Input Details
    print("\n--- 🆕 NEW STUDENT REGISTRATION ---")
    name = input("Enter Student Name: ")
    student_id = input("Enter Matric Number/ID: ")

    # 3. Open Camera
    print("\n📷 Opening Camera... Please look at the lens.")
    print("Press 's' to SNAP and SAVE.")
    print("Press 'q' to QUIT.")
    
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Could not open webcam.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow('Register Student - Press "s" to Save', frame)
        key = cv2.waitKey(1) & 0xFF
        
        # SAVE logic
        if key == ord('s'):
            print("📸 Capturing face...")
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            encodings = face_recognition.face_encodings(rgb_frame)

            if len(encodings) > 0:
                face_data = encodings[0]
                face_blob = pickle.dumps(face_data) # Convert math to bytes

                # Save to MySQL
                try:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    sql = "INSERT INTO students (student_id, name, face_encoding) VALUES (%s, %s, %s)"
                    val = (student_id, name, face_blob)
                    cursor.execute(sql, val)
                    conn.commit()
                    conn.close()
                    print(f"\n✅ SUCCESS! {name} has been registered!")
                except mysql.connector.Error as err:
                    print(f"\n❌ SQL Error: {err}")
                
                break 
            else:
                print("⚠️ No face detected! Try again.")

        # QUIT logic
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    register_student()