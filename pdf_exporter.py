# pdf_exporter.py
# Generate professional PDF reports

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO
from datetime import datetime


def generate_pdf_report(df, channel_stats):
    """Generate a professional PDF report of YouTube analytics"""
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    # Container for elements
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2563EB'),
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#6B7280'),
        spaceAfter=20,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#1F2937'),
        spaceAfter=12,
        spaceBefore=20,
        fontName='Helvetica-Bold'
    )
    
    # Title
    title = Paragraph("YouTube Analytics Report", title_style)
    elements.append(title)
    
    subtitle = Paragraph(f"{channel_stats['channel_name']} • Generated {datetime.now().strftime('%B %d, %Y')}", subtitle_style)
    elements.append(subtitle)
    
    elements.append(Spacer(1, 0.2*inch))
    
    # Channel Summary
    elements.append(Paragraph("Channel Summary", heading_style))
    
    summary_data = [
        ['Metric', 'Value'],
        ['Total Subscribers', f"{channel_stats['total_subscribers']:,}"],
        ['Total Views', f"{channel_stats['total_views']:,}"],
        ['Total Videos', f"{channel_stats['total_videos']:,}"],
        ['Avg Views per Video', f"{channel_stats['total_views'] // channel_stats['total_videos']:,}"]
    ]
    
    summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563EB')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E5E7EB')),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
    ]))
    
    elements.append(summary_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Video Data
    elements.append(Paragraph("Complete Video Dataset", heading_style))
    
    # Prepare table data
    table_data = [['Title', 'Upload Date', 'Views', 'Likes', 'Comments', 'Engagement %', 'Duration']]
    
    for _, row in df.iterrows():
        table_data.append([
            row['title'][:40] + '...' if len(row['title']) > 40 else row['title'],
            row['upload_date'].strftime('%Y-%m-%d'),
            f"{row['view_count']:,}",
            f"{row['like_count']:,}",
            f"{row['comment_count']:,}",
            f"{row['engagement_rate']:.2f}",
            f"{int(row['duration_seconds'] // 60)}:{int(row['duration_seconds'] % 60):02d}"
        ])
    
    # Create table with adjusted column widths
    col_widths = [2.2*inch, 0.9*inch, 0.7*inch, 0.6*inch, 0.7*inch, 0.8*inch, 0.7*inch]
    video_table = Table(table_data, colWidths=col_widths, repeatRows=1)
    
    video_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563EB')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (2, 1), (6, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E5E7EB')),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F9FAFB')]),
    ]))
    
    elements.append(video_table)
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer
