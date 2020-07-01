# Import necessary libraries
import pandas_datareader.data as pdr
import numpy as np
import datetime
from References.ATR_BollingerBand import atr

# Download historical data for required stocks
ticker = "AAPL"
ohlcv = pdr.get_data_yahoo(ticker, datetime.date.today()-datetime.timedelta(364), datetime.date.today())


# def atr(dataframe, n):
#     """function to calculate True Range and Average True Range"""
#     df = dataframe.copy()
#     df['H-L'] = abs(df['High']-df['Low'])
#     df['H-PC'] = abs(df['High']-df['Adj Close'].shift(1))
#     df['L-PC'] = abs(df['Low']-df['Adj Close'].shift(1))
#     df['TR'] = df[['H-L', 'H-PC', 'L-PC']].max(axis=1, skipna=False)
#     df['ATR'] = df['TR'].rolling(n).mean()
#     # df['ATR'] = df['TR'].ewm(span=n,adjust=False,min_periods=n).mean()
#     df2 = df.drop(['H-L', 'H-PC', 'L-PC'], axis=1)
#     return df2

def adx(df, n):
    """function to calculate ADX"""
    df2 = df.copy()                 # the period parameter of ATR function does
    df2['TR'] = atr(df2, n)['TR']   # not matter because period does not influence TR calculation
    df2['DMplus'] = np.where((df2['High']-df2['High'].shift(1)) > (df2['Low'].shift(1)-df2['Low']),
                             df2['High']-df2['High'].shift(1), 0)
    df2['DMplus'] = np.where(df2['DMplus'] < 0, 0, df2['DMplus'])
    df2['DMminus'] = np.where((df2['Low'].shift(1)-df2['Low']) > (df2['High']-df2['High'].shift(1)),
                              df2['Low'].shift(1)-df2['Low'], 0)
    df2['DMminus'] = np.where(df2['DMminus'] < 0, 0, df2['DMminus'])
    TRn = []
    DMplusN = []
    DMminusN = []
    TR = df2['TR'].tolist()
    DMplus = df2['DMplus'].tolist()
    DMminus = df2['DMminus'].tolist()
    for i in range(len(df2)):
        if i < n:
            TRn.append(np.NaN)
            DMplusN.append(np.NaN)
            DMminusN.append(np.NaN)
        elif i == n:
            TRn.append(df2['TR'].rolling(n).sum().tolist()[n])
            DMplusN.append(df2['DMplus'].rolling(n).sum().tolist()[n])
            DMminusN.append(df2['DMminus'].rolling(n).sum().tolist()[n])
        elif i > n:
            TRn.append(TRn[i-1] - (TRn[i-1]/14) + TR[i])
            DMplusN.append(DMplusN[i-1] - (DMplusN[i-1]/14) + DMplus[i])
            DMminusN.append(DMminusN[i-1] - (DMminusN[i-1]/14) + DMminus[i])
    df2['TRn'] = np.array(TRn)
    df2['DMplusN'] = np.array(DMplusN)
    df2['DMminusN'] = np.array(DMminusN)
    df2['DIplusN'] = 100*(df2['DMplusN']/df2['TRn'])
    df2['DIminusN'] = 100*(df2['DMminusN']/df2['TRn'])
    df2['DIdiff'] = abs(df2['DIplusN']-df2['DIminusN'])
    df2['DIsum'] = df2['DIplusN']+df2['DIminusN']
    df2['DX'] = 100*(df2['DIdiff']/df2['DIsum'])
    ADX = []
    DX = df2['DX'].tolist()
    for j in range(len(df2)):
        if j < 2*n-1:
            ADX.append(np.NaN)
        elif j == 2*n-1:
            ADX.append(df2['DX'][j-n+1:j+1].mean())
        elif j > 2*n-1:
            ADX.append(((n-1)*ADX[j-1] + DX[j])/n)
    df2['ADX'] = np.array(ADX)
    return df2['ADX']


