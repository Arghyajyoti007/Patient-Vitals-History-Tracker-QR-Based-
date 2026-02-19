# 🏥 QR-Link: Emergency Medical Snapshot System

**QR-Link** is a Python-based hospital management tool designed for rapid data retrieval during emergencies. By scanning a unique patient QR code, medical staff can instantly generate a comprehensive PDF report containing patient history, vital signs trends, and active prescriptions.

## 🚀 Key Features
* **Unique Patient Identification**: Auto-generates IDs in `PATIENT_001` format using Python string formatting.
* **Smart Data Entry**: Built-in validation to prevent duplicate registrations based on unique contact numbers.
* **Vitals Tracking**: Logs Heart Rate, BP, SpO2, and Temperature with timestamps.
* **Visual Analytics**: Generates a Matplotlib-powered heart rate trend graph with a "Normal Range" (60-100 BPM) safety overlay.
* **Automated PDF Reporting**: Creates a professional medical snapshot including patient details, trend graphs, and medication tables.

---

## 🛠️ Tech Stack
* **Language**: Python 3.x
* **Database**: MySQL
* **Libraries**: 
    * `mysql-connector-python` (Database management)
    * `fpdf` (PDF generation)
    * `matplotlib` (Data visualization)
    * `opencv-python` & `pyzbar` (QR scanning)

---

## 📂 Project Structure
```text
├── main.py                # Emergency Scanner & PDF Trigger
├── database_manager.py    # MySQL Logic (CRUD operations)
├── pdf_generator.py       # PDF Layout & Graph Plotting
├── add_patient_ui.py      # Data Entry Interface (Vitals/Prescriptions)
└── requirements.txt       # List of dependencies
