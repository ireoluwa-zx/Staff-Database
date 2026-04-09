import streamlit as st
import pandas as pd
import os

# File path for the CSV database
DATA_FILE = 'staff_database.csv'

# Initialize the CSV file if it doesn't exist to prevent errors
if not os.path.exists(DATA_FILE):
    df_init = pd.DataFrame(columns=[
        "Name", "Staff No", "RCC No", "Phone No", "Email", "Age", "Date of Birth",
        "Gender", "Marital Status", "Home Address", 
        "Office/Department", "Position/Duty", "Employment Type", "Hire Date", "Salary", 
        "Next of Kin", "Next of Kin Contact"
    ])
    df_init.to_csv(DATA_FILE, index=False)

# Make the page wider for better data viewing
st.set_page_config(page_title="Staff Directory Pro", layout="wide")
st.title("Enterprise Staff Database")
st.markdown("Prototype interface for capturing and managing employee records.")

# --- DATA COLLECTION FORM ---
with st.form("staff_data_form", clear_on_submit=True):
    st.subheader("1. Personal Information")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        name = st.text_input("Full Name")
        dob = st.date_input("Date of Birth")
        age = st.number_input("Age", min_value=16, max_value=100, step=1)
    with col2:
        gender = st.selectbox("Gender", ["Select...", "Male", "Female"])
        marital_status = st.selectbox("Marital Status", ["Select...", "Single", "Married", "Divorced", "Widowed"])
    with col3:
        phone = st.text_input("Phone Number")
        email = st.text_input("Email Address")
        
    address = st.text_input("Home Address")

    st.markdown("---")
    st.subheader("2. Professional Details")
    col4, col5, col6 = st.columns(3)
    
    with col4:
        staff_no = st.text_input("Staff Number")
        rcc_no = st.text_input("RCC Number")
        hire_date = st.date_input("Date of Hire")
    with col5:
        office = st.text_input("Office / Department")
        position = st.text_input("Position / Duty")
    with col6:
        emp_type = st.selectbox("Employment Type", ["Select...", "Full-Time", "Part-Time", "Contract", "SIWES / Intern"])
        salary = st.number_input("Annual Salary", min_value=0.0, step=1000.0)

    st.markdown("---")
    st.subheader("3. Emergency Contact")
    col7, col8 = st.columns(2)
    with col7:
        nok_name = st.text_input("Next of Kin (Full Name)")
    with col8:
        nok_contact = st.text_input("Next of Kin Contact (Phone No)")

    submitted = st.form_submit_button("Save Employee Record")

    if submitted:
        if name.strip() == "" or staff_no.strip() == "":
            st.error("Name and Staff Number are mandatory fields!")
        else:
            # Create a new record from the inputs
            new_record = pd.DataFrame([{
                "Name": name, "Staff No": staff_no, "RCC No": rcc_no, "Phone No": phone, 
                "Email": email, "Age": age, "Date of Birth": dob, "Gender": gender, 
                "Marital Status": marital_status, "Home Address": address,
                "Office/Department": office, "Position/Duty": position, 
                "Employment Type": emp_type, "Hire Date": hire_date, "Salary": salary,
                "Next of Kin": nok_name, "Next of Kin Contact": nok_contact
            }])
            
            # Read current CSV, append new data, and save back to CSV
            df = pd.read_csv(DATA_FILE)
            df = pd.concat([df, new_record], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            
            st.success(f"Record for {name} ({staff_no}) saved successfully!")

# --- DATABASE VIEWER ---
st.divider()
st.subheader("Staff Database Viewer")

if os.path.exists(DATA_FILE):
    current_db = pd.read_csv(DATA_FILE)
    if not current_db.empty:
        # Display as an interactive dataframe
        st.dataframe(current_db, use_container_width=True)
        
        # Download button for backups
        csv_export = current_db.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Database as CSV",
            data=csv_export,
            file_name='company_staff_database.csv',
            mime='text/csv',
        )
    else:
        st.info("The staff database is currently empty. Add a record above.")
