import streamlit as st
import pandas as pd
import io
import re
from modules.file_upload import upload_bank_statement
from modules.extractor import extract_transactions
from modules.categorizer import categorize_transactions
st.title("Bank Statement Analyzer")

uploaded_file = upload_bank_statement()

if uploaded_file:
    transactions = extract_transactions(uploaded_file)
    
    if transactions is not None:
        st.header("2. Process and Categorize")
        categorized_output = categorize_transactions(transactions)
        
        # ----------------------------------------------------------------------
        # FINAL CORRECTED PARSING LOGIC
        # ----------------------------------------------------------------------
        
        if isinstance(categorized_output, str) and categorized_output.strip():
            st.write("#### Raw Markdown Output from Categorizer:")
            st.code(categorized_output, language='markdown')
            
            try:
                lines = categorized_output.strip().split('\n')
                if lines and '```' in lines[0] and '```' in lines[-1]:
                    table_lines = lines[1:-1]
                else:
                    table_lines = lines

                filtered_lines = [
                    line.strip() for line in table_lines
                    if line.strip() and '---' not in line
                ]

                if len(filtered_lines) < 2:
                    st.error("Parsing Error: After cleaning, not enough lines remain to form a table.")
                else:
                    table_as_string = '\n'.join(filtered_lines)
                    
                    # Use pandas to read the string.
                    df = pd.read_csv(
                        io.StringIO(table_as_string),
                        sep=r'\s*\|\s*',
                        engine='python',
                        skipinitialspace=True,
                        thousands=','  # <-- THE FIX IS HERE. This tells pandas to treat ',' as a thousands separator.
                    ).dropna(axis=1, how='all')

                    df.columns = [col.strip().lower().replace(' ', '') for col in df.columns]

                    if 'category' in df.columns and 'totalamount' in df.columns:
                        # The to_numeric call is now simpler as the thousands separator is already handled.
                        df['totalamount'] = pd.to_numeric(df['totalamount']).fillna(0)
                        
                        result_json = {
                            "categories": df['category'].tolist(),
                            "totalAmount": df['totalamount'].tolist()
                        }
                        
                        st.header("3. Final JSON Output")
                        st.json(result_json)
                        
                    else:
                        st.error("Parsing Error: Could not find 'Category' and 'TotalAmount' columns.")
                        st.text("Detected columns:")
                        st.write(df.columns.tolist())

            except Exception as e:
                st.error(f"A critical error occurred during parsing: {e}")

        elif isinstance(categorized_output, str):
            st.error("The categorizer returned an empty string.")
        else:
            st.error(f"The categorizer returned an unexpected data type: {type(categorized_output).__name__}")
        # ----------------------------------------------------------------------
        # END OF PARSING LOGIC
        # ----------------------------------------------------------------------
    else:
        st.error("Could not extract transactions from the uploaded file.")

else:
    st.info("Please upload a bank statement to begin.")