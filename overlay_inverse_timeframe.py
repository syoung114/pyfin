import argparse

import pandas as pd
import yfinance as yf
import matplotlib.ticker as mtick
import datetime
from matplotlib import pyplot as plt

parser = argparse.ArgumentParser(description='Compares a ticker to the inverse of the S&P500. Useful for finding negative correlations.')
parser.add_argument('ticker', type=str, help='The custom ticker to compare.')
parser.add_argument('start_t_base', type=str, help='How far back to compare.')
parser.add_argument('end_t_base', type=str, help='How far back to compare.')
parser.add_argument('start_t_to', type=str, help='How far back to compare.')
args = parser.parse_args()

def invert(df):
    max = float('-inf')
    for index, row in df.iterrows():
        if row.iloc[0] > max:
            max = row.iloc[0]
    for index, row in df.iterrows():
        row.iloc[0] = max - row.iloc[0];
    return df


def closing_price(ticker, start_datetime, end_datetime):
    data = yf.download(ticker, start=start_datetime, end=end_datetime)['Adj Close']
    # This converts the data into a percentage so two price scales can be compared on a chart.
    asset = pd.DataFrame(data).apply(lambda x: x.div(x.iloc[0]).subtract(1).mul(100))

    return asset

def main():

    date_format = "%d%m%Y"

    start_t_base = args.start_t_base.replace('-', '')
    start_dt_base = datetime.datetime.strptime(start_t_base, date_format).date()

    end_t_base = args.end_t_base.replace('-', '')
    end_dt_base = datetime.datetime.strptime(end_t_base, date_format).date()

    start_t_to = args.start_t_to.replace('-', '')
    start_dt_to = datetime.datetime.strptime(start_t_to, date_format).date()

    end_dt_delta = end_dt_base - start_dt_base
    end_dt_to = datetime.combine(start_dt_to + end_dt_delta)
    
    base = closing_price(args.ticker, start_dt_base, end_dt_base)
    to = closing_price(args.ticker, start_dt_to, end_dt_to)

    # arg_t_inv = invert(arg_t.copy())

    # plt.plot(sp500.index, sp500.values, label='S&P500')
    plt.plot(base.index, base.values, label=args.ticker)
    # plt.plot(to.index, to.values, label=args.ticker)
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

now = dt.datetime.now()
delta = dt.timedelta(hours = 12)
t = now.time()
print(t)
# 12:39:11.039864

print(
    (datetime.combine(datetime.date(1,1,1), t) + delta).time()
)
# 00:39:11.039864
