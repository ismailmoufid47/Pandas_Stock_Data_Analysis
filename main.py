import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

default_symbol = "AAPL"
default_start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")

def prompt():
    global symbol
    global start_date
    global end_date
    symbol = input(f"Enter stock symbol, or press ENTER for default value, {default_symbol}: ") or default_symbol
    start_date = input(f"Enter start date (YYYY-MM-DD format, must be a year ago or further, or press ENTER for default value, {default_start_date}): ") or default_start_date
    end_date = (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=365)).strftime("%Y-%m-%d")

    if datetime.strptime(start_date, "%Y-%m-%d") >= datetime.now() - timedelta(days=365):
        print("Start date is invalid or not a year ago or further, please try again")
        prompt()

# Prompt for user input for symbol, start_date, and end_date
prompt()

def get_historical_data():
    try:
        global symbol
        global df
        df = yf.download(symbol, start=start_date, end=end_date)
        # Calculate daily returns
        df['Daily_Return'] = df['Adj Close'].pct_change()
    except:
        symbol = input(f"Invalid symbol, please Enter a valid symbol(default is {default_symbol}): ") or default_symbol
        get_historical_data()

get_historical_data()

# Calculate annualized volatility
annualized_volatility = df['Daily_Return'].std() * (252**0.5)  # Assuming 252 trading days in a year

# Calculate beta (market sensitivity)
market_data = yf.download('SPY', start=start_date, end=end_date)
market_returns = market_data['Adj Close'].pct_change()
beta = round(df['Daily_Return'].cov(market_returns) / market_returns.var(), 2)

# Define the report text
report_text = f"""
Analysis Report:

Analysis:
- Annualized Volatility: {annualized_volatility:.2%}%
- Beta: {beta}

Visualization:
- 30-Day Volatility Plot

Conclusions:"""

# Print the report to the terminal
print(report_text)

# Print statement based on annualized volatility
if annualized_volatility < 0.1:
    print(f"- {symbol}'s annualized volatility is low ({annualized_volatility:.2%}). It has relatively stable price movements.",)
elif 0.1 <= annualized_volatility < 0.3:
    print(f"- {symbol}'s annualized volatility is moderate ({annualized_volatility:.2%}). It experiences moderate price fluctuations.")
else:
    print(f"- {symbol}'s annualized volatility is high ({annualized_volatility:.2%}). It has significant price fluctuations.")

# Print statement based on beta
if beta == 1:
    print(f"- {symbol}'s beta is exactly 1, indicating it tends to move in line with the market.")
elif beta > 1:
    print(f"- {symbol}'s beta is {beta}, suggesting it is more volatile than the market.")
elif beta < 1:
    print(f"- {symbol}'s beta is {beta}, indicating it is less volatile than the market.")
else:
    print(f"Invalid beta value for {symbol}. Please check your data.")

# Calculate rolling 30-day volatility
rolling_volatility = df['Daily_Return'].rolling(window=30).std()

# Plot rolling volatility
rolling_volatility.plot(title=f'{symbol} 30-Day Volatility', figsize=(12, 6), legend=True, color='blue')

# Show the plot
plt.show()
