import yfinance as yf
import numpy_financial as npf
import argparse

parser = argparse.ArgumentParser(description='Calculates the net present value of a stock, given its ticker, and a discount rate.')
parser.add_argument('ticker', type=str, help='The custom ticker to compare.')
parser.add_argument('rate', type=float, help='The custom ticker to compare.')
# parser.add_argument('timeframe', type=str, help='The custom ticker to compare.',)
args = parser.parse_args()

t = yf.Ticker(args.ticker)
cfs = t.cashflow

free_cash_flows = []
for period, values in cfs.iteritems():
    op_total = values['Total Cash From Operating Activities']
    capex = values['Capital Expenditures']

    fcf = op_total + capex
    free_cash_flows = [fcf] + free_cash_flows

npv = npf.npv(args.rate, free_cash_flows);
print("{:.3f}".format(npv))