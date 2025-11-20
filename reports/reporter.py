# reports/reporter.py
import sqlite3
import csv
from fpdf import FPDF
from backend.database import DB_FILE

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Port Intent Detector PRO Report', ln=True, align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

def fetch_connections():
    """Fetch all connections from the database"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT pid, process_name, exe_path, local_addr, remote_addr, protocol, intent, suspicious, ts FROM connections ORDER BY ts ASC")
    results = cursor.fetchall()
    conn.close()
    return results

def generate_csv(file_path="connections_report.csv"):
    """Generate CSV report"""
    data = fetch_connections()
    with open(file_path, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["PID", "Process Name", "Executable", "Local Addr", "Remote Addr", "Protocol", "Intent", "Suspicious", "Timestamp"])
        writer.writerows(data)
    print(f"CSV report saved to {file_path}")

def generate_pdf(file_path="connections_report.pdf"):
    """Generate PDF report"""
    data = fetch_connections()
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_font("Arial", size=10)

    col_widths = [15, 30, 40, 25, 25, 15, 30, 15, 25]

    # Header
    headers = ["PID", "Process", "Exe", "Local", "Remote", "Proto", "Intent", "Susp", "Timestamp"]
    for i, h in enumerate(headers):
        pdf.cell(col_widths[i], 8, h, border=1)
    pdf.ln()

    # Rows
    for row in data:
        for i, item in enumerate(row):
            pdf.cell(col_widths[i], 6, str(item), border=1)
        pdf.ln()

    pdf.output(file_path)
    print(f"PDF report saved to {file_path}")
