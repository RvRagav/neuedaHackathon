import pandas as pd
import io
import streamlit as st
# For PDF extraction, you may use PyPDF2 or pdfplumber if needed

def extract_transactions(uploaded_file):
    if uploaded_file is None:
        return None
    filename = uploaded_file.name.lower()
    if filename.endswith(".csv"):
        try:
            df = pd.read_csv(uploaded_file)
            return df
        except Exception as e:
            st.error(f"Error reading CSV: {e}")
            return None
    elif filename.endswith(".pdf"):
        try:
            import pdfplumber
        except ImportError:
            st.error("pdfplumber is required for PDF extraction. Please install it with 'pip install pdfplumber'.")
            return None
        try:
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_file_path = tmp_file.name
            with pdfplumber.open(tmp_file_path) as pdf:
                text = "\n".join(page.extract_text() or "" for page in pdf.pages)
            # Try to extract table from PDF text (very basic, for demo)
            import re
            import pandas as pd
            # Try to find lines that look like CSV rows
            lines = [line for line in text.splitlines() if line.strip()]
            # Try to guess header and data
            header_idx = 0
            for i, line in enumerate(lines):
                if re.search(r"date", line, re.I) and re.search(r"amount", line, re.I):
                    header_idx = i
                    break
            data_lines = lines[header_idx:]
            if len(data_lines) < 2:
                return text  # Return raw text for categorizer
            # Try to parse as CSV
            try:
                from io import StringIO
                df = pd.read_csv(StringIO("\n".join(data_lines)))
                return df
            except Exception:
                return text  # Return raw text for categorizer
        except Exception as e:
            st.error(f"Error extracting PDF: {e}")
            return None
    else:
        st.error("Unsupported file type.")
        return None
