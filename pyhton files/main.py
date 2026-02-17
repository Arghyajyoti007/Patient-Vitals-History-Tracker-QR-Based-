from database_manager import HospitalDB
from qr_scanner import scan_qr
from pdf_generator import generate_patient_pdf


def start_system():
    # 1. Connect to Database
    db = HospitalDB()

    # 2. Start Scanner
    print("System Active. Please scan Patient QR Code...")
    patient_id = scan_qr()

    # 3. Retrieve Data
    patient_info = db.get_patient_record(patient_id)
    vitals_history = db.get_vitals_history(patient_id)

    if patient_info:
        print(f"Match Found: {patient_info['full_name']}")

        # 4. Generate the PDF Report with Matplotlib Trends
        generate_patient_pdf(patient_info, vitals_history)
        print("Success: Emergency Snapshot Prepared.")
    else:
        print("Error: Patient ID not recognized in database.")


if __name__ == "__main__":
    start_system()
