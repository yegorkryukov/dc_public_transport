def linear_regression(df, y):
    
    '''Function for single and multivariable regression:
        All Date objects should be in a datetime pd format (datetime64[ns]) (pd.to_datetime(df[date_column])).
        -------------------
        Attributes:
        df: a dataframe with at least 2 columns.
        y: an index of the dependent variable column (integer).
        -------------------
        Returns a tuple: 
        1. R_squared
        2. p_value for each of the independent variable in the same order as they appear in the df.
        
        Datetime objects are converted into Days. '''
    
    import pandas as pd
    import numpy as np
    import statsmodels.api as sm
    
    # Drop all NaNs
    df = df.copy()
    df = df.dropna(axis=0, how='any')
    
    # Check if there is a datetime object and convert in days
    for column in df.columns:
        if df[column].dtype == 'datetime64[ns]':
            df['delta'] = (df[column] - df[column].min()).astype('timedelta64[D]')
            df[column] = df['delta']
            df = df.drop(['delta'], axis=1)
    
    # Define a dependent column name
    dependent_name = df.columns[y]
    
    # Define independent column(s) name(s)
    features = [column for column in df]
    independent = [feature for feature in features if feature != dependent_name]
    
    # Create a model
    y = df[dependent_name]
    X = df[independent]
    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit()
    
    # Extract coeff
    r2 = model.rsquared
    
    df1 = pd.Series(model.pvalues).reset_index().drop(['index'], axis=1)
    pval = df1[0].tolist()
    pval.pop(0)
    
    coeff = (r2, *pval)
    
    return coeff, model.summary()