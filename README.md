#  Exam Guard - Biometric Exam Verification System

**Exam Guard** is a full-stack security application designed to prevent exam malpractice using facial recognition technology. It verifies student identities in real-time by comparing live webcam footage with a secure database of registered student profiles.

##  Key Features
* **Facial Recognition:** Uses the `face_recognition` library to verify identity with high accuracy.
* **Live Webcam Integration:** Captures real-time video for instant verification.
* **Secure Admin Dashboard:** Password-protected panel to manage student records.
* **Student Database:** Stores profiles (Name, ID, Department, Level, Photo) using SQLite.
* **Activity Logging:** Tracks and saves a history of all authorized and denied attempts.
* **Modern UI:** Responsive, user-friendly interface with visual feedback (Green for Verified, Red for Denied).

## Tech Stack
* **Backend:** Python, Flask
* **Database:** SQLAlchemy (SQLite)
* **AI/ML:** OpenCV, Face Recognition API
* **Frontend:** HTML5, CSS3

## ⚙️ How to Run
1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Run the Application:**
    ```bash
    python app.py
    ```
3.  **Open in Browser:**
    Go to `http://127.0.0.1:5000`

## 👤 Admin Access
* **URL:** `/admin`
* **Default Username:** `admin`
* **Default Password:** `mabel123`

---
*Created by Mabel (Computer Science, 400 Level)*