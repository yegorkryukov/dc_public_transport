## WMATA Bus data collection

`resources` folder contains:
1. historical data for bus ridership for 2012-2017 years (files: `Ridership_Data_for_FY_2012.csv`–`...2017.csv`)
2. `combined.csv`: 2012-2017 bus ridership data by month for the following bus operators: 
1.1. ART Bus
1.2. DC Circulator
1.3. MTA
1.4. Metro Bus
3. `bus_positions.csv`: WMATA bus positions collected from WMATA API. File appends new record with each API call

`wmata-bus-data.ipynb`: Jupyter notebook with the code



```python
import requests
import config
import pandas as pd
import numpy as np
from pprint import pprint
import os
```


```python
def getBusPositions(api_key):
    headers = {'api_key':api_key}
    #request all buses positions
    r = requests.get('https://api.wmata.com/Bus.svc/json/jBusPositions', headers=headers)
    if r.status_code == 200:
        response = r.json()
        return response
    else:
        print(f'getBusPositions: Unable to get the data. Error code: {r.status_code}')
        return False

#collecting bus positions and saving them to the file
def collectBusPositions():

    results = getBusPositions(config.api_key)

    if results:
        bus_positions = pd.DataFrame(results['BusPositions'])
        
        #convert date columns to datetime type
        bus_positions.loc[:, ['DateTime','TripEndTime','TripStartTime']] = \
            bus_positions.loc[:, ['DateTime','TripEndTime','TripStartTime']].apply(pd.to_datetime, errors='coerce')

        # if file does not exist write header 
        path = 'resources/bus_positions.csv'
        if not os.path.isfile(path):
            bus_positions.to_csv(path,index=False, )
        else: # else it exists so append without writing the header
            bus_positions.to_csv(path,mode = 'a',header=False,index=False)

if __name__ == '__main__':
    collectBusPositions()
    
print('Finished')
```

    Finished



```python
#data from July through June 

def readData():
    #cicle through year's CSV
    result = pd.DataFrame(columns=['Ridership'])
    for year in range(2013,2018):
        #read csv
        path = 'resources/Ridership_Data_for_FY_' + str(year) + '.csv'
        df = pd.read_csv(path)

        #leave the ridership columns only
        df = df[['Operator','July','August','September', \
                 'October','November','December', \
                 'January','February','March',\
                 'April','May','June']]

        #choose the bus lines to keep
        operators = (df['Operator']=='ART Bus')|(df['Operator']=='DC Circulator')|(df['Operator']=='MTA')|(df['Operator'] == 'Metro Bus') 
        df = df.loc[operators]

        #rename columns
        columns = ['Operator'] + \
                  [x + str(year) for x in df.columns.tolist()[1:7]] + \
                  [x + str(year+1) for x in df.columns.tolist()[7:]]
        df.columns = columns
        df = df.set_index('Operator')

        #setup datetime format
        rdT = df.transpose()
        rdT['date'] = rdT.index
        rdT = pd.melt(rdT, id_vars=['date'])
        rdT = rdT.groupby('date').agg({'value':sum})
        rdT.index = pd.to_datetime(rdT.index).strftime('%Y%m')
        rdT.columns = ['Ridership']
        result = result.append(rdT)
    return result

#collect and combine all the data
combined = readData().sort_index()
combined.index.name = 'Date'
combined.head()
#save to CSV
combined.to_csv('resources/combined.csv')
```

        