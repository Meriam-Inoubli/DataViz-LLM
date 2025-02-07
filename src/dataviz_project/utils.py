import pandas as pd
import streamlit as st
import chardet 
# 📌 Function to detect file encoding
def detect_encoding(file):
    raw_data = file.read()
    result = chardet.detect(raw_data)
    return result['encoding']

# 📌 Function to load the file and detect encoding
def load_dataset(uploaded_file):
    try:
        file_extension = uploaded_file.name.split(".")[-1].lower()

        if file_extension == "csv":
            file_encoding = detect_encoding(uploaded_file)
            uploaded_file.seek(0)  
            df = pd.read_csv(uploaded_file, encoding=file_encoding, sep=None, engine="python")

        elif file_extension in ["xls", "xlsx"]:
            df = pd.read_excel(uploaded_file)

        elif file_extension == "json":
            df = pd.read_json(uploaded_file)

        elif file_extension == "pdf":
            with pdfplumber.open(uploaded_file) as pdf:
                text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
                df = pd.DataFrame([line.split() for line in text.split("\n") if line])
        elif file_extension == "pdf":
             df = pdf_to_dataframe(uploaded_file)

        else:
            st.error("❌ Unsupported format. Please upload a CSV, Excel, JSON, or PDF file.")
            return None

        return df

    except Exception as e:
        st.error(f"❌ Error loading the file: {str(e)}")
        return None


def display_about_page():
    """Affiche la page 'About'."""
    st.title("ℹ️ About QueryGenius")

    st.markdown("""
        **QueryGenius** is a powerful tool designed to simplify data transformations and make data analysis more accessible. The app leverages a **Large Language Model (LLM)** to provide intelligent insights and natural language querying capabilities.

        ### Developed By:
        - **Kabeda Hiba**: Hiba.kabada@dauphine.eu
        - **Inoubli Meriam**: Meriam.inoubli@dauphine.eu
               
        ### Under the guidance of:
        - **Professor Hadrien Mariaccia**
       
       
        ### Technologies Used:
        - **Large Language Model (LLM)**: Powers the chatbot and natural language processing.
        - **Streamlit**: Framework for building the interactive web interface.
        - **Pandas & Numpy**: For efficient data manipulation and analysis.
        - **Matplotlib & Seaborn**: Libraries for data visualization.
        - **PDFplumber**: Extracts data from PDF files for conversion to usable formats.

    """)

    st.markdown("""
        ---
        Made with ❤️
    """)
