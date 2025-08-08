import pandas as pd
from sklearn.preprocessing import MinMaxScaler , StandardScaler

def load_data(file_path):
    """Loads a csv file into a pandas DataFrame ."""

    try:
        df=pd.read_csv(file_path)
        print("File Loaded successfully .")
        return df
    
    except FileNotFoundError:
        return "Error : The file was not found."
    except Exception as e:
        return f"An error occurred :{e}"
    
def get_summary(df):
    """Returns a summary of the DataFrame include info , head , and
    descriptive stats. """

    summary={
        "head":df.head().to_string(),
        "info":df.info(buf=None) , #Get the information as a sting buffer later
        "description":df.describe().to_string(),
        "missing_values": df.isnull().sum().to_string()
    }

    # A bit of workaround to capture df.info() output
    import io
    buffer=io.StringIO()
    df.info(buf=buffer)
    summary["info"]=buffer.getvalue()

    return summary

# In preprocess.py

def handle_missing_values(df, strategy='drop', subset=None):
    """
    Handles missing values in the DataFrame using a specified strategy.
    Strategies: 'drop', 'mean', 'median', 'mode'. This version is robust against edge cases.
    """
    df_copy = df.copy()
    if strategy == 'drop':
        return df_copy.dropna(subset=subset)
        
    elif strategy == 'mean':
        numeric_cols = df_copy.select_dtypes(include=['number']).columns
        # THE FIX: Ensure we call the mean() function with parentheses
        df_copy[numeric_cols] = df_copy[numeric_cols].fillna(df_copy[numeric_cols].mean())
        return df_copy
        
    elif strategy == 'median':
        numeric_cols = df_copy.select_dtypes(include=['number']).columns
        # THE FIX: Ensure we call the median() function with parentheses
        df_copy[numeric_cols] = df_copy[numeric_cols].fillna(df_copy[numeric_cols].median())
        return df_copy
        
    elif strategy == 'mode':
        for column in df_copy.columns:
            # THE FIX: Check if mode is not empty before accessing it
            mode_value = df_copy[column].mode()
            if not mode_value.empty:
                df_copy[column].fillna(mode_value[0], inplace=True)
        return df_copy
        
    else:
        return "Error: Invalid missing value handling strategy."
    
def remove_duplicates(df):
    """Removes duplicate row from the DataFrame ."""
    return df.drop_duplicates()

def convert_data_type(df,column , new_type):
    """Converts a columns  to a specified data type"""
    try:
        df[column]=df[column].astype(new_type)
        return df
    except Exception as e:
        return f"Error converting {column} to {new_type} : {e}"
    
def scale_features(df, columns, method='normalize'):
    """Scales specified numerical columns using normalization
    or standardization. """

    if method =='normalize':
        scaler=MinMaxScaler()

    elif method == 'standardize':
        scaler= StandardScaler()

    else :
        return "Error : Invalid scaling method."
    
    df_copy =df.copy()
    # Ensure all specified columns are numeric before scaling
    numeric_columns_to_scale = [col for col in columns if 
    pd.api.types.is_numeric_dtype(df_copy[col])]

    if not numeric_columns_to_scale:
        return "Error : No numeric columns selected for scaling . "
    
    df_copy[numeric_columns_to_scale] = scaler.fit_transform(df_copy[numeric_columns_to_scale])
    
    return df_copy

