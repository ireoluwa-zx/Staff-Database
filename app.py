import streamlit as st
import pandas as pd
import datetime
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Staff Directory Pro", layout="wide")
st.title("Enterprise Staff Database")
st.markdown("Prototype interface for capturing and managing employee records.")

# Establish connection to Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Fetch existing data from the sheet
try:
    # We read the first 17 columns. ttl=0 ensures it doesn't cache stale data.
    existing_data = conn.read(worksheet="Sheet1", usecols=list(range(17)), ttl=0)
    existing_data = existing_data.dropna(how="all") # Remove empty rows
except Exception as e:
    st.error("Error connecting to Google Sheets. Please check your Secrets configuration.")
    st.stop()

# --- DATA COLLECTION FORM ---
with st.form("staff_data_form", clear_on_submit=True):
    st.subheader("1. Personal Information")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        name = st.text_input("Full Name")
        dob = st.date_input("Date of Birth", min_value=datetime.date(1900, 1, 1), max_value=datetime.date.today())
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
        hire_date = st.date_input("Date of Hire", min_value=datetime.date(1900, 1, 1), max_value=datetime.date(2100, 12, 31))
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
            # Create a new record
            new_record = pd.DataFrame([{
                "Name": name, "Staff No": staff_no, "RCC No": rcc_no, "Phone No": phone, 
                "Email": email, "Age": age, "Date of Birth": dob.strftime("%Y-%m-%d"), 
                "Gender": gender, "Marital Status": marital_status, "Home Address": address,
                "Office/Department": office, "Position/Duty": position, 
                "Employment Type": emp_type, "Hire Date": hire_date.strftime("%Y-%m-%d"), 
                "Salary": salary, "Next of Kin": nok_name, "Next of Kin Contact": nok_contact
            }])
            
            # Append to existing data and update the Google Sheet
            updated_df = pd.concat([existing_data, new_record], ignore_index=True)
            conn.update(worksheet="Sheet1", data=updated_df)
            
            # Clear the cache so the viewer below immediately shows the new data
            st.cache_data.clear()
            st.success(f"Record for {name} saved directly to Google Sheets!")

# --- DATABASE VIEWER ---
st.divider()
st.subheader("Live Database Viewer")

# Fetch fresh data for the viewer
current_db = conn.read(worksheet="Sheet1", usecols=list(range(17)), ttl=0).dropna(how="all")

if not current_db.empty:
    st.dataframe(current_db, use_container_width=True)
else:
    st.info("The staff database is currently empty. Add a record above.")
