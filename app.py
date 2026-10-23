import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import io

st.set_page_config(page_title="Trainee Progress Report Generator", layout="centered")

st.title("Trainee Progress Report Generator")
st.write("Enter the information below to automatically generate and download the trainee progress report PDF.")

# --- PERSONAL INFORMATION ---
st.header("Trainee Information")
col1, col2 = st.columns(2)
with col1:
    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    campus = st.text_input("Campus")
with col2:
    dob = st.text_input("Date of Birth")
    phone = st.text_input("Phone Number")
    class_name = st.text_input("Class")

# --- LEARNING OUTCOMES ---
st.header("I. LEARNING OUTCOMES")
test_names = [
    "Mini test/Review test 1",
    "Mini test/Review test 2",
    "Mini test/Review test 3",
    "Mini test/Review test 4",
    "Final test",
    "Revision test"
]

scores_data = []
headers = ["Test Name", "Skill 1", "Skill 2", "Skill 3", "Skill 4", "Skill 5", "Skill 6", "Total Score"]

for idx, name in enumerate(test_names):
    st.subheader(name)
    cols = st.columns(7)
    s1 = cols[0].number_input(f"Skill 1", 0.0, 100.0, 0.0, key=f"s1_{idx}")
    s2 = cols[1].number_input(f"Skill 2", 0.0, 100.0, 0.0, key=f"s2_{idx}")
    s3 = cols[2].number_input(f"Skill 3", 0.0, 100.0, 0.0, key=f"s3_{idx}")
    s4 = cols[3].number_input(f"Skill 4", 0.0, 100.0, 0.0, key=f"s4_{idx}")
    s5 = cols[4].number_input(f"Skill 5", 0.0, 100.0, 0.0, key=f"s5_{idx}")
    s6 = cols[5].number_input(f"Skill 6", 0.0, 100.0, 0.0, key=f"s6_{idx}")
    
    total = (s1 + s2 + s3 + s4 + s5 + s6) / 6
    cols[6].markdown(f"**Avg: {total:.1f}**")
    scores_data.append([name, str(s1), str(s2), str(s3), str(s4), str(s5), str(s6), f"{total:.1f}"])

# --- INSTRUCTOR'S REMARKS ---
st.header("II. INSTRUCTOR'S REMARKS")
total_sessions = st.number_input("Total Number of Sessions", min_value=1, value=30, step=1)

col_a, col_b = st.columns(2)
with col_a:
    absences = st.number_input("Number of Absences", min_value=0, max_value=total_sessions, value=0, step=1)
with col_b:
    incomplete_hw = st.number_input("Number of Incomplete Homeworks", min_value=0, max_value=total_sessions, value=0, step=1)

st.write("**Performance and Attitude Evaluation:**")
col_m1, col_m2 = st.columns(2)
with col_m1:
    midterm_status = st.selectbox("Midterm Status", ["Good", "Average", "Needs Improvement", "Excellent"])
with col_m2:
    midterm_comment = st.text_area("Midterm Comments", height=100)

col_f1, col_f2 = st.columns(2)
with col_f1:
    final_status = st.selectbox("Final Status", ["Good", "Average", "Needs Improvement", "Excellent"])
with col_f2:
    final_comment = st.text_area("Final Comments", height=100)

result = st.selectbox("Result", ["Passed", "Failed", "Pending"])

st.header("Instructor & Report Date")
lecturer_name = st.text_input("Lecturer Name")
report_date = st.date_input("Date")

