import os
from flask import Flask, render_template, request, send_from_directory
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

app = Flask(__name__)

# Folder to store generated invoices
INVOICE_FOLDER = 'invoices'
os.makedirs(INVOICE_FOLDER, exist_ok=True)

def generate_pdf_invoice(row, output_filename):
    doc = SimpleDocTemplate(output_filename, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#1E293B')
    )
    story.append(Paragraph("INVOICE", title_style))
    story.append(Spacer(1, 12))

    details_text = f"""
    <b>Invoice No:</b> {row.get('InvoiceNo', 'INV-000')}<br/>
    <b>Date:</b> {row.get('Date', 'N/A')}<br/>
    <b>Customer Name:</b> {row.get('CustomerName', 'N/A')}<br/>
    <b>Email:</b> {row.get('CustomerEmail', 'N/A')}
    """
    story.append(Paragraph(details_text, styles['Normal']))
    story.append(Spacer(1, 20))

    item = str(row.get('ItemDescription', 'Product/Service'))
    qty = str(row.get('Quantity', 1))
    price = float(row.get('UnitPrice', 0.0))
    total = float(row.get('TotalAmount', price))

    data = [
        ['Description', 'Quantity', 'Unit Price ($)', 'Total ($)'],
        [item, str(qty), f"{price:.2f}", f"{total:.2f}"]
    ]

    table = Table(data, colWidths=[250, 80, 100, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F172A')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F8FAFC')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
    ]))

    story.append(table)
    story.append(Spacer(1, 20))

    total_text = f"<b>Grand Total: ${total:.2f}</b>"
    story.append(Paragraph(total_text, styles['Heading2']))

    doc.build(story)

# New Route to serve PDF files directly to browser
@app.route('/invoices/<filename>')
def download_invoice(filename):
    return send_from_directory(INVOICE_FOLDER, filename)

@app.route('/', methods=['GET', 'POST'])
def index():
    generated_files = []
    if request.method == 'POST':
        file = request.files.get('file')
        if not file or not file.filename.endswith(('.xlsx', '.xls')):
            return "Please upload a valid Excel file (.xlsx or .xls)", 400

        df = pd.read_excel(file)

        for index, row in df.iterrows():
            inv_no = str(row.get('InvoiceNo', f'INV_{index+1}'))
            filename = f"{inv_no}.pdf"
            pdf_path = os.path.join(INVOICE_FOLDER, filename)
            generate_pdf_invoice(row, pdf_path)
            generated_files.append(filename)

        return render_template('index.html', success=True, files=generated_files)

    return render_template('index.html', success=False)

if __name__ == '__main__':
    app.run(debug=True)