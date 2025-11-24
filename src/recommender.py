import pandas as pd

def find_matching_products(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    """
    Filters the main DataFrame based on user-selected criteria.
    Returns filtered DataFrame (unsorted).
    """
    # Collect working copy and drop rows missing essential numeric fields for filtering
    results = df.copy().dropna(
        subset=[
            'Price_INR', 'RAM_GB', 'Battery_mAh', 'Front_Camera_MP',
            'Back_Camera_MP', 'Screen_Size_Inches', 'Launched Year'
        ],
        how='any'
    )

    # Apply brand and processor multi-selects
    if filters.get('brands'):
        results = results[results['Company Name'].isin(filters['brands'])]

    if filters.get('processors'):
        results = results[results['Processor'].isin(filters['processors'])]

    # Apply >= filters
    results = results[results['RAM_GB'] >= filters.get('min_ram', 0)]
    results = results[results['Battery_mAh'] >= filters.get('min_battery', 0)]
    results = results[results['Front_Camera_MP'] >= filters.get('min_front_camera', 0)]
    results = results[results['Back_Camera_MP'] >= filters.get('min_back_camera', 0)]
    results = results[results['Screen_Size_Inches'] >= filters.get('min_screen_size', 0.0)]
    results = results[results['Launched Year'] >= filters.get('min_launch_year', 0)]

    # Apply price <= filter
    results = results[results['Price_INR'] <= filters.get('max_price', results['Price_INR'].max())]

    return results
