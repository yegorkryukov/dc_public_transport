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
        plt.title(f'Correlation between {dependent_name} and {independent[0]}')
        
        #return fig
        
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
        
        #return fig
        
    else:
        print('DF contains more than 2 predictor variables, regression can\'t be visualizes at this time')

        return model.summary()