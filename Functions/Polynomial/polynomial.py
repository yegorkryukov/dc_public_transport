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
    X_num = mdates.date2num(X)
    
    #calculate Polynomial coefficients, highest power first
    #ndarray, shape (deg + 1,) or (deg + 1, K)
    coefs = np.polyfit(X_num, Y, degree)

    #Construct the polynomial
    p = np.poly1d(coefs)
    
    return p

def plotPoly(X, Y, p, show=True):
    '''
    Creates a Polynomial plot
    
    Parameters
    ----------
    X : `pd.datetime` array-like
    Y :  array-like of X size
    p : `numpy.lib.polynomial.poly1d` object
    
    Returns
    -------
    f : `matplotlib.figure.Figure`
    '''
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    
    #buld the plot
    #####new temp add
    plt.style.use('seaborn-whitegrid')
    f, ax = plt.subplots(figsize=(5,5))
    
    #plt.style.use('fivethirtyeight')
    #f = plt.figure(figsize=(20,10))
    
    #convert dates to num values for poly function
    X_num = mdates.date2num(X)
    
    plt.plot(X, Y, label='Actual Ridership')
    plt.plot(X, p(X_num), "r-", label='Regression Model') #p(X) evaluates the polynomial at X
    
    plt.title('Polynomial Regression', weight='bold')
    plt.ylabel('Ridership, trips')
    plt.xlabel('Time')
    plt.legend()
    
    if show:
        plt.show()
    else:
        plt.close(f)
    return f