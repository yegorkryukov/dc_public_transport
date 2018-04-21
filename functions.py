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

def linear_regression_plot(df,y):
    
    '''Function returns linear regression plots for 2 and 3 columns dataframes.
        All Date objects should be in a datetime pd format (datetime64[ns]) (pd.to_datetime(df[date_column])).
        -------------------
        Attributes:
        df: a dataframe with at least 2 columns.
        y: an index of the dependent variable column (integer).
        -------------------
        Returns plots:
        1. for df with 2 columns: 2-dimensional scatter plot with fitted line.
        2. for df with 3 columns: 2-d plane in 3-d space, with data points above the hyperplane
        in white and points below the hyperplane in black. The color of the plane is determined
        by the corresonding predicted values (pink = high, blue = low).
        Datetime objects are converted into Months in all correlation graphs. '''
    
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    import statsmodels.api as sm
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.ticker as ticker
    
    df = df.copy()
    df = df.dropna(axis=0, how='any')
    
    for column in df.columns:
        if df[column].dtype == 'datetime64[ns]':
            df['delta'] = (df[column] - df[column].min()).astype('timedelta64[M]')
            df[column] = df['delta']
            df = df.drop(['delta'], axis=1)
            
    dependent_name = df.columns[y]
    features = [column for column in df]
    independent = [feature for feature in features if feature != dependent_name]
    
    if len(df.columns) == 2:
        fig = plt.figure(figsize=(8, 5))
        ax = sns.regplot(x=independent[0], y=dependent_name, data=df, color='g')
        scale_y = 1e6
        ticks_y = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x/scale_y))
        ax.yaxis.set_major_formatter(ticks_y)
        plt.title(f'Correlation between {dependent_name} and {independent[0]}')
        
        return fig
        
    elif len(df.columns) ==3:
        y = df[dependent_name]
        X = df[independent]
        X = sm.add_constant(X)
        model = sm.OLS(y, X).fit()
        
        x1, x2 = np.meshgrid(np.linspace(X.iloc[:,1].min(), X.iloc[:,1].max(), 100), 
                       np.linspace(X.iloc[:,2].min(), X.iloc[:,2].max(), 100))
        Z = model.params[0] + model.params[1] * x1 + model.params[2] * x2
        
        fig = plt.figure(figsize=(8, 5))
        ax = Axes3D(fig, azim=-115, elev=15)
        surf = ax.plot_surface(x1, x2, Z, cmap=plt.cm.cool, alpha=0.6, linewidth=0)
        resid = y - model.predict(X)

        ax.scatter(X[resid >= 0].iloc[:,1], X[resid >= 0].iloc[:,2], y[resid >= 0], color='black', alpha=1.0, facecolor='white')
        ax.scatter(X[resid < 0].iloc[:,1], X[resid < 0].iloc[:,2], y[resid < 0], color='black', alpha=1.0)
        ax.set_xlabel(independent[0])
        ax.set_ylabel(independent[1])
        ax.set_zlabel(dependent_name)
        
        return fig
        
    else:
        print('DF contains more than 2 predictor variables, regression can\'t be visualizes at this time')

        return model.summary()

def getPoly(X, Y, degree):
    '''
    Calculates least squares polynomial fit of 'degree' of the fitting polynomial
    
    Parameters
    ----------
    X : `pd.datetime` array-like
    Y :  array-like of X size
    
    Returns
    -------
    p : `numpy.lib.polynomial.poly1d` object
    '''
    import numpy as np
    import warnings
    warnings.simplefilter('ignore', np.RankWarning)
    import matplotlib.dates as mdates
    
    #convert dates to num values for poly function
    if X.dtype == 'datetime64[ns]':
        X_num = mdates.date2num(X)
    else:
        X_num = X
    
    #calculate Polynomial coefficients, highest power first
    #ndarray, shape (deg + 1,) or (deg + 1, K)
    coefs = np.polyfit(X_num, Y, int(degree))

    #Construct the polynomial
    p = np.poly1d(coefs)
    
    return p

