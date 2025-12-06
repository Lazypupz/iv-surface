import numpy as np
import pandas as pd
from datetime import datetime, timezone
from scipy.interpolate import griddata

MIN_STRIKES_PER_EXPIRY = 8

def cleanAndProcess_option_data(df):

    #empty df NoneObject type has no attr empty or copy
    df = df.dropna(subset=["strike", "T", "impliedVolatility"])

    points = df[["T", "strike"]].values      
    values = df["impliedVolatility"].values
    
    #filtering out the expiries with less than 8 strikes.
    expiry_counts = df.groupby("T")["strikes"].count()
    liquid_expiries = expiry_counts[expiry_counts >= MIN_STRIKES_PER_EXPIRY].index()
    df = df[df["T"].isin(liquid_expiries)]

    #removing all IV's that are above 2.5. Due to the fact that 
    strike_grid = np.linspace(df["strike"].min(), df["strike"].max(), 50)
    T_grid = np.linspace(df["T"].min(), df["T"].max(), 50)
    X, Y = np.meshgrid(strike_grid, T_grid)
    
    Z = griddata(points, values, (X, Y), method="cubic")
    Z = np.clip(Z, 0.05, 2.5)

    return df, X, Y, Z, points, values


