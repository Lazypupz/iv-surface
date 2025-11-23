import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def _normalize_df(df):
    """Ensure expiry is date type and daystoexpiry is numeric type."""
    df = df.copy()
    if "expiry" in df.columns:
        df["expiry"] = pd.to_datetime(df["expiry"]).dt.date
    if "daystoexpiry" in df.columns:
        df["daystoexpiry"] = pd.to_numeric(df["daystoexpiry"], errors="coerce")
    return df

def create_3d_surface(df, option_type, selected_expiry=None):

    if df["expiry"].nunique() > 1 and df["strike"].nunique() > 1:
        pivot = df.pivot_table(index="strike", columns='daystoexpiry', values="impliedVolatility")
        pivot = pivot.dropna(how="all", axis=0).dropna(how="all", axis=0)

        if pivot.shape[0] >= 2 and pivot.shape[1] >= 2:
            x = pivot.columns.values  # days to expiry
            y = pivot.index.values  # strike prices
            z = pivot.values      # implied volatilities

            surface = go.Figure(data=[go.Surface(z=z, x=x, y=y)])
            surface.update_layout(title=f"Implied Volatility Surface ({option_type})", autosize=False, width=800, height=800,
                                scene=dict(xaxis_title="Days to Expiration",
                                            yaxis_title="Strike Price",
                                            zaxis_title="Implied Volatility"))
            st.plotly_chart(surface, use_container_width=True)
        else:
            st.info("Not enough grid points across expirations and strikes to make a 3d surface")
    else:
        st.warning("Not enough expirations available for this ticker.")

    return surface

def make_skew_plot(df, option_type, selected_expiry):
    skew_df = df[["strike", "impliedVolatility"]].dropna()
    if skew_df.empty:
        st.info("No data for selected expiry")
        return

    skew_df = skew_df.sort_values('strike')

    skew_fig = go.Figure()
    skew_fig.add_trace(go.Scatter(x=skew_df['strike'], y=skew_df["impliedVolatility"],
                            mode='lines+markers', name='IV'))
    title = f'({option_type}) IV Skew for {selected_expiry}' if selected_expiry is not None else 'Call IV Skew'
    skew_fig.update_layout(title=title, xaxis_title='Strike', yaxis_title="impliedVolatility")

    return skew_fig


def plot_graph(df, option_type, selected_expiry):
    df = _normalize_df(df)

    if df.empty:
        st.info(f"No {option_type} option data available to plot.")
        return
    
    if selected_expiry is None:
        create_3d_surface(df, option_type, selected_expiry)
    else:
        skew_fig = make_skew_plot(df, option_type, selected_expiry)
        if skew_fig:
            st.plotly_chart(skew_fig, use_container_width=True)
        
    return

'''
def _filter_options_at_expiry(df, selected_expiry):
    df = df.copy()

    if selected_expiry is None:
        return
    options_at_expiry = df[df["expiry"] == pd.to_datetime(selected_expiry).date()]
    filtered_options_at_expiry = options_at_expiry[options_at_expiry["daystoexpiry"] == 0]
    filtered_options_at_expiry = filtered_options_at_expiry[filtered_options_at_expiry["impliedVolatility"] > 0.001]

def _filter_options_at_strike(df, strike_price):
    df = df.copy()

    options_at_strike = df[df["strike"] == strike_price]
    filtered_options_at_strike = options_at_strike[options_at_strike["impliedVolatility"] > 0.001]
    return filtered_options_at_strike
'''

    
    
    