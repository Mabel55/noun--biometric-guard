import mysql.connector

db_config = {
    'host': "localhost",
    'user': "root",
    
    'password': "1234",  
    'database': "exam_guard"
}

try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    
    # Create the table if it is missing
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id VARCHAR(50) PRIMARY KEY,
            name VARCHAR(100),
            face_encoding BLOB
        )
    """)
    conn.commit()
    print("✅ SUCCESS: Database Table is Ready!")
    conn.close()
except Exception as e:
    print(f"❌ Error: {e}")