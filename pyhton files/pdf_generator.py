from fpdf import FPDF
import matplotlib.pyplot as plt
import os
import platform
import subprocess


class MedicalReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'CITY GENERAL HOSPITAL - EMERGENCY SNAPSHOT', 0, 1, 'C')
        self.set_font('Arial', 'I', 10)
        self.cell(0, 5, 'Automated Medical Record System', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')


def generate_patient_pdf(patient_data, vitals_history, prescriptions=None):
    pdf = MedicalReport()
    pdf.add_page()

    # 1. Patient Information Section
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, f"Patient Name: {patient_data['full_name']}", 0, 1)
    pdf.set_font('Arial', '', 11)
    pdf.cell(0, 8, f"Patient ID: {patient_data['p_id']}", 0, 1)
    pdf.cell(0, 8, f"Blood Group: {patient_data['blood_group']}", 0, 1)

    if patient_data['allergies']:
        pdf.set_text_color(255, 0, 0)
        pdf.set_font('Arial', 'B', 11)
        pdf.cell(0, 10, f"CRITICAL ALLERGIES: {patient_data['allergies']}", 0, 1)
        pdf.set_text_color(0, 0, 0)

    pdf.ln(5)

    # 2. Generate Matplotlib Graph
    # Reverse history so the oldest data is on the left
    graph_data = vitals_history[:10]
    graph_data.reverse()

    times = [v['recorded_at'].strftime('%H:%M') for v in graph_data]
    heart_rates = [v['heart_rate'] for v in graph_data]

    plt.figure(figsize=(6, 3))
    plt.plot(times, heart_rates, marker='o', linestyle='-', color='red', linewidth=2)

    # Add the "Normal Range" shading
    plt.axhspan(60, 100, facecolor='green', alpha=0.1, label='Normal Range')

    plt.title('Heart Rate Trend (BPM)')
    plt.xlabel('Time')
    plt.ylabel('BPM')
    plt.grid(True, linestyle='--', alpha=0.6)

    graph_path = "temp_trend.png"
    plt.savefig(graph_path, bbox_inches='tight')
    plt.close()

    # 3. Add Graph to PDF
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, "Vitals Trend Analysis:", 0, 1)
    current_y = pdf.get_y()
    pdf.image(graph_path, x=10, y=current_y, w=180)
    pdf.set_y(current_y + 85)  # Adjusted spacing

    # 4. Vitals Table
    pdf.ln(5)
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(45, 10, 'Timestamp', 1)
    pdf.cell(35, 10, 'Heart Rate', 1)
    pdf.cell(35, 10, 'BP', 1)
    pdf.cell(35, 10, 'SpO2', 1)
    pdf.ln()

    pdf.set_font('Arial', '', 10)
    for entry in vitals_history[:5]:
        pdf.cell(45, 10, entry['recorded_at'].strftime('%Y-%m-%d %H:%M'), 1)
        pdf.cell(35, 10, f"{entry['heart_rate']} BPM", 1)
        pdf.cell(35, 10, entry['blood_pressure'], 1)
        pdf.cell(35, 10, f"{entry['spo2']}%", 1)
        pdf.ln()

    # 5. Prescriptions Table
    if prescriptions:
        pdf.ln(10)
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, "Active Prescriptions:", 0, 1)

        pdf.set_font('Arial', 'B', 10)
        pdf.cell(50, 10, 'Medication', 1)
        pdf.cell(30, 10, 'Dosage', 1)
        pdf.cell(40, 10, 'Frequency', 1)
        pdf.cell(40, 10, 'Doctor', 1)
        pdf.ln()

        pdf.set_font('Arial', '', 10)
        for p in prescriptions:
            pdf.cell(50, 10, p['medication_name'], 1)
            pdf.cell(30, 10, p['dosage'], 1)
            pdf.cell(40, 10, p['frequency'], 1)
            pdf.cell(40, 10, p['doctor_name'], 1)
            pdf.ln()

    # Save and Open
    file_name = f"Report_{patient_data['p_id']}.pdf"
    pdf.output(file_name)
    print(f"✅ Medical Report generated: {file_name}")

    try:
        if platform.system() == "Windows":
            os.startfile(file_name)
        elif platform.system() == "Darwin":
            subprocess.call(["open", file_name])
        else:
            subprocess.call(["xdg-open", file_name])
    except Exception as e:
        print(f"Could not open PDF automatically: {e}")

    if os.path.exists(graph_path):
        os.remove(graph_path)
