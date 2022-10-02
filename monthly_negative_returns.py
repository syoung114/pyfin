import argparse
import yfinance as yf
# from pandas_datareader.data import DataReader

parser = argparse.ArgumentParser(description='Counts the months that a security had negative returns. This is different from averaging the return of all months regardless of their performance.')
parser.add_argument('ticker', type=str, help='The custom ticker to compare.')
args = parser.parse_args()

def monthly_pct(ticker):
    first_iteration = True

    previous_month_close = None
    current_month_close = None

    month_count = [0] * 12

    for index, row in ticker.iterrows():
        
        current_month_close = row['Close']

        if first_iteration:
            previous_month_close = current_month_close
            first_iteration = False
            continue
        
        pct_change = (current_month_close / previous_month_close - 1)# * 100

        if (pct_change < 0):
            month_count[index.month - 1] += 1
        
        # print(f"{row['Date']} {row['Close']}")
        # print(f"{pct_change}")

        previous_month_close = current_month_close

    return month_count

def get_sorted_index(a):
    '''Returns an array of indices noting where to move the array values so that the array is sorted.'''
    return sorted(range(len(a)), key=lambda k: a[k])

def sort_by_index(a, a_indices):
    '''Sorts an array by indices contained in another array.'''
    original_a = a.copy()
    for i, a_index in enumerate(a_indices):
        a[-(i+1)] = original_a[a_index]
    return a

def main():

    months = {
        'jan' : 0,
        'feb' : 0,
        'mar' : 0,
        'apr' : 0,
        'may' : 0,
        'jun' : 0,
        'jul' : 0,
        'aug' : 0,
        'sep' : 0,
        'oct' : 0,
        'nov' : 0,
        'dec' : 0
    }
    
    t = yf.download(args.ticker, interval='1mo')
    # t = yf.download('^GSPC', interval='1mo')
    print(t)
    returns = monthly_pct(t)

    returns_sorted_id = get_sorted_index(returns)
    months_by_index = sort_by_index(list(months.keys()), returns_sorted_id)
    returns_by_index = sort_by_index(returns.copy(), returns_sorted_id)


    # months.update(zip(months, returns))
    # months.update(zip(months_by_index, returns_by_index))

    sorted_months = dict(zip(months_by_index, returns_by_index))

    print(t['name'])
    print(sorted_months)
    print(f'Total periods = {len(t)}')
    print(f'Total negative periods = {sum(returns)}')

if __name__ == '__main__':
    main()