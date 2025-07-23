
from fpdf import FPDF
import datetime

class ScanReportPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'ScanAI - Image/Video Analysis Report', ln=True, align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

    def add_scan_results(self, filename, scan_type, result_data):
        self.add_page()
        self.set_font('Arial', '', 12)
        self.cell(0, 10, f"File Scanned: {filename}", ln=True)
        self.cell(0, 10, f"Scan Type: {scan_type}", ln=True)
        self.cell(0, 10, f"Scan Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
        self.ln(10)
        for key, value in result_data.items():
            self.multi_cell(0, 10, f"{key}: {value}")
