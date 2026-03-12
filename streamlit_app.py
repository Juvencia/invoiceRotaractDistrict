
import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib import colors
from io import BytesIO

st.set_page_config(page_title="Rotaract District Invoice Generator", layout="centered")

st.title("Rotaract District Dues Invoice Generator")

# initialize invoice counter
if "invoice_counter" not in st.session_state:
    st.session_state.invoice_counter = 1

with st.form("invoice_form"):
    bill_to = st.text_input("Bill To")
    club_name = st.text_input("Club Name")
    invoice_date = st.date_input("Invoice Date")
    payment_due = st.date_input("Payment Due")
    members = st.number_input("Jumlah Member", min_value=1, step=1)
    rate = st.number_input("Dues per Member (Rp)", value=150000)

    submitted = st.form_submit_button("Generate Invoice")

if submitted:
    invoice_no = f"DD#{st.session_state.invoice_counter:02d}-2026"
    total = members * rate

    st.session_state.invoice_counter += 1

    st.success(f"Invoice Generated: {invoice_no}")

    st.subheader("Invoice Preview")

    st.write(f"**Bill To:** {bill_to}")
    st.write(f"**Club:** {club_name}")
    st.write(f"**Invoice Date:** {invoice_date}")
    st.write(f"**Payment Due:** {payment_due}")

    st.table({
        "Description":["Annual Rotaract Dues"],
        "Qty":[members],
        "Rate":[f"Rp {rate:,.0f}"],
        "Amount":[f"Rp {total:,.0f}"]
    })

    st.write(f"### Total Due: Rp {total:,.0f}")

    if st.button("Generate PDF"):

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=(21*cm, 29.7*cm))

        styles = getSampleStyleSheet()

        elements = []

        elements.append(Paragraph("Rotaract Club - District Dues Invoice", styles["Title"]))
        elements.append(Spacer(1,12))

        elements.append(Paragraph(f"Invoice Number: {invoice_no}", styles["Normal"]))
        elements.append(Paragraph(f"Bill To: {bill_to}", styles["Normal"]))
        elements.append(Paragraph(f"Club: {club_name}", styles["Normal"]))
        elements.append(Paragraph(f"Invoice Date: {invoice_date}", styles["Normal"]))
        elements.append(Paragraph(f"Payment Due: {payment_due}", styles["Normal"]))

        elements.append(Spacer(1,20))

        data = [
            ["Description","Qty","Rate","Amount"],
            ["Annual Rotaract Dues", members, f"Rp {rate:,.0f}", f"Rp {total:,.0f}"]
        ]

        table = Table(data)

        table.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,0),colors.pink),
            ("GRID",(0,0),(-1,-1),1,colors.grey)
        ]))

        elements.append(table)

        elements.append(Spacer(1,20))

        elements.append(Paragraph(f"Total Due: Rp {total:,.0f}", styles["Heading2"]))
        elements.append(Spacer(1,20))

        elements.append(Paragraph("Payment Information:", styles["Heading3"]))
        elements.append(Paragraph("Bank: Jago", styles["Normal"]))
        elements.append(Paragraph("Account Holder: Juvenus", styles["Normal"]))
        elements.append(Paragraph("Account Number: 101682490106", styles["Normal"]))

        doc.build(elements)

        pdf = buffer.getvalue()
        buffer.close()

        st.download_button(
            label="Download PDF",
            data=pdf,
            file_name=f"{invoice_no}.pdf",
            mime="application/pdf"
        )
