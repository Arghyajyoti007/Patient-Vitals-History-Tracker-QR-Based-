import mysql.connector

class HospitalDB:
    def __init__(self):
        try:
            self.db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Arghya@123",
                database="hospital_db"
            )
            self.cursor = self.db.cursor(dictionary=True)
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    # --- CREATE OPERATIONS ---

    def register_patient(self, p_id, name, dob, blood_grp, allergies, contact):
        """Inserts a new patient record into the database."""
        query = """INSERT INTO patient_master (p_id, full_name, dob, blood_group, allergies, emergency_contact) 
                   VALUES (%s, %s, %s, %s, %s, %s)"""
        values = (p_id, name, dob, blood_grp, allergies, contact)
        self.cursor.execute(query, values)
        self.db.commit()
        print(f"Successfully registered: {name} with ID: {p_id}")

    def add_vitals(self, p_id, hr, bp, spo2, temp):
        """Logs a new set of vitals for a specific patient ID."""
        query = """INSERT INTO vitals_log (p_id, heart_rate, blood_pressure, spo2, temperature) 
                   VALUES (%s, %s, %s, %s, %s)"""
        values = (p_id, hr, bp, spo2, temp)
        self.cursor.execute(query, values)
        self.db.commit()
        print(f"Vitals logged for ID: {p_id}")

    def add_prescription(self, p_id, med_name, dosage, frequency, doc_name, date):
        """Adds a medication record to the prescriptions table."""
        query = """INSERT INTO prescriptions (p_id, medication_name, dosage, frequency, doctor_name, prescribed_date) 
                   VALUES (%s, %s, %s, %s, %s, %s)"""
        values = (p_id, med_name, dosage, frequency, doc_name, date)
        self.cursor.execute(query, values)
        self.db.commit()
        print(f"✅ Prescription for {med_name} added to ID: {p_id}")

    
    # --- READ / LOOKUP OPERATIONS ---

    def get_patient_record(self, p_id):
        """Retrieves patient profile using the Patient ID (p_id)."""
        query = "SELECT * FROM patient_master WHERE p_id = %s"
        self.cursor.execute(query, (p_id,))
        return self.cursor.fetchone()

    def get_patient_by_phone(self, phone):
        """Retrieves patient profile using the unique phone number."""
        query = "SELECT * FROM patient_master WHERE emergency_contact = %s"
        self.cursor.execute(query, (phone,))
        return self.cursor.fetchone()

    def get_vitals_history(self, p_id):
        """Retrieves all logged vitals for a patient, newest first."""
        query = "SELECT * FROM vitals_log WHERE p_id = %s ORDER BY recorded_at DESC"
        self.cursor.execute(query, (p_id,))
        return self.cursor.fetchall()
        

    # --- UTILITY OPERATIONS ---

    def generate_new_pid(self):
        """
        Calculates the next ID based on the count of rows.
        Example: If 5 patients exist, returns 'PATIENT_006'.
        """
        self.cursor.execute("SELECT COUNT(*) as total FROM patient_master")
        result = self.cursor.fetchone()
        next_num = result['total'] + 1
        return f"PATIENT_{next_num:03d}"

    def close_connection(self):
        """Properly closes the database connection."""
        self.cursor.close()

        self.db.close()
