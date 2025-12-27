from flask import Flask, render_template, request
import csv
app = Flask(__name__)

# FUNCTION: Find student by Fingerprint ID
def get_student_by_id(search_id):
    try:
        with open('student.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['fingerprint_id'] == search_id:
                    return row
                
    except FileNotFoundError:
        return None
    return None

@app.route('/', methods=['GET', 'POST'])
def home():
    student = None
    error = None
    
    if request.method == 'POST':
        f_id = request.form['fingerprint_id']
        student = get_student_by_id(f_id)
        
        if not student:
            error = "NO MATCH FOUND! possible impersonater."
    return render_template('index.html', student=student, error=error)
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000, debug=True)
    
    
        