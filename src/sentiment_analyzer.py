import pandas as pd

def rank_by_sentiment(df: pd.DataFrame, sentiment_col: str = "Final_Sentiment") -> pd.DataFrame:
    """
    Given a filtered dataframe, attach a 'Sentiment Score' column and
    return the dataframe sorted by sentiment (descending).
    This method uses the existing 'Final_Sentiment' numeric score
    previously computed for each product.
    """
    out = df.copy()
    # Ensure column exists and is numeric
    if sentiment_col not in out.columns:
        out['Final_Sentiment'] = 0.0

    out['Sentiment Score'] = pd.to_numeric(out.get(sentiment_col, 0.0), errors='coerce').fillna(0.0)

    # Sort descending by sentiment score (higher = better)
    out = out.sort_values(by='Sentiment Score', ascending=False)

    return out
