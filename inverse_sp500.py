import argparse

import pandas as pd
import yfinance as yf
import matplotlib.ticker as mtick
from datetime import date, timedelta
from matplotlib import pyplot as plt

parser = argparse.ArgumentParser(description='Compares a ticker to the inverse of the S&P500. Useful for finding negative correlations.')
parser.add_argument('ticker', type=str, help='The custom ticker to compare.')
parser.add_argument('years', type=int, help='How far back to compare.')
args = parser.parse_args()

def invert(df):
    max = float('-inf')
    for index, row in df.iterrows():
        if row.iloc[0] > max:
            max = row.iloc[0]
    for index, row in df.iterrows():
        row.iloc[0] = max - row.iloc[0];
    return df


def closing_price(ticker):

    start_t = date.today() - timedelta(365*args.years)
    start_t.strftime('%Y-%m-%d')

    end_t = date.today() - timedelta(0)
    end_t.strftime('%Y-%m-%d')

    data = yf.download(ticker, start=start_t, end=end_t)['Adj Close']
    asset = pd.DataFrame(data).apply(lambda x: x.div(x.iloc[0]).subtract(1).mul(100))

    return asset

def main():

    sp500 = closing_price('SPY')
    sp500_inv = invert(sp500.copy())
    arg_t = closing_price(args.ticker)
    # arg_t_inv = invert(arg_t.copy())

    plt.plot(sp500.index, sp500.values, label='S&P500')
    plt.plot(sp500.index, sp500_inv.values, label='S&P500 inverse')
    plt.plot(sp500.index, arg_t.values, label=args.ticker)
    # plt.plot(sp500.index, arg_t_inv.values, label=f'{args.ticker} inverse'})

    # actualName = yf.Ticker(args.ticker).info['longName']

    # plt.yscale('log')
    plt.xlabel("Time")
    plt.ylabel("% Change")
    plt.title(f"Inverse S&P500 vs {args.ticker}")
    # plt.title(f"Inverse S&P500 vs {actualName}")
    plt.legend()
    plt.show()
    
main()