import streamlit as st
import pandas as pd
from preprocess import load_data, get_summary, handle_missing_values, remove_duplicates, scale_features

st.set_page_config(layout="wide")
st.title("Data Preprocessing Chatbot")

# --- Helper function to convert DataFrame to CSV for download ---
@st.cache_data
def convert_df_to_csv(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False).encode('utf-8')

# --- Callback function to process missing values ---
def process_missing_values():
    strategy_key = st.session_state.missing_values_select
    if strategy_key == 'None':
        return
    df_copy = st.session_state.df_processed.copy()
    if strategy_key == 'Drop Rows with Missing Values':
        st.session_state.df_processed = handle_missing_values(df_copy, strategy='drop')
        st.success("Dropped rows with missing values.")
    elif strategy_key == 'Fill with Mean':
        st.session_state.df_processed = handle_missing_values(df_copy, strategy='mean')
        st.success("Filled missing values with the mean.")
    elif strategy_key == 'Fill with Median':
        st.session_state.df_processed = handle_missing_values(df_copy, strategy='median')
        st.success("Filled missing values with the median.")
    elif strategy_key == 'Fill with Mode':
        st.session_state.df_processed = handle_missing_values(df_copy, strategy='mode')
        st.success("Filled missing values with the mode.")

# --- Sidebar for Upload and Control ---
with st.sidebar:
    st.header("1. Upload Data")
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"], key="file_uploader")
    if 'df_original' not in st.session_state: st.session_state.df_original = None
    if 'df_processed' not in st.session_state: st.session_state.df_processed = None

# --- Main App Logic ---
if uploaded_file is not None and st.session_state.df_original is None:
    df = load_data(uploaded_file)
    if isinstance(df, pd.DataFrame):
        st.session_state.df_original = df.copy()
        st.session_state.df_processed = df.copy()
    else:
        st.error(df)
        st.session_state.df_original = None

# --- Display Data and Controls if DataFrame exists ---
if st.session_state.df_processed is not None:
    with st.sidebar:
        st.header("2. Preprocessing Options")
        if st.button("Reset Data to Original"):
            st.session_state.df_processed = st.session_state.df_original.copy()
            st.session_state.missing_values_select = 'None'
            st.success("Data has been reset to its original state.")
            st.rerun()
        show_summary_btn = st.button("Show Data Summary")
        st.subheader("Handle Missing Values")
        st.selectbox(
            "Choose a method:",
            options=['None', 'Drop Rows with Missing Values', 'Fill with Mean', 'Fill with Median', 'Fill with Mode'],
            key='missing_values_select',
            on_change=process_missing_values
        )
        remove_duplicates_btn = st.button("Remove Duplicates")
        st.subheader("Scale Numerical Features")
        numeric_cols = st.session_state.df_processed.select_dtypes(include=['number']).columns.tolist()
        if numeric_cols:
            cols_to_scale = st.multiselect("Select columns to scale:", options=numeric_cols, key='scale_cols')
            scaling_method = st.selectbox("Choose a scaling method:", options=['Normalize (Min-Max)', 'Standardize (Z-score)'], key='scaling_method')
            apply_scaling_btn = st.button("Apply Scaling")
        else:
            st.warning("No numerical columns available to scale.")
            apply_scaling_btn = False
        
        # --- NEW: Download Button ---
        st.header("3. Download Processed Data")
        csv_data = convert_df_to_csv(st.session_state.df_processed)
        st.download_button(
            label="Download data as CSV",
            data=csv_data,
            file_name='processed_data.csv',
            mime='text/csv',
        )

    # --- Button-Click Action Logic ---
    if remove_duplicates_btn:
        rows_before = len(st.session_state.df_processed)
        st.session_state.df_processed = remove_duplicates(st.session_state.df_processed)
        rows_after = len(st.session_state.df_processed)
        duplicates_removed = rows_before - rows_after
        st.success(f"Found and removed {duplicates_removed} duplicate row(s).")
        st.rerun()

    if apply_scaling_btn:
        if not cols_to_scale:
            st.warning("Please select at least one column to scale.")
        else:
            method_map = {'Normalize (Min-Max)': 'normalize', 'Standardize (Z-score)': 'standardize'}
            selected_method = method_map[scaling_method]
            st.session_state.df_processed = scale_features(st.session_state.df_processed, columns=cols_to_scale, method=selected_method)
            st.success(f"Successfully applied {scaling_method} to the selected columns.")
            st.rerun()

    # --- Main panel for displaying results ---
    st.header("Current Data Preview")
    st.dataframe(st.session_state.df_processed.head())
    
    if show_summary_btn:
        st.subheader("Data Summary")
        summary = get_summary(st.session_state.df_processed)
        st.markdown("##### Missing Values Count"); st.text(summary['missing_values'])
        st.markdown("##### Data Types and Info"); st.text(summary['info'])
        st.markdown("##### Descriptive Statistics"); st.text(summary['description'])
else:
    st.info("Awaiting CSV file upload. Please upload a file in the sidebar.")

