# 🎓 NOUN Biometric Exam Guard

**Exam Guard** is a security verification system designed for the **National Open University of Nigeria (NOUN)** to prevent exam malpractice and impersonation. 

It uses a **Biometric Simulation** to verify student identities in real-time before they enter the exam hall.

## 🚀 Key Features

### 🧬 1. Biometric Verification Simulation
* Simulates a fingerprint scanner interface.
* Instantly retrieves student details from a secure database based on their unique biometric ID.

### 🚨 2. Impersonation Detection
* Automatically flags unregistered or fake IDs.
* Displays a **"RED ALERT"** warning if a non-student tries to gain access.

### 📱 3. Mobile "Haptic" Scanner
* Optimized for mobile phones.
* Uses **Haptic Feedback (Vibration)** API to make the phone physically vibrate when the user presses the "Scan" button, mimicking a real hardware scanner.

### 📂 4. Digital Student Database
* Stores and retrieves student records including:
    * **Full Name & Photo**
    * **Matriculation Number**
    * **Department & Level**

---

## 🛠️ Tech Stack
* **Backend:** Python (Flask)
* **Frontend:** HTML5, CSS3 (Matrix/Hacker Theme), JavaScript
* **Database:** CSV (Lightweight Flat-File Database)
* **Hardware Integration:** JavaScript Vibration API

---

## 📸 How It Works
1.  **The Checkpoint:** The invigilator or student opens the app on a mobile device or laptop.
2.  **The Scan:** The user places their finger on the green scanner pad.
3.  **The Process:** The phone vibrates to confirm the scan, and the ID is sent to the Python backend.
4.  **The Result:**
    * **✅ ACCESS GRANTED:** Shows the student's face and matric number.
    * **❌ ACCESS DENIED:** Triggers an impersonator alert.

---

## 💻 Installation
1.  Clone the repository:
    ```bash
    git clone [https://github.com/Mabel55/noun-biometric-guard.git](https://github.com/Mabel55/noun-biometric-guard.git)
    ```
2.  Create a virtual environment:
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```
3.  Install Flask:
    ```bash
    pip install flask
    ```
4.  Run the application:
    ```bash
    python app.py
    ```

---
*Built by Arua Mabel Chinasa. Solving real-world problems with Code.*