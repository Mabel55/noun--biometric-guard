from app import app, db, Student

def add_new_student():
    print("ADD NEW STUDENT TO DATABASE")
    
    # Ask for detail
    s_id = input("ENTER ID NUMBER (e.g. 100): ")
    s_name = input("Enter Full Name:")
    s_dept = input("Enter Department")
    s_level = input("Enter Level (e.g 100 level): ")
    
    #Auto save the image name based on ID
    s_image = f"{s_id}.jpg"
    
    # save to database
    with app.app_context():
        # check if identity already exists
        existing = Student.query.get(s_id)
        if existing:
            print(f" Error ID {s_id} already exists!")
            return
        
        # create new student
        new_student = Student(
            id=s_id,
            name=s_name,
            dept=s_dept,
            level=s_level,
            image=s_image
        )
    
        
        
        db.session.add(new_student)
        db.session.commit()
        print(f"SUCCESS: {s_name} has been added to the database!")
        
if __name__ == "__main__":
    add_new_student()