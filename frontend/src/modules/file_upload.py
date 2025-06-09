import streamlit as st

def upload_bank_statement():
    st.write("## Upload your bank statement (CSV or PDF)")
    uploaded_file = st.file_uploader("Choose a file", type=["csv", "pdf"])
    return uploaded_file
