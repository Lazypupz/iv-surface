# Implied Volatility Surface

hobby project after reading paul wilmott intro to quant finance. threw this together on a week-end and sold my exams. 2nd python ,project production level ofc. 
whats _pycache_ btw???

**Status:** still lots TODO

## Overview

Displays implied volatilty surface (and skew) of option chains from tickers FROM Yahoo finance.

## Features

- Fetch live options data by ticker symbol
- View implied volatility skew (2d graph) for a specific expiry date #never knew of skew before this.
- Visualize 3D volatility surface across all available expirations
- Switch between call and put options
- 10 second load for the surface :D
- surface is missing surface area due to limited market data or my code (probably the latter)
- will not assist you in trading whatsoever...

## Setup

### Prerequisites

- Python 3.9+
- ```bash
   pip install -r requirements.txt
  ```

### Installation

1. Clone the repo and navigate to the project directory:
   ```bash
   cd implied-volatility
   ```

2. Install dependicies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the App

From the project root:

```bash
cd src/implied_volatility
streamlit run main.py
```

The app will open at `http://localhost:8501`.

## Usage

1. **Enter a ticker** (e.g., `AAPL`, `TSLA`) and click Submit #defaults to AAPL
2. **Select expiry**:
   - `All Expiries` – shows a 3D surface across all available expirations
   - A specific date – shows the 2D volatility skew for that expiry
3. **Choose option type** – `call` or `put`
4. **View the plots** – interactive Plotly charts

## License

MIT
