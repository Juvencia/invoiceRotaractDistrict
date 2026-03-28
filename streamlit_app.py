import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib import colors
from io import BytesIO


logo = Image("assets/rotaract_district_logo.png", width=5*cm, height=2.5*cm)

st.set_page_config(page_title="Rotaract Invoice Generator")

st.title("Rotaract District Dues Invoice")

if "counter" not in st.session_state:
    st.session_state.counter = 1

with st.form("invoice_form"):

    invoice_number_input = st.text_input("Invoice Number (DD#01-2026)")

    bill_to = st.text_input("Bill To")
    club_name = st.text_input("Club Name")

    invoice_date = st.date_input("Invoice Date")
    payment_due = st.date_input("Payment Due")

    members = st.number_input("Jumlah Member", min_value=1)

    submit = st.form_submit_button("Generate Invoice")

if submit:

    rate = 20000
    total = members * rate

    if invoice_number_input != "":
        invoice_number = invoice_number_input
    else:
        invoice_number = f"DD#{st.session_state.counter:02d}-2026"
        st.session_state.counter += 1

    st.session_state.invoice = {
        "invoice_number": invoice_number,
        "bill_to": bill_to,
        "club_name": club_name,
        "invoice_date": invoice_date,
        "payment_due": payment_due,
        "members": members,
        "rate": rate,
        "total": total
    }

if "invoice" in st.session_state:

    data = st.session_state.invoice

    st.markdown("---")

    st.subheader("Invoice Preview")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Bill To**")
        st.write(data["bill_to"])
        st.write(data["club_name"])

    with col2:
        st.write(f"**Invoice #:** {data['invoice_number']}")
        st.write(f"Invoice Date: {data['invoice_date']}")
        st.write(f"Payment Due: {data['payment_due']}")

    st.markdown("### ")

    table = {
        "Description": ["Annual Rotaract Dues"],
        "Qty": [data["members"]],
        "Rate": [f"Rp {data['rate']:,}"],
        "Amount": [f"Rp {data['total']:,}"]
    }

    st.table(table)

    st.write("Subtotal:", f"Rp {data['total']:,}")
    st.write("Tax (0%): Rp 0")
    st.write("### Total Due:", f"Rp {data['total']:,}")

    st.markdown("### Payment Information")

    st.write("Bank: Jago")
    st.write("Account Holder: Juvenus")
    st.write("Account Number: 101682490106")

    st.markdown("Thank you for your commitment!")

    if st.button("Generate PDF"):

        buffer = BytesIO()

        doc = SimpleDocTemplate(buffer, pagesize=(21*cm,29.7*cm))

        styles = getSampleStyleSheet()

        elements = []
        
        elements.append
        logo,
        elements.append(Paragraph("Rotaract Club - Club Dues Invoice", styles["Title"]))

        elements.append(Spacer(1,20))

        elements.append(Paragraph(f"Invoice Number: {data['invoice_number']}", styles["Normal"]))
        elements.append(Paragraph(f"Bill To: {data['bill_to']}", styles["Normal"]))
        elements.append(Paragraph(f"Club: {data['club_name']}", styles["Normal"]))
        elements.append(Paragraph(f"Invoice Date: {data['invoice_date']}", styles["Normal"]))
        elements.append(Paragraph(f"Payment Due: {data['payment_due']}", styles["Normal"]))

        elements.append(Spacer(1,20))

        pdf_table = Table([
            ["Description","Qty","Rate","Amount"],
            ["Annual Rotaract Dues",
             data["members"],
             f"Rp {data['rate']:,}",
             f"Rp {data['total']:,}"]
        ])

        pdf_table.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,0),colors.lightpink),
            ("GRID",(0,0),(-1,-1),1,colors.grey)
        ]))

        elements.append(pdf_table)

        elements.append(Spacer(1,20))

        elements.append(Paragraph(f"Total Due: Rp {data['total']:,}", styles["Heading2"]))

        elements.append(Spacer(1,20))

        elements.append(Paragraph("Payment Information", styles["Heading3"]))
        elements.append(Paragraph("Bank: Jago", styles["Normal"]))
        elements.append(Paragraph("Account Holder: Juvenus", styles["Normal"]))
        elements.append(Paragraph("Account Number: 101682490106", styles["Normal"]))

        doc.build(elements)

        pdf = buffer.getvalue()

        st.download_button(
            "Download Invoice PDF",
            pdf,
            file_name=f"{data['invoice_number']}.pdf",
            mime="application/pdf"
        )
