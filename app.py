# Import necessary libraries
from dotenv import load_dotenv
import streamlit as st
import os
import sqlite3
import google.generativeai as generativeai
import kagglehub

# Load environment variables
load_dotenv()

# Configure Google Gemini API
generativeai.configure(api_key=os.getenv("GOOGLE_GEMINI_KEY"))


# Download the latest version of the Meta Kaggle dataset
def download_kaggle_data():
    path = kagglehub.dataset_download("kaggle/meta-kaggle-code")
    print("Path to dataset files:", path)
    return path


# Function to get response from Gemini Pro for Python code generation
def get_gemini_code(prompt):
    try:
        model = generativeai.GenerativeModel(model_name="models/gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Error generating code: {str(e)}"


# Function to execute generated SQL queries
def read_sql_query(sql, db):
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        conn.commit()
        conn.close()
        return rows
    except Exception as e:
        return [f"❌ SQL execution error: {str(e)}"]


# Predefined prompt for code generation based on the Meta Kaggle dataset
prompt = """
I want you to work as a Python code expert who can generate scripts for data processing based on Meta Kaggle dataset.
For example, a question could be: "generate code to load the Meta Kaggle dataset",
The response could be:
import pandas as pd
data = pd.read_csv('Meta_Kaggle.csv')
"""

# Streamlit app for user interaction
st.set_page_config(page_title="LLM Code Generator by chibihime >u<")
st.header("Kaggle Code Generator using Gemini Pro API")

# Download the Kaggle dataset and display path to the user
if st.button("Download Meta Kaggle Dataset"):
    dataset_path = download_kaggle_data()
    st.write("✅ Dataset downloaded to:", dataset_path)

# Input from user
user_input = st.text_input("Ask for code generation:", key="input")
submit = st.button("Generate Code")

# Trigger code generation
if submit and user_input.strip():
    st.subheader("Generated Code:")
    code_response = get_gemini_code(user_input)
    st.code(code_response, language="python")

    # Run SQL query if relevant
    if "select" in user_input.lower() or "sql" in user_input.lower():
        st.subheader("Query Results:")
        result = read_sql_query(code_response, "meta_kaggle.db")
        for row in result:
            st.write(row)
