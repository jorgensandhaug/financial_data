"""
A script to get financial data from financial modeling prep API
"""

# Import libraries
import requests
import json
import pandas as pd

api_key = "39cd664ac80cfc25a7bc5913a1176bbb"

# Define function to get data
def get_data(ticker):
    """
    This function gets financial data from financial modeling prep API and return a dataframe where all non-empty numbers are converted to dollar values
    """

    # First check if the ticker is in list of all tickers from the API
    all_tickers = requests.get("https://financialmodelingprep.com/api/v3/company/stock/list?apikey=" + api_key)
    all_tickers = json.loads(all_tickers.text)
    all_tickers = all_tickers["symbolsList"]
    all_tickers = [t["symbol"] for t in all_tickers]

    # If the ticker is not in the list, print error message and return None
    if ticker not in all_tickers:
        print("Ticker not found")
        return None





    # Get data from financial modeling prep API
    url = f"https://financialmodelingprep.com/api/v3/financials/income-statement/{ticker}?apikey={api_key}"
    response = requests.get(url)
    # Check if the response is valid
    if response.status_code != 200:
        print("Error: Please check the ticker symbol")
        return None
    data = json.loads(response.text)
    
    # Convert data to a dataframe if successful
    df = pd.DataFrame(data["financials"])
    
    # Convert date column to datetime
    df["date"] = pd.to_datetime(df["date"])

    # Convert all non-empty numbers to float
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].apply(lambda x: float(x.replace(",", "")) if x != "" else x)
    


    # transpose dataframe
    df = df.T
    # make first row columns, and remove first row
    df.columns = df.iloc[0]
    df = df.iloc[1:]

    # Return the dataframe
    return df




"""
get data for ticker and save to .xlsx file
"""

# Get data for ticker
ticker = "AAPL"
df = get_data(ticker)

# If data is not empty, save to .xlsx file in data folder
if df is not None:
    df.to_excel(f"data/{ticker}.xlsx")
    print(f"Data for {ticker} saved to data/{ticker}.xlsx")



