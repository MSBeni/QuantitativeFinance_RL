# Import necesary libraries
import pandas_datareader.data as pdr
import numpy as np
import datetime
import statsmodels.api as sm


# Download historical data for required stocks
ticker = "AAPL"
ohlcv = pdr.get_data_yahoo(ticker, datetime.date.today()-datetime.timedelta(364), datetime.date.today())


def slope(ser, n):
    """function to calculate the slope of n consecutive points on a plot"""
    slopes = [i*0 for i in range(n-1)]
    for i in range(n, len(ser)+1):
        y = ser[i-n:i]
        x = np.array(range(n))
        y_scaled = (y - y.min())/(y.max() - y.min())
        x_scaled = (x - x.min())/(x.max() - x.min())
        x_scaled = sm.add_constant(x_scaled)
        model = sm.OLS(y_scaled, x_scaled)
        results = model.fit()
        # print(results.summary())
        slopes.append(results.params[-1])
    slope_angle = (np.rad2deg(np.arctan(np.array(slopes))))
    return np.array(slope_angle)


