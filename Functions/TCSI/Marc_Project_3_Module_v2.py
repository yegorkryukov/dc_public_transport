def TCSI(df):
    """This function analyzes time series data and returns Returns statsmodels.tsa.seasonal.DecomposeResult in the form of a
    dictionary and a dataframe with Trend (T), Seasonal Index(S), and Noise (CI) in a dataframe.   
    
    Attributes
    ----------
    DataFrame consists of 2 columns, where the first one is Date in pd_datetime format. No need to drop NaNs."""
    
    #Import the followning libraries
    from statsmodels.tsa.seasonal import seasonal_decompose
    import pandas as pd
    
    df1 = df.dropna(how='any').reset_index().drop(['index'],axis=1)
    obs = df1.iloc[:,1].tolist()
    
    result = seasonal_decompose(obs, model='multiplicative', freq=12)
    result_dic = vars(result)
    
    result_df = pd.DataFrame.from_dict(result_dic)
    result_df=result_df.drop(['nobs'],axis=1)
    result_df['Date'] = df1.iloc[:,0]
    result_df['Year'] = pd.DatetimeIndex(result_df['Date']).year 
    result_df['Month'] = pd.DatetimeIndex(result_df['Date']).month
    
    return result, result_df
    