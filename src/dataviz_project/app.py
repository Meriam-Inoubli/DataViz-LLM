import streamlit as st

from Claude_chat_responses import chatbot_interface_claude
from Gemini_chat_responses import chatbot_interface_gemini
from data_transformation_page import data_transformation_pagee
from utils import display_about_page

# Configuration de l'application
st.set_page_config(page_title="QueryGenius", page_icon="🤖", layout="wide")


st.markdown("""
    <style>
        .title-container {
            margin-top: 0px; /* Reducing space above */
            margin-bottom: 5px; /* Optional: Reducing space below */
        }
    </style>
    <div class="title-container">
        <h2 style='text-align: center;'>🚀 Unlock the Power of Data & Chat with</h2>
        <h1 style='text-align: center; font-weight: bold;'>QueryGenius </h1>
    </div>
""", unsafe_allow_html=True)

# Initialize session state for storing transformed data
if "transformed_df" not in st.session_state:
    st.session_state.transformed_df = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "visualizations" not in st.session_state:
    st.session_state.visualizations = []

# Barre latérale pour la navigation
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>QueryGenius</h2>", unsafe_allow_html=True)
    page = st.radio("Go to", ["How to use", "Chatbot", "Data Transformation", "About"])
    if page == "Chatbot":
       st.subheader("API Configuration")

       # Dropdown list to choose the API
       api_choice = st.selectbox("Select an API:", ["Claude", "Gemini"])

        # Input field for the API key based on the selection
       if api_choice == "Claude":
            api_key1 = st.text_input("Enter your Claude API key:", type="password")
            st.write(f"Currently using: Claude API")
       else:
            api_key2 = st.text_input("Enter your Gemini API key:", type="password")
            st.write(f"Currently using: Gemini API")
# Affichage des différentes pages en fonction du choix de l'utilisateur
if page == "Chatbot":
    if api_choice == "Claude":
       chatbot_interface_claude(api_key1)
    else:
       chatbot_interface_gemini(api_key2)
elif page == "Data Transformation":
    data_transformation_pagee()
elif page == "About":
    display_about_page()
else:
    st.markdown("""
         
        This application allows you to interact with a chatbot and perform data cleaning and transformation.  
        Below is a guide on how to use each section:
    """)

    st.subheader("🤖 Chatbot")
    st.markdown("""
        - Navigate to the **Chatbot** page from the sidebar.
        - Choose the type of API key you possess and upload your dataset.
        - A set of default transformations will be applied to your dataset.
        - You can **customize the transformations** by visiting the **Data Transformation** section.
        - Once your dataset is transformed, you can **query your database using the LLM** to display visualizations.
    """)

    st.subheader("📊 Data Transformation")
    st.markdown("""
        - Go to the **Data Transformation** section.
        - Upload a dataset in **CSV, Excel, JSON, or PDF** format.
        - The app will **analyze your data** and display an overview.
        - You can perform the following transformations:
            - **Handle missing values**: Fill missing data with mean, median, or most frequent values, or drop them.
            - **Remove duplicates**: Choose whether to keep or delete duplicate rows.
            - **Handle outliers**: Apply transformations like logarithmic scaling or replace extreme values with mean/median.
        - Once the transformations are applied, you can **download the cleaned dataset**.
    """)

    st.subheader("ℹ️ About")
    st.markdown("""
        - Check the **About** page for more details on this project and its purpose.
    """)

    st.success("🚀 You are now ready to use the app! Select a section from the sidebar.")
