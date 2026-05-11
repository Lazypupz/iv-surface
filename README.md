# Implied Volatility Surface

<<<<<<< HEAD
hobby project after reading paul wilmott intro to quant finance. threw this together on a week-end.
(image.png)
=======
toy project after reading paul wilmott intro to quant finance

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
>>>>>>> d5ad2bfb2be04d007bbed4c6a3d20f5abb58887c

### Prerequisites

- Python 3.9+

### Installation

if you can't figure it out, you don't deserve the bloat.

## Running the App

From the project root:

```bash
cd src/implied_volatility
streamlit run main.py
or
python -m streamlit run main.py
```

The app will open at `http://localhost:8501`.

## License

MIT
