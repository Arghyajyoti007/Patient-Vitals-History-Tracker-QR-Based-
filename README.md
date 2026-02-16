# 🏥 Patient Vitals & History Tracker (QR-Based)

A modular Python system for high-speed retrieval of patient medical records via QR codes.

## 🏗️ Modules
- `database_manager.py`: Handles MySQL connections and CRUD operations.
- `qr_scanner.py`: Computer Vision module for patient ID retrieval.
- `pdf_generator.py`: Generates emergency medical snapshots with Matplotlib trends.
- `main.py`: Orchestrates the workflow.

## 🛠️ Setup
1. **Database:** Run the SQL scripts in `/sql/schema.sql` to initialize MySQL.
2. **Dependencies:** ```bash
   pip install mysql-connector-python opencv-python pyzbar fpdf matplotlib