def plotPoly(X, Y, p, show=True,x_label=None,y_label='',title='',Mtick=True,lw=2):
    '''
    Creates a Polynomial plot
    
    Parameters
    ----------
    X : `pd.datetime` array-like
    Y :  array-like of X size
    p : `numpy.lib.polynomial.poly1d` object
    show : boolean, display figure at the end of function if True
    xy_label,title : text for labels and plot title
    Mtick : Million tick, if True shows Y ticks in millions (value/1e6)
    
    Returns
    -------
    f : `matplotlib.figure.Figure`
    '''
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    import matplotlib.ticker as ticker

    #buld the plot
    plt.style.use('seaborn-whitegrid')
    f, ax = plt.subplots(figsize=(10,5))
    #plt.style.use('fivethirtyeight')
    #f = plt.figure(figsize=(20,10))
    
    #set y axis scale to million
    if Mtick:
        scale_y = 1e6
        ticks_y = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x/scale_y))
        ax.yaxis.set_major_formatter(ticks_y)
        y_label = y_label + ' , Million'
    
    #convert dates to num values for poly function
    if X.dtype == 'datetime64[ns]':
        X_num = mdates.date2num(X)
    else:
        X_num = X
    
    plt.plot(X, Y, label='Actual',lw=lw, marker='o')
    plt.plot(X, p(X_num), "r-", label='Model') #p(X) evaluates the polynomial at X
    
    #ax.set_ylim(0,30*1e6)
    ax.set_xlim(min(X_num),max(X_num))
    
    plt.title(title+' Polynomial Regression', weight='bold')
    plt.ylabel(y_label, weight='bold')
    plt.xlabel(x_label, weight='bold')
    plt.legend()
    
    if show:
        plt.show()
    else:
        plt.close(f)
    return f

def calcPoly(df,X='Date',degree=3,Mtick=False,lw=2):
    '''
    Returns a DF with calculated polynomial coeffs
    
    Parameters
    ----------
    df : Pandas DataFrame, must have first `Date` column of datetime dtype, 
         other columns should be of `numeric` dtype
    degree : calculate up to degree of power
    Mtick : Million tick, if True shows Y ticks in millions (value/1e6)
    
    Results
    -------
    Dataframe
    Saved PNGs
    '''    
    #set column names for the plot excluding 'Date' column [1:]
    columns = df.columns.tolist()[1:]
    
    result_df = pd.DataFrame()
    
    for degree in range(2,degree+1):
        for data in columns:
            temp = df[[X,data]]
            temp = temp.dropna(how='any')

            #print(f'Getting poly for {data}, {degree}')
            p = getPoly(temp[X], temp[data], degree)

            #add coeffs to df
            result_df = pd.concat([result_df,pd.DataFrame(
                {data+'_x_'+str(degree):p.coef[::-1]})],axis=1) 
            #reverse order of poly so column of DF represent power of X

            f = plotPoly(temp[X].values, temp[data],p,show=False,x_label='Timeline',y_label=data,
                     title=data+', x'+str(degree),Mtick=Mtick,lw=lw)
            path_to_plot = 'results/plots/'+data+'_polynomial_x'+str(degree)+'.png'
            f.savefig(path_to_plot,dpi=150,transparent=True,bbox_inches='tight') 
    
    return result_df.T

def calcPolyY(df,Y,degree=3,Mtick=False,lw=2):
    '''
    Returns a DF with calculated polynomial coeffs for dependant Variable Y
    
    Parameters
    ----------
    df : Pandas DataFrame, must have first `Date` column of datetime dtype, 
         other columns should be of `numeric` dtype
    Y : dependant variable
    degree : calculate up to degree of power
    Mtick : Million tick, if True shows Y ticks in millions (value/1e6)
    
    Results
    -------
    Dataframe
    Saved PNGs
    '''    
    #set column names for the plot excluding Y column 
    columns = df.drop(columns=Y).columns.tolist()
    
    result_df = pd.DataFrame()
    
    for degree in range(2,degree+1):
        for X in columns:
            temp = df[[X,Y]]
            temp = temp.dropna(how='any')

            #print(f'Getting poly for {data}, {degree}')
            p = getPoly(temp[X], temp[Y], degree)

            #add coeffs to df
            result_df = pd.concat([result_df,pd.DataFrame(
                {X+'_'+Y+'_x_'+str(degree):p.coef[::-1]})],axis=1) 
            #reverse order of poly so column of DF represent power of X

            f = plotPoly(temp[X].values, temp[Y],p,show=False,x_label=X,y_label=Y,
                     title=X+'/'+Y+', x'+str(degree),Mtick=Mtick,lw=lw)
            path_to_plot = 'results/plots/'+X+'_'+Y+'_polynomial_x'+str(degree)+'.png'
            f.savefig(path_to_plot,dpi=150,transparent=True,bbox_inches='tight') 
    
    return result_df.T