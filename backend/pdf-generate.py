# generate_test_pdfs.py
"""
Generate synthetic invoice PDFs for testing the PDF Data Extractor
Creates both digital and scanned-style PDFs with various table formats
"""

import os
from datetime import datetime, timedelta
import random
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.pdfgen import canvas

def create_invoice_1():
    """Create a simple digital invoice with clear tables"""
    filename = "test-pdfs/invoice_001_digital.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Company Header
    header_style = ParagraphStyle(
        'CustomHeader',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=20,
        alignment=1  # Center
    )
    
    story.append(Paragraph("ACME CORPORATION", header_style))
    story.append(Paragraph("123 Business Ave, New York, NY 10001<br/>Tel: (555) 123-4567", styles['Normal']))
    story.append(Spacer(1, 0.5*inch))
    
    # Invoice Title
    story.append(Paragraph("INVOICE", styles['Title']))
    story.append(Spacer(1, 0.2*inch))
    
    # Invoice Details
    invoice_data = [
        ['Invoice Number:', 'INV-2024-001'],
        ['Date:', '2024-10-15'],
        ['Due Date:', '2024-11-15'],
        ['Customer ID:', 'CUST-4532']
    ]
    
    details_table = Table(invoice_data, colWidths=[2*inch, 3*inch])
    details_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(details_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Bill To / Ship To
    billing_data = [
        ['BILL TO:', 'SHIP TO:'],
        ['Tech Solutions Inc.\n456 Innovation Drive\nSan Francisco, CA 94105\nUSA', 
         'Tech Solutions Inc.\n789 Warehouse Blvd\nOakland, CA 94607\nUSA']
    ]
    
    billing_table = Table(billing_data, colWidths=[3.5*inch, 3.5*inch])
    billing_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(billing_table)
    story.append(Spacer(1, 0.5*inch))
    
    # Main Invoice Items Table
    items_data = [
        ['Item Code', 'Description', 'Quantity', 'Unit Price', 'Total'],
        ['LAPTOP-001', 'Dell Latitude 5520 Laptop', '5', '$1,200.00', '$6,000.00'],
        ['MOUSE-002', 'Logitech MX Master 3 Mouse', '10', '$99.99', '$999.90'],
        ['KEYB-003', 'Mechanical Keyboard RGB', '10', '$149.99', '$1,499.90'],
        ['MONITOR-004', '27" 4K Monitor', '5', '$599.00', '$2,995.00'],
        ['DOCK-005', 'USB-C Docking Station', '5', '$199.00', '$995.00'],
        ['CABLE-006', 'HDMI Cable 6ft (Pack of 10)', '2', '$49.99', '$99.98'],
    ]
    
    items_table = Table(items_data, colWidths=[1.2*inch, 2.5*inch, 0.8*inch, 1*inch, 1*inch])
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(items_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Summary Table
    summary_data = [
        ['', '', '', 'Subtotal:', '$12,589.78'],
        ['', '', '', 'Tax (8.5%):', '$1,070.13'],
        ['', '', '', 'Shipping:', '$50.00'],
        ['', '', '', 'TOTAL:', '$13,709.91'],
    ]
    
    summary_table = Table(summary_data, colWidths=[1.2*inch, 2.5*inch, 0.8*inch, 1*inch, 1*inch])
    summary_table.setStyle(TableStyle([
        ('ALIGN', (3, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (3, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (3, -1), (-1, -1), 12),
        ('BACKGROUND', (3, -1), (-1, -1), colors.yellow),
        ('GRID', (3, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(summary_table)
    
    doc.build(story)
    print(f"Created: {filename}")

def create_invoice_2():
    """Create a service invoice with hourly billing"""
    filename = "test-pdfs/invoice_002_services.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Header
    story.append(Paragraph("CONSULTING SERVICES INVOICE", styles['Title']))
    story.append(Spacer(1, 0.3*inch))
    
    # Invoice Info
    info_data = [
        ['Invoice #:', 'SVC-2024-0892'],
        ['Project:', 'Website Redesign Phase 2'],
        ['Period:', 'September 1-30, 2024'],
        ['Client:', 'StartUp Innovations Ltd.'],
    ]
    
    info_table = Table(info_data, colWidths=[1.5*inch, 4*inch])
    info_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 0.5*inch))
    
    # Services Table
    services_data = [
        ['Date', 'Service Description', 'Hours', 'Rate/Hour', 'Amount'],
        ['2024-09-05', 'Frontend Development - React Components', '8', '$150', '$1,200.00'],
        ['2024-09-08', 'Backend API Development', '6', '$150', '$900.00'],
        ['2024-09-12', 'Database Schema Design', '4', '$175', '$700.00'],
        ['2024-09-15', 'UI/UX Design Consultation', '3', '$125', '$375.00'],
        ['2024-09-18', 'Testing and QA', '5', '$100', '$500.00'],
        ['2024-09-22', 'Deployment and Configuration', '4', '$150', '$600.00'],
        ['2024-09-25', 'Documentation', '3', '$100', '$300.00'],
        ['2024-09-28', 'Client Training Session', '2', '$125', '$250.00'],
    ]
    
    services_table = Table(services_data, colWidths=[1.2*inch, 2.8*inch, 0.8*inch, 1*inch, 1.2*inch])
    services_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10b981')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    story.append(services_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Totals
    totals_data = [
        ['Total Hours:', '35', '', 'Subtotal:', '$4,825.00'],
        ['', '', '', 'Discount (10%):', '-$482.50'],
        ['', '', '', 'Net Total:', '$4,342.50'],
    ]
    
    totals_table = Table(totals_data, colWidths=[1.2*inch, 0.8*inch, 2*inch, 1*inch, 1.2*inch])
    totals_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (1, -1), 'RIGHT'),
        ('ALIGN', (3, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('BACKGROUND', (3, -1), (-1, -1), colors.HexColor('#10b981')),
        ('TEXTCOLOR', (3, -1), (-1, -1), colors.white),
        ('GRID', (3, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(totals_table)
    
    doc.build(story)
    print(f"Created: {filename}")

def create_invoice_3():
    """Create a multi-page invoice with multiple tables"""
    filename = "test-pdfs/invoice_003_multipage.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # First Page - Header and Customer Info
    story.append(Paragraph("GLOBAL SUPPLIES CORPORATION", styles['Title']))
    story.append(Paragraph("Wholesale Distribution Invoice", styles['Heading2']))
    story.append(Spacer(1, 0.3*inch))
    
    # Customer and Invoice Details in two columns
    details_data = [
        ['INVOICE DETAILS', 'CUSTOMER INFORMATION'],
        ['Invoice No: WHL-2024-45678\nDate: Oct 10, 2024\nTerms: Net 30\nPO Number: PO-89234', 
         'Retail Mart Inc.\n1234 Commerce Street\nLos Angeles, CA 90001\nTax ID: 98-7654321']
    ]
    
    details_table = Table(details_data, colWidths=[3.5*inch, 3.5*inch])
    details_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.navy),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(details_table)
    story.append(Spacer(1, 0.5*inch))
    
    # Large Items Table (will span multiple pages)
    items_data = [
        ['SKU', 'Product Description', 'Unit', 'Qty', 'Unit Price', 'Total']
    ]
    
    # Generate 50 items to ensure multi-page
    products = [
        ('Office Chair Ergonomic', 'EA', 25, 89.99),
        ('Desk Lamp LED', 'EA', 50, 24.99),
        ('Paper A4 (Box)', 'BOX', 100, 12.50),
        ('Ballpoint Pens (Pack)', 'PCK', 200, 3.99),
        ('Stapler Heavy Duty', 'EA', 30, 15.99),
        ('File Folders (Box)', 'BOX', 50, 8.99),
        ('Whiteboard 4x6', 'EA', 10, 149.99),
        ('Printer Ink Black', 'EA', 60, 29.99),
        ('Printer Ink Color', 'EA', 40, 34.99),
        ('USB Flash Drive 32GB', 'EA', 100, 9.99),
        ('Notebook Spiral', 'EA', 300, 2.49),
        ('Calculator Scientific', 'EA', 25, 19.99),
        ('Paper Clips (Box)', 'BOX', 100, 1.99),
        ('Sticky Notes', 'PCK', 150, 4.49),
        ('Scissors', 'EA', 40, 6.99),
        ('Tape Dispenser', 'EA', 35, 7.99),
        ('Correction Fluid', 'EA', 80, 2.99),
        ('Highlighter Set', 'SET', 60, 5.99),
        ('Rubber Bands (Box)', 'BOX', 50, 3.49),
        ('Envelopes #10 (Box)', 'BOX', 30, 11.99),
    ]
    
    total_amount = 0
    for i, (product, unit, qty, price) in enumerate(products):
        sku = f'SKU-{1000 + i}'
        total = qty * price
        total_amount += total
        items_data.append([
            sku,
            product,
            unit,
            str(qty),
            f'${price:.2f}',
            f'${total:.2f}'
        ])
    
    items_table = Table(items_data, colWidths=[1*inch, 2.5*inch, 0.7*inch, 0.6*inch, 1*inch, 1.2*inch])
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4b5563')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f3f4f6')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    story.append(items_table)
    story.append(PageBreak())
    
    # Summary Page
    story.append(Paragraph("INVOICE SUMMARY", styles['Heading2']))
    story.append(Spacer(1, 0.3*inch))
    
    tax_rate = 0.0875
    tax_amount = total_amount * tax_rate
    shipping = 125.00
    grand_total = total_amount + tax_amount + shipping
    
    summary_data = [
        ['Description', 'Amount'],
        ['Merchandise Subtotal', f'${total_amount:,.2f}'],
        [f'Sales Tax ({tax_rate*100}%)', f'${tax_amount:,.2f}'],
        ['Shipping & Handling', f'${shipping:,.2f}'],
        ['GRAND TOTAL', f'${grand_total:,.2f}'],
    ]
    
    summary_table = Table(summary_data, colWidths=[4*inch, 2*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4b5563')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, -1), (-1, -1), 12),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#fbbf24')),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(summary_table)
    
    doc.build(story)
    print(f"Created: {filename}")

def create_invoice_4():
    """Create a restaurant/food service invoice"""
    filename = "test-pdfs/invoice_004_restaurant.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Header
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width/2, height - 50, "GOURMET SUPPLIES DISTRIBUTION")
    
    c.setFont("Helvetica", 12)
    c.drawCentredString(width/2, height - 70, "Food Service & Restaurant Supplies")
    
    # Invoice details box
    c.rect(50, height - 150, 200, 60)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(55, height - 100, "INVOICE #: FOOD-2024-3421")
    c.drawString(55, height - 115, "DATE: October 18, 2024")
    c.drawString(55, height - 130, "DUE: November 2, 2024")
    
    # Customer box
    c.rect(350, height - 150, 200, 60)
    c.drawString(355, height - 100, "BILL TO:")
    c.setFont("Helvetica", 9)
    c.drawString(355, height - 115, "The Riverside Bistro")
    c.drawString(355, height - 130, "789 Waterfront Ave, Miami, FL")
    
    # Table Header
    y_position = height - 200
    c.setFont("Helvetica-Bold", 10)
    c.rect(50, y_position - 20, 500, 20)
    c.drawString(55, y_position - 15, "Item")
    c.drawString(200, y_position - 15, "Description")
    c.drawString(350, y_position - 15, "Qty")
    c.drawString(400, y_position - 15, "Unit")
    c.drawString(450, y_position - 15, "Price")
    c.drawString(500, y_position - 15, "Total")
    
    # Table Items
    c.setFont("Helvetica", 9)
    items = [
        ("BEEF-001", "Prime Beef Ribeye (lb)", "50", "LB", "12.99", "649.50"),
        ("CHKN-002", "Organic Chicken Breast", "80", "LB", "6.49", "519.20"),
        ("FISH-003", "Fresh Atlantic Salmon", "40", "LB", "14.99", "599.60"),
        ("VEG-004", "Mixed Vegetables (Case)", "10", "CS", "24.99", "249.90"),
        ("RICE-005", "Jasmine Rice (50lb bag)", "5", "BAG", "42.00", "210.00"),
        ("OIL-006", "Extra Virgin Olive Oil", "12", "GAL", "28.50", "342.00"),
        ("FLOUR-007", "All Purpose Flour", "20", "BAG", "15.99", "319.80"),
        ("DAIRY-008", "Heavy Cream", "24", "QT", "4.99", "119.76"),
        ("EGGS-009", "Farm Fresh Eggs", "30", "DOZ", "3.49", "104.70"),
        ("SPICE-010", "Assorted Spices Set", "5", "SET", "89.99", "449.95"),
    ]
    
    y_position -= 30
    for item in items:
        c.drawString(55, y_position, item[0])
        c.drawString(120, y_position, item[1])
        c.drawString(355, y_position, item[2])
        c.drawString(400, y_position, item[3])
        c.drawString(450, y_position, f"${item[4]}")
        c.drawString(500, y_position, f"${item[5]}")
        y_position -= 15
    
    # Summary
    y_position -= 20
    c.line(350, y_position, 550, y_position)
    
    c.setFont("Helvetica-Bold", 10)
    c.drawString(400, y_position - 20, "Subtotal:")
    c.drawString(490, y_position - 20, "$3,564.41")
    
    c.drawString(400, y_position - 35, "Tax (7%):")
    c.drawString(490, y_position - 35, "$249.51")
    
    c.drawString(400, y_position - 50, "Delivery:")
    c.drawString(490, y_position - 50, "$35.00")
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(400, y_position - 70, "TOTAL:")
    c.drawString(485, y_position - 70, "$3,848.92")
    
    c.save()
    print(f"Created: {filename}")

def create_invoice_5():
    """Create a summary invoice consolidating multiple invoices"""
    filename = "test-pdfs/invoice_005_summary.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'ConsolidatedTitle',
        parent=styles['Title'],
        fontSize=18,
        textColor=colors.HexColor('#7c3aed'),
    )
    story.append(Paragraph("CONSOLIDATED INVOICE SUMMARY", title_style))
    story.append(Paragraph("Q3 2024 - All Branches", styles['Heading3']))
    story.append(Spacer(1, 0.3*inch))
    
    # Summary Info
    story.append(Paragraph("Period: July 1 - September 30, 2024", styles['Normal']))
    story.append(Paragraph("Prepared: October 18, 2024", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Individual Invoices Table
    invoice_data = [
        ['Invoice #', 'Date', 'Branch', 'Customer', 'Amount'],
        ['INV-2024-7001', '2024-07-05', 'New York', 'ABC Corp', '$5,234.50'],
        ['INV-2024-7089', '2024-07-12', 'Los Angeles', 'XYZ Ltd', '$3,456.78'],
        ['INV-2024-7156', '2024-07-20', 'Chicago', 'Tech Solutions', '$8,901.23'],
        ['INV-2024-8002', '2024-08-03', 'New York', 'Global Inc', '$2,345.67'],
        ['INV-2024-8045', '2024-08-15', 'Miami', 'Retail Plus', '$6,789.01'],
        ['INV-2024-8098', '2024-08-22', 'Los Angeles', 'Service Pro', '$4,567.89'],
        ['INV-2024-8134', '2024-08-28', 'Chicago', 'Manufacturing Co', '$7,890.12'],
        ['INV-2024-9003', '2024-09-05', 'Miami', 'Distribution LLC', '$3,456.78'],
        ['INV-2024-9067', '2024-09-14', 'New York', 'Consulting Group', '$5,678.90'],
        ['INV-2024-9122', '2024-09-25', 'Los Angeles', 'Logistics Inc', '$9,012.34'],
    ]
    
    invoice_table = Table(invoice_data, colWidths=[1.3*inch, 1*inch, 1*inch, 1.8*inch, 1.2*inch])
    invoice_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#7c3aed')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f3e8ff')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    story.append(invoice_table)
    story.append(Spacer(1, 0.4*inch))
    
    # Branch Summary Table
    story.append(Paragraph("SUMMARY BY BRANCH", styles['Heading3']))
    story.append(Spacer(1, 0.2*inch))
    
    branch_data = [
        ['Branch', 'Invoice Count', 'Total Amount', 'Average'],
        ['New York', '3', '$13,469.07', '$4,489.69'],
        ['Los Angeles', '3', '$17,036.01', '$5,678.67'],
        ['Chicago', '2', '$16,791.35', '$8,395.68'],
        ['Miami', '2', '$10,246.56', '$5,123.28'],
    ]
    
    branch_table = Table(branch_data, colWidths=[1.5*inch, 1.2*inch, 1.5*inch, 1.5*inch])
    branch_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#7c3aed')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#faf5ff')),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(branch_table)
    story.append(Spacer(1, 0.4*inch))
    
    # Grand Total
    total_style = ParagraphStyle(
        'TotalStyle',
        parent=styles['Normal'],
        fontSize=14,
        fontName='Helvetica-Bold',
        textColor=colors.HexColor('#7c3aed'),
        alignment=2,  # Right align
    )
    story.append(Paragraph("GRAND TOTAL: $57,542.99", total_style))
    story.append(Paragraph("Total Invoices: 10", styles['BodyText']))
    
    doc.build(story)
    print(f"Created: {filename}")

def main():
    """Generate all test PDFs"""
    # Create test-pdfs directory if it doesn't exist
    os.makedirs('test-pdfs', exist_ok=True)
    
    print("Generating test PDF invoices...")
    print("=" * 50)
    
    try:
        # Generate all invoice types
        create_invoice_1()  # Standard product invoice
        create_invoice_2()  # Service/hourly invoice
        create_invoice_3()  # Multi-page invoice
        create_invoice_4()  # Restaurant supply invoice
        create_invoice_5()  # Consolidated summary invoice
        
        print("=" * 50)
        print("✅ Successfully generated 5 test PDF invoices!")
        print("📁 Files are in the 'test-pdfs' directory")
        print("\nYou can now test your PDF extractor with these files.")
        
    except ImportError as e:
        print(f"Error: Missing required library: {e}")
        print("\nPlease install the required library:")
        print("pip install reportlab")
    except Exception as e:
        print(f"Error generating PDFs: {e}")

if __name__ == "__main__":
    main()