import numpy_financial as npf
import argparse

parser = argparse.ArgumentParser(description='Accepts a list of cash flows and a discount rate and returns the net present value.')
parser.add_argument('-c','--cashflows', nargs='+', help='<Required> Set flag', required=True)
parser.add_argument('-r', '--rate', type=float, help='The custom ticker to compare.', required=True)
args = parser.parse_args()

try:
    # Convert the input list from a str list to an int list. Would throw errors here from bad user input.
    cashflows = list(map(float, args.cashflows))
except:
    print("Error: Bad user input. Expected list of only numbers in --cashflows argument.")
else:
    npv = npf.npv(args.rate, cashflows);
    print("{:.3f}".format(npv))
