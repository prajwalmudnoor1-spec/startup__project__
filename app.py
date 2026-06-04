import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Startup Data Viewer",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 Startup Data Viewer")
st.write("Upload and explore startup data.")

# Load dataset
try:
    df = pd.read_csv("startup_data.csv")

    # Display dataset
    st.subheader("Dataset Preview")
    st.dataframe(df, use_container_width=True)

    # Dataset information
    st.subheader("Dataset Information")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Rows", df.shape[0])

    with col2:
        st.metric("Columns", df.shape[1])

    # Column names
    st.subheader("Columns")
    st.write(df.columns.tolist())

    # Summary statistics
    st.subheader("Summary Statistics")
    st.dataframe(df.describe())

    # Missing values
    st.subheader("Missing Values")
    missing_values = df.isnull().sum()
    st.dataframe(missing_values[missing_values > 0])

    # Select column for inspection
    st.subheader("Column Explorer")
    selected_column = st.selectbox(
        "Select a column",
        df.columns
    )

    st.write(f"### Values from '{selected_column}'")
    st.write(df[selected_column])

except FileNotFoundError:
    st.error(
        "❌ startup_data.csv not found. "
        "Make sure the file is in the same folder as app.py."
    )
except Exception as e:
    st.error(f"An error occurred: {e}")
