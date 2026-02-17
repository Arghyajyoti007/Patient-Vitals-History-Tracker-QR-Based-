from fpdf import FPDF
import matplotlib.pyplot as plt
import os
import platform
import subprocess


class MedicalReport(FPDF):
    def header(self):
        # Hospital Branding
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'CITY GENERAL HOSPITAL - EMERGENCY SNAPSHOT', 0, 1, 'C')
        self.set_font('Arial', 'I', 10)
        self.cell(0, 5, 'Automated Medical Record System', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')


def generate_patient_pdf(patient_data, vitals_history):
    pdf = MedicalReport()
    pdf.add_page()

    # 1. Patient Information Section
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, f"Patient Name: {patient_data['full_name']}", 0, 1)
    pdf.set_font('Arial', '', 11)
    pdf.cell(0, 8, f"Patient ID: {patient_data['p_id']}", 0, 1)
    pdf.cell(0, 8, f"Blood Group: {patient_data['blood_group']}", 0, 1)

    # Highlight Allergies in Red-style (Bold)
    if patient_data['allergies']:
        pdf.set_text_color(255, 0, 0)
        pdf.set_font('Arial', 'B', 11)
        pdf.cell(0, 10, f"CRITICAL ALLERGIES: {patient_data['allergies']}", 0, 1)
        pdf.set_text_color(0, 0, 0)  # Reset color

    pdf.ln(10)

    # 2. Generate Matplotlib Graph
    # We extract the last 5-10 heart rate readings for the trend
    times = [v['recorded_at'].strftime('%H:%M') for v in vitals_history[-10:]]
    heart_rates = [v['heart_rate'] for v in vitals_history[-10:]]

    plt.figure(figsize=(6, 3))
    plt.plot(times, heart_rates, marker='o', color='red', linewidth=2)
    plt.title('Heart Rate Trend (BPM)')
    plt.grid(True, linestyle='--', alpha=0.6)

    # Save the graph as a temporary image
    graph_path = "temp_trend.png"
    plt.savefig(graph_path, bbox_inches='tight')
    plt.close()

    # 3. Add Graph to PDF
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, "Vitals Trend Analysis:", 0, 1)

    # Capture the current Y position before placing the image
    current_y = pdf.get_y()

    # Place image (w=180 is roughly the width of the page)
    pdf.image(graph_path, x=10, y=current_y, w=180)

    # CRITICAL FIX: Move the cursor manually below the image.
    # If the image width is 180, its height in this aspect ratio is about 90.
    # We set the new Y to current_y + 95 to leave a small gap.
    pdf.set_y(current_y + 95)

    # 4. Vitals Table (Now it will start below the graph)
    pdf.ln(5)  # Extra breathing room
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(45, 10, 'Timestamp', 1)
    pdf.cell(35, 10, 'Heart Rate', 1)
    pdf.cell(35, 10, 'BP', 1)
    pdf.cell(35, 10, 'SpO2', 1)
    pdf.ln()


    pdf.set_font('Arial', '', 10)
    for entry in vitals_history[:5]:  # Show last 5 records in table
        pdf.cell(40, 10, entry['recorded_at'].strftime('%Y-%m-%d %H:%M'), 1)
        pdf.cell(40, 10, f"{entry['heart_rate']} BPM", 1)
        pdf.cell(40, 10, entry['blood_pressure'], 1)
        pdf.cell(40, 10, f"{entry['spo2']}%", 1)
        pdf.ln()

    # Output the PDF
    file_name = f"Report_{patient_data['p_id']}.pdf"
    pdf.output(file_name)

    # ... (inside your generate_patient_pdf function, after pdf.output(file_name))

    print(f"✅ Medical Report generated: {file_name}")

    # Auto-open the PDF based on the Operating System
    try:
        if platform.system() == "Windows":
            os.startfile(file_name)
        elif platform.system() == "Darwin":  # macOS
            subprocess.call(["open", file_name])
        else:  # Linux
            subprocess.call(["xdg-open", file_name])
    except Exception as e:
        print(f"Could not open PDF automatically: {e}")

    # Clean up the temporary image
    if os.path.exists(graph_path):
        os.remove(graph_path)

    print(f"✅ Medical Report generated: {file_name}")