# --- PDF GENERATION FUNCTION ---
def generate_pdf():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=16,
        alignment=1, # Center
        spaceAfter=12
    )
    
    story.append(Paragraph("TRAINEE PROGRESS REPORT", title_style))
    story.append(Spacer(1, 10))
    
    # Personal info table
    info_data = [
        [f"Full Name: {full_name}", f"Date of Birth: {dob}"],
        [f"Email: {email}", f"Phone Number: {phone}"],
        [f"Campus: {campus}", f"Class: {class_name}"]
    ]
    t_info = Table(info_data, colWidths=[250, 250])
    t_info.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_info)
    story.append(Spacer(1, 15))
    
    # Section I: Learning Outcomes
    story.append(Paragraph("<b>I. LEARNING OUTCOMES:</b>", styles['Heading2']))
    story.append(Spacer(1, 5))
    
    table_content = [headers] + scores_data
    t_outcomes = Table(table_content, colWidths=[110, 50, 50, 50, 50, 50, 50, 60])
    t_outcomes.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_outcomes)
    story.append(Spacer(1, 15))
    
    # Section II: Remarks
    story.append(Paragraph("<b>II. INSTRUCTOR'S REMARKS:</b>", styles['Heading2']))
    story.append(Spacer(1, 5))
    
    # Cấu hình text tự xuống dòng cho comment
    comment_style = ParagraphStyle(
        'CommentStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        alignment=4, # Justify (Căn đều hai bên)
        leading=12 
    )
    
    remarks_data = [
        ["No.", "Evaluation Content", "Status", "Comments"],
        ["I", "Attendance", "", ""],
        ["1", "Number of Absences", f"({absences}/{total_sessions})", ""],
        ["2", "Number of Incomplete Homeworks", f"({incomplete_hw}/{total_sessions})", ""],
        ["II", "Performance and Attitude Evaluation", "", ""],
        ["1", "Midterm", midterm_status, Paragraph(midterm_comment, comment_style)],
        ["2", "Final", final_status, Paragraph(final_comment, comment_style)],
    ]
    
    t_remarks = Table(remarks_data, colWidths=[30, 180, 100, 190])
    t_remarks.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'TOP'), # Căn lề trên để khung chữ đẹp khi dài ra
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_remarks)
    story.append(Spacer(1, 10))
    
    story.append(Paragraph(f"<b>Result:</b> {result}", styles['Normal']))
    story.append(Spacer(1, 15))
    
    # Footer Date & Signature
    footer_style = ParagraphStyle(
        'FooterStyle',
        parent=styles['Normal'],
        alignment=1, # Center
        fontName='Helvetica',
        fontSize=10
    )
    
    date_str = f"Month {report_date.month} Day {report_date.day} Year {report_date.year}"
    footer_data = [
        [Paragraph("", styles['Normal']), Paragraph(date_str, footer_style)],
        [Paragraph("", styles['Normal']), Paragraph("<b>LECTURER</b>", footer_style)],
        [Paragraph("", styles['Normal']), Paragraph("(Signature & Full Name)", footer_style)],
        [Paragraph("", styles['Normal']), Paragraph("", footer_style)], 
        [Paragraph("", styles['Normal']), Paragraph("", footer_style)],
        [Paragraph("", styles['Normal']), Paragraph("", footer_style)], 
        [Paragraph("", styles['Normal']), Paragraph("", footer_style)], 
        [Paragraph("", styles['Normal']), Paragraph("", footer_style)], 
        [Paragraph("", styles['Normal']), Paragraph("", footer_style)], 
        [Paragraph("", styles['Normal']), Paragraph("", footer_style)], 
        [Paragraph("", styles['Normal']), Paragraph("", footer_style)],
        [Paragraph("", styles['Normal']), Paragraph("", footer_style)], 
        [Paragraph("", styles['Normal']), Paragraph("", footer_style)], 
        [Paragraph("", styles['Normal']), Paragraph(f"<b>{lecturer_name}</b>", footer_style)]
    ]
    
    t_footer = Table(footer_data, colWidths=[300, 200])
    t_footer.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_footer)
    
    doc.build(story)
    buffer.seek(0)
    return buffer

# --- DOWNLOAD BUTTON ---
st.markdown("---")
if st.button("Generate & Download PDF Report", type="primary"):
    if not full_name:
        st.warning("Please enter the trainee's Full Name before generating the report!")
    else:
        pdf_file = generate_pdf()
        st.success("Report generated successfully!")
        st.download_button(
            label="Download Completed PDF File",
            data=pdf_file,
            file_name=f"Trainee_Progress_Report_{full_name.replace(' ', '_')}.pdf",
            mime="application/pdf"
        )
