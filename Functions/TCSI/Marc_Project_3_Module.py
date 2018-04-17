
# coding: utf-8

# In[ ]:


def TCSI(time_span, observations,year_start):
    """This function analyzes time series data and returns Returns statsmodels.tsa.seasonal.DecomposeResult in the form of a
    dictionary and a dataframe with Trend (T), Seasonal Index(S), and Noise (CI) in a dataframe.   
    
    Attributes
    ----------
    time_span : list
        The list of times over the interval that was used to collect the observations 
    
    observations: list
        The list of observations that were collect for each increment of the time interval
        
    year_start : int
        The year the time series starts
                                                                                                         """
    
    'Import the followning libraries'
    from statsmodels.tsa.seasonal import seasonal_decompose
    import pandas as pd

    
    result = seasonal_decompose(observations, model='multiplicative', freq=12)
    
    ###########################################################################
    result_dic=vars(result)
    result_df=pd.DataFrame.from_dict(result_dic)

    result_df=result_df.drop(['nobs'],axis=1)
    result_df['Year']=''
    result_df['Month'] =''
    length_of_interval = len(observations)
    result_df['Date'] = pd.date_range(start='2011',freq='M',periods=length_of_interval)

    month_lst=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    year=year_start
    month_count = 0
    for ind, row in result_df.iterrows():
        result_df.at[ind, 'Month'] = month_lst[month_count]
        result_df.at[ind, 'Year'] = year
        month_count +=1
        if month_count == 12:
            month_count = 0
            year=year+1
    return result, result_df

###################################################################################################################

def seasonal_index_rank(TCSI_df):
    
    """This function analyzes seasonal index series data and prints the month and index in a descending order.
    
    Attributes
    ----------
    TCSI : dataframe
        The dataframe containing trend, seasonal, and random data
        """
    
    month_lst=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    seasonal_df=TCSI_df.loc[:,['seasonal','Year','Month','Date']]
    seasonal_df_monthly=seasonal_df[seasonal_df.Year==seasonal_df.at[0,'Date'].year]
    
    #Find month with highest ridership
    monthly_series=seasonal_df_monthly['seasonal']
    rank_series= monthly_series.nlargest(n=12, keep='first')
    for j in range(rank_series.size):
        print (month_lst[rank_series.index[j]]+ '--> '+ str(monthly_series[rank_series.index[j]]))

