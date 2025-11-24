import streamlit as st
import pandas as pd
import re

def extract_number(value):
    """Extracts the first integer from a string."""
    if isinstance(value, str):
        match = re.search(r'(\d+)', value)
        if match:
            return int(match.group(1))
    return None

def extract_float(value):
    """Extracts the first float (e.g., 6.1) from a string."""
    if isinstance(value, str):
        match = re.search(r'(\d+\.?\d*)', value)
        if match:
            return float(match.group(1))
    return None

@st.cache_data
@st.cache_data
def load_data(csv_path: str = "data/final_data.csv"):
    """
    Loads product data from a CSV, cleans it for filtering,
    and caches the result. Now uses the local project CSV.
    """
    try:
        df = pd.read_csv(csv_path, encoding='latin-1')

        # --- Data Cleaning ---
        df['RAM_GB'] = df['RAM'].apply(extract_number)
        df['Battery_mAh'] = df['Battery Capacity'].apply(extract_number)
        df['Back_Camera_MP'] = df['Back Camera'].apply(extract_number)
        df['Front_Camera_MP'] = df['Front Camera'].apply(extract_number)
        df['Screen_Size_Inches'] = df['Screen Size'].apply(extract_float)

        # Clean India price
        df['Price_INR'] = (
            df['Launched Price (India)']
            .astype(str)
            .str.replace('INR', '', regex=False)
            .str.replace('₹', '', regex=False)
            .str.replace(',', '', regex=False)
            .str.replace(' ', '', regex=False)
        )
        df['Price_INR'] = pd.to_numeric(df['Price_INR'], errors='coerce')

        df['Launched Year'] = pd.to_numeric(df['Launched Year'], errors='coerce')

        # Ensure Final_Sentiment exists
        if 'Final_Sentiment' not in df.columns:
            df['Final_Sentiment'] = 0.0
        df['Final_Sentiment'] = pd.to_numeric(df['Final_Sentiment'], errors='coerce').fillna(0.0)

        # Add Tweet_Count if missing
        tweet_cols = [c for c in df.columns if c.startswith("Tweet_") or c.startswith("Gen_Tweet_")]
        if 'Tweet_Count' not in df.columns:
            df['Tweet_Count'] = df[tweet_cols].notna().sum(axis=1)

        return df

    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None


    except FileNotFoundError:
        st.error(f"Data file not found at {csv_path}. Please verify the path.")
        return None
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None
