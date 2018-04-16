
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from Marc_Project_3_Module import TCSI
from Marc_Project_3_Module import seasonal_index_rank
month_lst=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']


# In[2]:


########################################################################################################


# In[3]:


metro_df = pd.read_csv('data_acquisition/combined/metro.csv')


# In[4]:


metro_df['Date'] = pd.to_datetime(metro_df['Date'])


# In[5]:


#Get arguements for the function call
year_start = metro_df.at[0,'Date'].year
time_interval_lst = metro_df['Date'].tolist()
series_lst =metro_df['Ridership'].tolist()

#Call the function for TCSI
TCSI_result,result_df = TCSI(time_interval_lst,series_lst,year_start)

TCSI_result.plot()
plt.show()


# In[6]:


seasonal_index_rank(result_df)


# In[ ]:


####################################################################################################

