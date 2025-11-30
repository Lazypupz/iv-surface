import numpy as np
import pandas as pd
from datetime import datetime, timezone

MIN_STRIKES_PER_EXPIRY = 12
MAX_BID_ASK_PCT = 0.2

def time_to_expiry_years(expiry_date, now=None):
    now = now or datetime.now(timezone.utc)
    if isinstance(expiry_date, pd.Timestamp):
        expiry_date = expiry_date.to_pydatetime()
    else:
        expiry = expiry_date
    secs = (expiry_date - now).total_seconds()
    return max(secs / (365.00 * 24 * 3600), 0)

def clean_option_chain(df):
    df = df.copy()

