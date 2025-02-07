import os
import pandas as pd
import numpy as np
import streamlit as st
import pdfplumber
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import zscore



def pdf_to_dataframe(uploaded_file):
    with pdfplumber.open(uploaded_file) as pdf:
        tables = []
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                tables.append(pd.DataFrame(table[1:], columns=table[0]))
        return pd.concat(tables, ignore_index=True) if tables else None

# 📌 Function to display a detailed summary of the data
def summarize_data(df):
    st.subheader("📊 Dataset Summary")

    col1, col2 = st.columns(2)  

    with col1:
        st.write("### 📋 General Statistics")
        summary_df = pd.DataFrame({
            "Statistic": ["Number of rows", "Number of columns", "Missing values", "Duplicates"],
            "Value": [df.shape[0], df.shape[1], df.isnull().sum().sum(), df.duplicated().sum()]
        })
        st.dataframe(summary_df, hide_index=True, use_container_width=True)

    with col2:
        st.write("### 📑 Data Types")
        dtype_df = pd.DataFrame({
            "Column": df.columns,
            "Type": df.dtypes.astype(str)
        })
        st.dataframe(dtype_df, hide_index=True, use_container_width=True)

    st.write("### 🔍 Preview of First Rows")
    st.dataframe(df.head())

# 📌 Function to handle missing values
def handle_missing_values(df, strategy="mean"):
    if df.isnull().sum().sum() == 0:
        return df

    st.write(f"🛠 **Handling Missing Values:** `{strategy}`")
    if strategy == "mean":
        df.fillna(df.select_dtypes(include=["number"]).mean(), inplace=True)
        df.fillna(df.select_dtypes(exclude=["number"]).mode().iloc[0], inplace=True)
    elif strategy == "median":
        df.fillna(df.select_dtypes(include=["number"]).median(), inplace=True)
        df.fillna(df.select_dtypes(exclude=["number"]).mode().iloc[0], inplace=True)
    elif strategy == "most_frequent":
        df.fillna(df.mode().iloc[0], inplace=True)
    elif strategy == "drop":
        df.dropna(inplace=True)

    
    return df

# 📌 Function to remove duplicates
def handle_duplicates(df, handle_dupes="Remove"):
    before = df.shape[0]

    if handle_dupes == "Remove":
        df = df.drop_duplicates()
        after = df.shape[0]
        st.write(f"🔄 **Duplicate Removal:** {before - after} rows removed")
    else:
        st.write("✅ **No duplicate removal.** Data remains unchanged.")



    return df

# 📌 Function to handle outliers with strategy selection
def handle_outliers(df, strategy="Nothing", threshold=3):
    # Sélectionner les colonnes numériques
    numeric_cols = df.select_dtypes(include=[np.number])

    if numeric_cols.empty:
        st.warning("⚠️ No numerical columns found. No outlier treatment applied.")
        return df

    # Calculer les scores Z pour identifier les outliers
    z_scores = np.abs(zscore(numeric_cols, nan_policy="omit"))
    outliers = z_scores > threshold

    if strategy == "Nothing":
        return df

    elif strategy == "Log_transformation":
        st.write("🛠 **Applying logarithmic transformation to outliers.**")
        for col in numeric_cols.columns:
            df[col] = df[col].apply(lambda x: np.log(x + 1) if x > 0 else x)

    elif strategy == "Mean":
        st.write("🛠 **Replacing outliers with mean.**")
        for col in numeric_cols.columns:
            mean_val = df[col].mean()
            df.loc[outliers[:, numeric_cols.columns.get_loc(col)], col] = mean_val

    elif strategy == "Median":
        st.write("🛠 **Replacing outliers with median.**")
        for col in numeric_cols.columns:
            median_val = df[col].median()
            df.loc[outliers[:, numeric_cols.columns.get_loc(col)], col] = median_val

    elif strategy == "Drop":
        st.write(f"🛠 **Removing rows containing outliers.**")
        before = df.shape[0]
        df = df[~outliers.any(axis=1)]
        after = df.shape[0]
        st.write(f"🚀 **Outliers removed:** {before - after} rows")

    return df