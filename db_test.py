import mysql.connector

# CONNECT
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",  
    database="exam_guard"
)
cursor = conn.cursor()

# 1. DISABLE CHECKS (Unlock the door)
cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

# 2. DELETE THE TABLES
cursor.execute("DROP TABLE IF EXISTS students")
cursor.execute("DROP TABLE IF EXISTS attendance_logs") # Deleting this too just in case!

# 3. RE-ENABLE CHECKS (Lock the door)
cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

conn.commit()
print("✅ SUCCESS: Old tables deleted! The database is clean.")