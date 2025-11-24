import streamlit as st
import pandas as pd
from src.data_loader import load_data
from src.recommender import find_matching_products
from src.sentiment_analyzer import rank_by_sentiment

# --- Page Configuration ---
st.set_page_config(
    page_title="Mobile Recommender",
    page_icon="📱",
    layout="wide"
)

st.title("📱 Mobile Phone Recommender")
st.write("Find the perfect phone based on your specs, ranked by social sentiment!")

# --- Load Data ---
# Use the final_data.csv you produced earlier (this path is the one you gave me)
DATA_FILE = "data/final_data.csv"

df = load_data(DATA_FILE)

if df is not None:
    # --- Sidebar Filters ---
    st.sidebar.header("Filter Your Search")

    # Unique values
    unique_brands = sorted(df['Company Name'].dropna().unique().tolist())
    unique_processors = sorted(df['Processor'].dropna().unique().tolist())

    # Helper to safely get min/max
    def get_min_max(df, column, col_type=int):
        safe = df[column].dropna()
        if safe.empty:
            return (0, 100) if col_type == int else (0.0, 10.0)
        try:
            s = safe.astype(col_type)
            return (int(s.min()), int(s.max())) if col_type == int else (float(s.min()), float(s.max()))
        except Exception:
            return (0, 100) if col_type == int else (0.0, 10.0)

    min_price, max_price = get_min_max(df, 'Price_INR')
    min_ram, max_ram = get_min_max(df, 'RAM_GB')
    min_batt, max_batt = get_min_max(df, 'Battery_mAh')
    min_front_cam, max_front_cam = get_min_max(df, 'Front_Camera_MP')
    min_back_cam, max_back_cam = get_min_max(df, 'Back_Camera_MP')
    min_screen, max_screen = get_min_max(df, 'Screen_Size_Inches', float)
    min_year, max_year = get_min_max(df, 'Launched Year')

    # --- Create Widgets ---
    selected_brands = st.sidebar.multiselect("Brand", unique_brands, default=unique_brands)
    selected_processors = st.sidebar.multiselect("Processor", unique_processors)

    selected_max_price = st.sidebar.slider("Max Price (INR)", int(min_price or 0), int(max_price or 0), int(max_price or 0))

    st.sidebar.divider()

    selected_min_ram = st.sidebar.slider("Min RAM (GB)", int(min_ram or 0), int(max_ram or 0), int(min_ram or 0))
    selected_min_battery = st.sidebar.slider("Min Battery (mAh)", int(min_batt or 0), int(max_batt or 0), int(min_batt or 0))
    selected_min_front_cam = st.sidebar.slider("Min Front Camera (MP)", int(min_front_cam or 0), int(max_front_cam or 0), int(min_front_cam or 0))
    selected_min_back_cam = st.sidebar.slider("Min Back Camera (MP)", int(min_back_cam or 0), int(max_back_cam or 0), int(min_back_cam or 0))
    selected_min_screen = st.sidebar.slider("Min Screen Size (Inches)", float(min_screen or 0.0), float(max_screen or 0.0), float(min_screen or 0.0), step=0.1)
    selected_min_year = st.sidebar.slider("Min Launch Year", int(min_year or 0), int(max_year or 0), int(min_year or 0))

    # Store filters in a dictionary
    filters = {
        "brands": selected_brands,
        "processors": selected_processors,
        "max_price": selected_max_price,
        "min_ram": selected_min_ram,
        "min_battery": selected_min_battery,
        "min_front_camera": selected_min_front_cam,
        "min_back_camera": selected_min_back_cam,
        "min_screen_size": selected_min_screen,
        "min_launch_year": selected_min_year
    }

    # --- Main Page Logic ---
    if st.sidebar.button("Find Phones", type="primary"):
        # 1. Get filtered products
        recommended_products = find_matching_products(df, filters)

        if recommended_products.empty:
            st.warning("No products match your criteria. Please adjust your filters.")
        else:
            # 2. Rank them by sentiment
            st.subheader(f"Found {len(recommended_products)} matching phones. Ranking by sentiment...")
            with st.spinner("Analyzing social sentiment..."):
                ranked_products = rank_by_sentiment(recommended_products, sentiment_col='Final_Sentiment')

            st.success("Done! Here are your top recommendations:")

            # 3. Display results
            columns_to_show = [
                'Model Name',
                'Sentiment Score',
                'Price_INR',
                'RAM_GB',
                'Battery_mAh',
                'Front_Camera_MP',
                'Back_Camera_MP',
                'Screen_Size_Inches',
                'Launched Year',
                'Processor',
                'Company Name'
            ]

            display_df = ranked_products[columns_to_show].copy()
            # Format price for display
            display_df['Price_INR'] = display_df['Price_INR'].apply(lambda x: f"₹{int(x):,}" if pd.notna(x) else "N/A")

            st.dataframe(display_df, use_container_width=True, hide_index=True)
else:
    st.error("Could not load product data. Please check the 'data' file path.")
