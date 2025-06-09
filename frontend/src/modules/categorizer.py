import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

def categorize_transactions(transactions_df):
    # Try to load from .env if not already loaded
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        st.info("GOOGLE_API_KEY environment variable not set. Please set it in your environment before running the app. Example (in PowerShell):")
        st.code("$env:GOOGLE_API_KEY = 'your-gemini-api-key'")
        return None
    # Prepare prompt for Gemini
    if hasattr(transactions_df, 'to_csv'):
        # DataFrame (CSV or parsed PDF)
        prompt = (
            "Categorize the following bank transactions into categories such as Food, Travel, Utilities, Shopping, etc. "
            "Return ONLY the total amount for each category as a table with columns: Category, TotalAmount. Do not include individual transactions.\n"
            f"Transactions:\n{transactions_df.to_csv(index=False)}"
        )
    elif isinstance(transactions_df, str):
        # Raw text from PDF
        prompt = (
            "The following is a raw text dump of a bank statement. "
            "Extract all transactions and aggregate them into categories such as Food, Travel, Utilities, Shopping, etc. "
            "Return ONLY the total amount for each category as a table with columns: Category, TotalAmount. Do not include individual transactions.\n"
            f"Bank Statement Text:\n{transactions_df}"
        )
    else:
        st.error("Unsupported data format for categorization.")
        return None
    try:
        # Use the correct model name for Gemini 1.5 Pro
        llm = ChatGoogleGenerativeAI(api_key=api_key, model="gemini-2.0-flash")
        response = llm([HumanMessage(content=prompt)])
        print(response.content)
        # Try to parse the response as a table
        # st.write("Gemini response:", response.content)  # Optionally log for debugging
        return response.content
    except Exception as e:
        st.error(f"Error with Gemini API: {e}")
        return None
