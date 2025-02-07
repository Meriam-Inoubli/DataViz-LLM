import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from utils import load_dataset

from dataviz_project.data_transformation import (
    summarize_data,
    handle_duplicates, 
    handle_outliers,
    handle_missing_values
)

def data_transformation_pagee():
    st.title("📊 Data Cleaning & Transformation")
    uploaded_file = st.file_uploader("Upload your dataset (CSV, Excel, JSON, PDF)", type=["csv", "xlsx", "json", "pdf"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)  
        st.session_state.transformed_df = df
    if uploaded_file:
        try:
            df = load_dataset(uploaded_file)
            if df is not None:
                summarize_data(df)
               
                # Handling missing values
                st.subheader("💪 Handle Missing Values")
                strategy = st.selectbox("Select strategy", ["mean", "median", "most_frequent", "drop"])
                df = handle_missing_values(df, strategy)
                st.write("### 🔍 Preview After Handling Missing Values")
                st.dataframe(df.head())
                st.session_state.transformed_df = df

                # Handling duplicates
                st.subheader("🛠️ Handle Duplicates")
                handle_dupes = st.radio("Choose action", ["Keep", "Remove"])
                df = handle_duplicates(df, handle_dupes)
                st.write("### 🔍 Preview After Handling Duplicates")
                st.dataframe(df.head())
                st.subheader("🌟 Handle Outliers")
                outlier_strategy = st.selectbox("Choose strategy", ["Nothing", "Log_transformation", "Mean","Median","Drop"])
                df1 = df.copy()
                df1 = handle_outliers(df1, outlier_strategy)  # Appliquer la transformation sur la copie
                st.session_state.transformed_df = df1

                # 📌 Sélectionner une colonne numérique à visualiser
                numeric_cols = df.select_dtypes(include=[np.number])
                selected_col = st.selectbox("📊 Select a column to visualize:", numeric_cols.columns)

                # 📊 Visualization before transformation
                st.write(f"### 📊 Distribution of `{selected_col}` Before Handling")
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.hist(df[selected_col], bins=30, edgecolor="black", alpha=0.7, label="Before")
                ax.set_title(f"Distribution of `{selected_col}` Before Handling")
                ax.set_xlabel(selected_col)
                ax.set_ylabel("Frequency")
                st.pyplot(fig)

                # 📊 Visualization after transformation
                st.write(f"### 📊 Distribution of `{selected_col}` After Handling")
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.hist(df1[selected_col], bins=30, edgecolor="black", color="orange", alpha=0.7, label="After")
                ax.set_title(f"Distribution of `{selected_col}` After Handling")
                ax.set_xlabel(selected_col)
                ax.set_ylabel("Frequency")
                st.pyplot(fig)


                # Preview of data after transformation
                st.write("### 🔍 Preview After Handling Outliers")
                st.dataframe(df.head())
                st.success("Data transformation applied successfully!")
        except Exception as e:
            st.error(f"Error processing file: {e}")

                # 📤 Option pour télécharger le fichier transformé
        st.download_button(
                    label="📥 Télécharger les données transformées",
                    data=df.to_csv(index=False).encode("utf-8"),
                    file_name="data_cleaned.csv",
                    mime="text/csv"
                ) 
