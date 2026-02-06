# 🛡️ Biometric Exam Guard

> **A Secure, AI-Powered Student Verification System for Anti-Impersonation in Examinations.**

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-Web_Framework-red?style=for-the-badge&logo=flask)
![MySQL](https://img.shields.io/badge/MySQL-Database-orange?style=for-the-badge&logo=mysql)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer_Vision-green?style=for-the-badge&logo=opencv)

## 📖 Overview
**Biometric Exam Guard** is a multi-factor authentication system designed to eliminate examination malpractice (specifically impersonation) in educational institutions. 

Unlike traditional ID card checks, this system uses **Facial Recognition** combined with **Liveness Detection (Blink Verification)** to ensure that the student physically present at the computer is the actual registered candidate.

This project was developed as a Final Year Project for the **Department of Computer Science, National Open University of Nigeria (NOUN)**.

---

## 🚀 Key Features

### 1. 👤 Student Registration & Encoding
* Captures student details (Matric No, Name).
* Uses **dlib** to generate a unique 128-dimensional face encoding.
* Stores encodings securely as BLOB data in a **MySQL** database.

### 2. 👁️ Liveness Detection (Anti-Spoofing)
* **Prevents photo attacks:** Users cannot simply hold up a picture of a student.
* **Eye Aspect Ratio (EAR):** The system calculates the distance between eyelids using `scipy.spatial` and facial landmarks.
* **Logic:** Access is denied until the user blinks naturally, proving they are a live human.

### 3. 🔐 Real-Time Verification
* Connects to the webcam using **OpenCV**.
* Matches live video feed against the database in real-time.
* **Green Box:** Identity Verified (Access Granted).
* **Red Warning:** Unknown Face (Access Denied).

### 4. 🎓 Exam Portal Integration
* Automatically redirects verified students to the secure exam interface.
* Prevents unauthorized access to question papers.

---

## 🛠️ Technology Stack

* **Backend:** Python (Flask)
* **Database:** MySQL (XAMPP/WAMP)
* **Computer Vision:** OpenCV (`cv2`), `face_recognition`, `dlib`
* **Data Processing:** NumPy, SciPy (for Euclidean distance math)
* **Frontend:** HTML5, CSS3, Bootstrap 4, JavaScript

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/biometric-exam-guard.git](https://github.com/your-username/biometric-exam-guard.git)
cd biometric-exam-guard