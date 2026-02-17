from database_manager import HospitalDB


def get_int_input(prompt):
    """Ensures the user enters a whole number."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("❌ Invalid input. Please enter a whole number.")


def get_float_input(prompt):
    """Ensures the user enters a decimal number (like temperature)."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("❌ Invalid input. Please enter a numeric value (e.g., 36.5).")


def take_details(db):
    print("\n--- NEW PATIENT REGISTRATION ---")
    contact = input("Emergency Contact Number: ").strip()

    existing = db.get_patient_by_phone(contact)
    if existing:
        print(f"⚠️ Duplicate Detected! Phone {contact} belongs to {existing['full_name']} (ID: {existing['p_id']})")
        return

    name = input("Full Name: ").strip()
    dob = input("DOB (YYYY-MM-DD): ").strip()
    bg = input("Blood Group: ").strip()
    allergies = input("Allergies: ").strip()

    new_pid = db.generate_new_pid()
    db.register_patient(new_pid, name, dob, bg, allergies, contact)

    # REFINEMENT: Pass the new_pid directly to log_vitals
    print(f"✅ Success! Assigned ID: {new_pid}")
    log_vitals(db, auto_id=new_pid)


def log_vitals(db, auto_id=None):
    print("\n--- LOG VITALS ---")

    # REFINEMENT: If we already have the ID (from registration), use it automatically
    if auto_id:
        p_id = auto_id
    else:
        p_id = input("Enter Patient ID: ").strip()

    patient = db.get_patient_record(p_id)

    if patient:
        print(f"Logging for: {patient['full_name']} (ID: {p_id})")
        hr = get_int_input("Heart Rate (BPM): ")
        bp = input("Blood Pressure (e.g., 120/80): ").strip()
        spo2 = get_int_input("SpO2 (%): ")
        temp = get_float_input("Temperature (Celsius): ")

        db.add_vitals(p_id, hr, bp, spo2, temp)
        print("✅ Vitals logged successfully.")
    else:
        print("❌ Patient not found.")
        choice = input("Would you like to register them now? (y/n): ").lower()
        if choice == 'y':
            take_details(db)


from datetime import date  # To get current date automatically


def add_prescription_ui(db):
    print("\n--- ADD PRESCRIPTION ---")
    p_id = input("Enter Patient ID: ").strip()
    patient = db.get_patient_record(p_id)

    if patient:
        print(f"Adding medication for: {patient['full_name']}")
        med = input("Medication Name: ").strip()
        dose = input("Dosage (e.g., 500mg): ").strip()
        freq = input("Frequency (e.g., Twice daily): ").strip()
        doc = input("Prescribing Doctor: ").strip()
        today = date.today().strftime('%Y-%m-%d')  # Auto-fills today's date

        db.add_prescription(p_id, med, dose, freq, doc, today)
    else:
        print("❌ Patient not found.")



def menu():
    try:
        db = HospitalDB()
    except Exception as e:
        print(f"❌ Database Connection Error: {e}")
        return

    while True:
        print("\n" + "=" * 30)
        print(" 🏥 HOSPITAL MANAGEMENT SYSTEM")
        print("=" * 30)
        print("1. Register New Patient")
        print("2. Log New Vitals")
        print("3. Add Prescription")
        print("4. Exit")

        choice = input("\nSelect Option: ").strip()

        if choice == '1':
            take_details(db)
        elif choice == '2':
            log_vitals(db)
        elif choice == '3':
            add_prescription_ui(db)
        elif choice == '4':
            print("Exiting System... Goodbye.")
            break
        else:
            print("❌ Invalid selection. Please choose 1, 2, or 3.")


if __name__ == "__main__":
    menu()