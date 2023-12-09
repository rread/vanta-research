from datetime import datetime
import pandas as pd
import yfinance as yf

stock_symbol = "QQQ"
start_date = "2010-01-04"
end_date = "2023-11-05"  # datetime.now()

# import pandas as pd
# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_colwidth', None)
# pd.set_option('display.width', 2000)


def main():
    df = yf.download(stock_symbol, start=start_date, end=end_date)

    df['dayofweek'] = df.index.to_series().dt.dayofweek
    df['year'] = df.index.to_series().dt.isocalendar().year
    df['week'] = df.index.to_series().dt.isocalendar().week

    weeks = df.groupby(['year', 'week'])

    print(f"AChecking {stock_symbol} from {start_date} to {end_date}")

    print("Weekdays with highest close.")
    print_day_list(weekday_histogram(weeks, highest_close))

    print("\nWeekdays with lowest close.")
    print_day_list(weekday_histogram(weeks, lowest_close))

    print("\nWeekdays with highest high.")
    print_day_list(weekday_histogram(weeks, highest_high))

    print("\nWeekdays with lowest low")
    print_day_list(weekday_histogram(weeks, lowest_low))


def highest_close(week):
    return week[week.Close == week.Close.max()]

def lowest_close(week):
    return week[week.Close == week.Close.min()]

def highest_high(week):
    return week[week.High == week.High.max()]


def lowest_low(week):
    return week[week.Low == week.Low.min()]


def weekday_histogram(weeks, scan_fn):
    dayhist = new_day_list()
    for name, week in weeks:
        results = scan_fn(week)
        # sometimes there is a tie
        for day in results.dayofweek:
            dayhist[day] += 1
    return dayhist


day_names = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}

def new_day_list():
    hist = pd.Series(data=0, index=day_names.keys())
    return hist

def print_day_list(hist):
    s = pd.Series(data=hist.values, index=day_names.values())
    for name, count in s.items():
        print(f"{name}: {count}")


if __name__ == '__main__':
    main()
