import streamlit as st
import pandas as pd
import openai
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set OpenAI API Key (Replace with your API Key)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Streamlit App
st.title("📊 AI-Powered Data Insights Chatbot")
st.write("Upload a dataset and ask AI to generate insights!")

# File Upload
uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:
    # Load Data
    file_ext = uploaded_file.name.split(".")[-1]
    if file_ext == "csv":
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    
    st.write("### Preview of Data:")
    st.dataframe(df.head())
    
    # User Query Input
    user_query = st.text_input("Ask a question about the data:")
    
    if user_query:
        prompt = f"Analyze the following dataset and answer the query.\n\nDataset:\n{df.head(5).to_string()}\n\nQuery: {user_query}\n"
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are a data analysis assistant."},
                      {"role": "user", "content": prompt}]
        )
        
        ai_response = response["choices"][0]["message"]["content"]
        
        st.write("### AI Response:")
        st.write(ai_response)
    
    # Visualization Option
    if st.button("Generate Summary Statistics & Charts"):
        st.write("### Summary Statistics:")
        st.write(df.describe())
        
        st.write("### Data Distribution:")
        num_cols = df.select_dtypes(include=['number']).columns
        for col in num_cols:
            fig, ax = plt.subplots()
            sns.histplot(df[col], kde=True, ax=ax)
            st.pyplot(fig)
