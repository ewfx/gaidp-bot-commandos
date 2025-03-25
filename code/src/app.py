import streamlit as st
import requests
import json

# API Base URL
API_BASE_URL = "http://127.0.0.1:8000/check_compliance/"

st.set_page_config(page_title="Transaction Compliance Checker", layout="centered")

# Streamlit UI
st.title("🔍 Transaction Compliance Checker")

# Compliance Type Selection
section = st.radio("Select Compliance Type:", ["H1", "H2"])

st.markdown("Enter transaction details manually to check compliance.")

# User Input Form
with st.form("transaction_form"):
    col1, col2 = st.columns(2)
    
    if section == "H1":
        with col1:
            customer_id = st.text_input("📌 Customer ID", "CUST123")
            internal_id = st.text_input("🔢 Internal ID", "INT456")
            original_internal_id = st.text_input("🔢 Original Internal ID", "ORG789")
            obligor_name = st.text_input("🏢 Obligor Name", "ABC Corp")
            city = st.text_input("🌆 City", "New York")
            country = st.text_input("🌍 Country", "USA")
            zip_code = st.text_input("📍 Zip Code", "10001")
            industry_code = st.text_input("🏭 Industry Code", "531312")
            industry_code_type = st.selectbox("🔖 Industry Code Type", ["NAICS", "SIC", "GICS"], index=0)
            risk_rating = st.text_input("📊 Obligor Internal Risk Rating", "A")
            tin = st.text_input("🆔 TIN", "123-45-6789")
            stock_exchange = st.text_input("📈 Stock Exchange", "NYSE")
        
        with col2:
            ticker_symbol = st.text_input("📉 Ticker Symbol", "ABC")
            cusip = st.text_input("🔢 CUSIP", "123456789")
            internal_credit_facility_id = st.text_input("🏦 Internal Credit Facility ID", "CF001")
            original_internal_credit_facility_id = st.text_input("🏦 Original Internal Credit Facility ID", "CF002")
            origination_date = st.date_input("📅 Origination Date")
            maturity_date = st.date_input("📅 Maturity Date")
            credit_facility_type = st.selectbox("🏦 Credit Facility Type", list(range(20)), index=0)
            other_credit_facility_type = st.text_input("🏦 Other Credit Facility Type", "N/A")
            credit_facility_purpose = st.selectbox("🎯 Credit Facility Purpose", list(range(33)), index=0)
            other_credit_facility_purpose = st.text_input("🎯 Other Credit Facility Purpose", "N/A")
            committed_exposure = st.text_input("💰 Committed Exposure", "1000000")
            utilized_exposure = st.text_input("💰 Utilized Exposure", "500000")
    
    elif section == "H2":
        with col1:
            loan_number = st.text_input("📌 Loan Number", "LN123456")
            obligor_name = st.text_input("🏢 Obligor Name", "XYZ Bank")
            outstanding_balance = st.text_input("💰 Outstanding Balance", "20000000")
            line_reported = st.text_input("📑 Line Reported on FR Y-9C", "10")
            committed_exposure_global = st.text_input("💰 Committed Exposure Global", "15000000")
            cumulative_charge_offs = st.text_input("💰 Cumulative Charge-offs", "0")
            participation_flag = st.selectbox("🏳️ Participation Flag", list(range(1, 6)), index=0)
            lien_position = st.selectbox("🏦 Lien Position", list(range(1, 6)), index=0)
            property_type = st.selectbox("🏠 Property Type", list(range(1, 13)), index=0)
            origination_date = st.date_input("📅 Origination Date")
            location = st.text_input("📍 Location", "10001")
            noi_at_origination = st.text_input("💰 Net Operating Income at Origination", "5000000")
        
        with col2:
            value_at_origination = st.text_input("💰 Value at Origination", "25000000")
            value_basis = st.selectbox("📊 Value Basis", list(range(1, 4)), index=0)
            internal_rating = st.text_area("📊 Internal Rating", "Rating-1:0.5; Rating-2:0.5")

    submit_button = st.form_submit_button("Check Compliance 🚀")

if submit_button:
    # Prepare transaction data
    transaction_data = {}
    if section == "H1":
        transaction_data = {
            "Customer ID": customer_id,
            "Internal ID": internal_id,
            "Original Internal ID": original_internal_id,
            "Obligor Name": obligor_name,
            "City": city,
            "Country": country,
            "Zip Code": zip_code,
            "Industry Code": industry_code,
            "Industry Code Type": industry_code_type,
            "Obligor Internal Risk Rating": risk_rating,
            "TIN": tin,
            "Stock Exchange": stock_exchange,
            "Ticker Symbol": ticker_symbol,
            "CUSIP": cusip,
            "Internal Credit Facility ID": internal_credit_facility_id,
            "Original Internal Credit Facility ID": original_internal_credit_facility_id,
            "Origination Date": str(origination_date),
            "Maturity Date": str(maturity_date),
            "Credit Facility Type": credit_facility_type,
            "Other Credit Facility Type": other_credit_facility_type,
            "Credit Facility Purpose": credit_facility_purpose,
            "Other Credit Facility Purpose": other_credit_facility_purpose,
            "Committed Exposure": committed_exposure,
            "Utilized Exposure": utilized_exposure
        }
    elif section == "H2":
        transaction_data = {
            "Loan Number": loan_number,
            "Obligor Name": obligor_name,
            "Outstanding Balance": outstanding_balance,
            "Line Reported on FR Y-9C": line_reported,
            "Committed Exposure Global": committed_exposure_global,
            "Cumulative Charge-offs": cumulative_charge_offs,
            "Participation Flag": participation_flag,
            "Lien Position": lien_position,
            "Property Type": property_type,
            "Origination Date": str(origination_date),
            "Location": location,
            "Net Operating Income at Origination": noi_at_origination,
            "Value at Origination": value_at_origination,
            "Value Basis": value_basis,
            "Internal Rating": internal_rating
        }

    with st.spinner("Validating transaction..."):
        try:
            response = requests.post(f"{API_BASE_URL}{section}", json=transaction_data)
            if response.status_code == 200:
                compliance_result = response.json()
                st.subheader("✅ Compliance Result")
                if compliance_result["compliant"] == "Yes":
                    st.success("This transaction **complies** with all profiling rules. 🎉")
                else:
                    st.error("This transaction **does not comply** with profiling rules. ⚠️")
                st.metric(label="📊 Risk Score", value=f"{compliance_result['risk_score']}%")
                if compliance_result["violated_rules"]:
                    st.subheader("❌ Violated Rules")
                    for rule in compliance_result["violated_rules"]:
                        st.warning(f"- {rule}")
                if compliance_result["remedies"]:
                    st.subheader("🛠 Suggested Remedies")
                    for remedy in compliance_result["remedies"]:
                        st.info(f"- {remedy}")
            else:
                st.error("Error: Failed to validate transaction.")
                st.text(response.text)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
