create database hospital_db;

use hospital_db;

-- 1. Patient Master: Permanent medical profile
CREATE TABLE patient_master (
    id INT AUTO_INCREMENT UNIQUE, -- This handles the numbering (1, 2, 3...)
    p_id VARCHAR(50) PRIMARY KEY, -- This will store 'PATIENT_001'
    full_name VARCHAR(100) NOT NULL,
    dob DATE,
    blood_group VARCHAR(5),
    allergies TEXT,
    emergency_contact VARCHAR(15) NOT NULL UNIQUE, -- Your unique check
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Vitals Log: Time-series health data
CREATE TABLE vitals_log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    p_id VARCHAR(50),
    heart_rate INT,
    blood_pressure VARCHAR(10), -- e.g., "120/80"
    spo2 INT,                   -- Oxygen saturation
    temperature DECIMAL(4,1),
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (p_id) REFERENCES patient_master(p_id) ON DELETE CASCADE
);

-- 3. Prescriptions: Active medication and dosage
CREATE TABLE prescriptions (
    presc_id INT AUTO_INCREMENT PRIMARY KEY,
    p_id VARCHAR(50),
    medication_name VARCHAR(100),
    dosage VARCHAR(50),
    frequency VARCHAR(50),
    doctor_name VARCHAR(100),
    prescribed_date DATE,
    FOREIGN KEY (p_id) REFERENCES patient_master(p_id)
);



select * from patient_master;
select * from vitals_log;
select * from prescriptions;
