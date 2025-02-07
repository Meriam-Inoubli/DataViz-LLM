import streamlit as st
import pandas as pd
import anthropic  
import matplotlib.pyplot as plt
import re
from dataviz_project.data_transformation import (
    summarize_data,
    handle_duplicates, 
    handle_outliers,
    handle_missing_values
)
from utils import load_dataset


# Load environment variables (API key)


# Helper function to interact with Claude API
def query_claude(prompt: str,api_key) -> str:
    """
    Sends a request to Claude (Anthropic) API and returns the response.
    """
    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",  
        messages=[{"role": "user", "content": prompt}],
        max_tokens=8000
    )
    return response.content[0].text.strip()

# Analyze the user query: Identify what type of question is being asked about the dataset
def analyze_query(user_request: str,api_key) -> str:
    """
    Analyzes the user request and provides a summary of what data is involved and what visualization is needed.
    """
    prompt = f"""
    Given the user's request, summarize the following:
    - What is the specific question about the dataset (e.g., trends, distributions, comparisons)?
    - What type of data is involved (categorical, numerical, time-series)?
    - What key insights or visualizations should be provided to answer the question?

    User Request:
    "{user_request}"
    """
    return query_claude(prompt,api_key)

# Select appropriate visualizations based on the dataset and question
def select_best_visualization(data: pd.DataFrame, user_request: str,api_key) -> str:
    """
    Based on the dataset summary and the user's request, recommend the three most effective visualization techniques while ensuring compliance with data visualization best practices:
    """
    dataset_summary = data.describe(include='all').to_string()
    prompt = f"""
    Based on the dataset summary and the user's request, recommend the three most effective visualization techniques while ensuring compliance with data visualization best practices:
    -Clearly specify the type of visualization in 2 sentences (e.g., line chart, bar chart, heatmap, box plot).
    -Justify why each visualization is the most suitable choice given the dataset and the analytical goal in 2 sentences.
    -Consider factors like data clarity, ease of interpretation, and suitability for large datasets in 2 sentences.
    -If applicable, suggest enhancements like color schemes, annotations, or interactive elements that improve user experience in 2 sentences.
    
    Dataset Summary:
    {dataset_summary}

    User Request:
    {user_request}

    Provide a list of 3 visualization types that are most suited for answering this question.
    """
    return query_claude(prompt,api_key)

# Generate Python code for the selected visualization types
def generate_visualization_code(data: pd.DataFrame, visualization_types: str, user_request: str,api_key) -> str:
    """
    Based on the user's request and dataset, generate Python code to implement the selected visualizations.
    """
    dataset_info = data.dtypes.to_string()
    prompt = f"""
    Based on the dataset and user request, generate Correct Python code for the following visualizations using matplotlib, seaborn, or plotly:
    - {visualization_types}

    Dataset Columns and Types:
    {dataset_info}

    User Request:
    {user_request}

    Guidelines:
    -Use the DataFrame variable name df.
    -Import all the necessary libraries you need for the visualizations.
    -The code should be optimized and correct for Streamlit and ensure clear, precise, and well-structured visualizations.
    -Apply appropriate titles, axis labels, legends, and color schemes for readability.
    -Use gridlines, annotations, and formatting enhancements where relevant.
    -Ensure the code is executable without requiring modifications.
    -Return only the Python code; do not include explanations.
    """
    return query_claude(prompt,api_key)

# Explain why specific visualizations are appropriate for the user's request
def explain_visualization_choice(visualization_types: str, user_request: str,api_key) -> str:
    """
    Explain why each of the following visualizations is the best choice for answering the user's question, ensuring clarity and alignment with best practices:
    Provides an interpretation of each visualization and how it helps in answering the question.
    """
    prompt = f"""
    -Provide a brief but precise explanation for each visualization.
    -Clearly describe what insights each visualization will reveal.
    -For each visualization, explain how it answers the specific question posed by the user and the insights it provides.
    -Interpret the visualizations in the context of the dataset and the user's request.
   
    Visualization Types: {visualization_types}

    User Request:
    {user_request}
    """
    return query_claude(prompt,api_key)

# Main Streamlit interface for chatbot
def chatbot_interface_claude(api_key):
    st.title("💬 AI Chatbot for Data Visualization")
    uploaded_file = st.file_uploader("📂 Please upload your dataset (CSV, Excel, JSON, PDF)", type=["csv", "xlsx", "json", "pdf"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)  
        st.session_state.transformed_df = df 
    
    if "transformed_df" in st.session_state and st.session_state.transformed_df is not None:
        df = st.session_state.transformed_df.copy()
        st.write("📂 **Current Dataset transformed:**")
        st.write("### 🔍 Preview of First Rows")
        st.dataframe(df.head())
    
    
    if uploaded_file:
        try:
            df = load_dataset(uploaded_file)
            if df is not None:
                # Appliquer la transformation par défaut
                df = handle_missing_values(df, "most_frequent")
                df = handle_duplicates(df, "Remove")
                df = handle_outliers(df, "Nothing")
                
                st.session_state.transformed_df = df
                st.success("✅ A default transformation has been applied to your data. You can customize it in the 'Data Transformation' section'.")
                
                st.subheader("📊 Transformed Dataset Preview")
                st.dataframe(df.head())
        except Exception as e:
            st.error(f"❌ Error processing file: {e}")

    for message in st.session_state.messages:
        st.chat_message(message["role"]).write(message["content"])

    # Show all previous visualizations if any
    if "visualizations" in st.session_state:
        for viz in st.session_state.visualizations:
            st.pyplot(viz)

    user_input = st.chat_input("Ask your question here...")
    
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)

        if  api_key and st.session_state.transformed_df is not None:
            with st.spinner("⏳ Processing your request..."):
                query_analysis = analyze_query(user_input,api_key)
                best_viz = select_best_visualization(df, user_input,api_key)
                explanation = explain_visualization_choice(best_viz, user_input,api_key)
                code = generate_visualization_code(df, best_viz, user_input,api_key)

                response = f"**🔍 Query Analysis:** {query_analysis}\n\n" \
                           f"**📊 Selected Visualization:** {best_viz}\n\n" \
                           f"**🖥 Generated Python Code:**\npython\n{code}\n"
                
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.chat_message("assistant").write(response)

                try:
                    match = re.search(r"python\n(.*?)\n", code, re.DOTALL)
                    python_code = match.group(1) if match else code
                    python_code = python_code.replace("plt.show()", "st.pyplot(plt)")

                    # Store visualization
                    fig, ax = plt.subplots(figsize=(8, 4))
                    exec(python_code, globals())
                    st.session_state.visualizations.append(fig)
                    
                    # Display the visualization
                    st.pyplot(fig)
                except Exception as e:
                    error_msg = f"⚠️ Error executing visualization: {e}"
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
                    st.chat_message("assistant").write(error_msg)
        else:
            st.info("🔹 Please enter your API key and upload a dataset to get started!")
# Run the app
if __name__ == "__main__":
    chatbot_interface()