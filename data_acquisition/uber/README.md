## Get the data as Pandas DF with time as index to highest granularity

### Collect the data of Uber trips, aggregated by month 2016 -2018 years


```python
import pandas as pd
import glob
from matplotlib import pyplot as plt
import seaborn as sns
```


```python
# Write a path to the files and an empty df
path = glob.glob('raw_data/monthly/*/*.csv')
df = pd.DataFrame()
```


```python
# Create merged df
x = 0
for filepath in path:
    name = filepath.split('/')
    readfile = pd.read_csv(filepath)
    df_x = pd.DataFrame(readfile)
    df_x['year'] = int(name[2])
    
    df = df.append(df_x, ignore_index=True)
    x += 1
```


```python
df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>sourceid</th>
      <th>dstid</th>
      <th>month</th>
      <th>mean_travel_time</th>
      <th>standard_deviation_travel_time</th>
      <th>geometric_mean_travel_time</th>
      <th>geometric_standard_deviation_travel_time</th>
      <th>year</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>210</td>
      <td>415</td>
      <td>10</td>
      <td>1857.75</td>
      <td>818.52</td>
      <td>1756.84</td>
      <td>1.35</td>
      <td>2017</td>
    </tr>
    <tr>
      <th>1</th>
      <td>351</td>
      <td>16</td>
      <td>10</td>
      <td>1130.30</td>
      <td>436.73</td>
      <td>1072.17</td>
      <td>1.35</td>
      <td>2017</td>
    </tr>
    <tr>
      <th>2</th>
      <td>248</td>
      <td>237</td>
      <td>12</td>
      <td>861.58</td>
      <td>331.51</td>
      <td>810.05</td>
      <td>1.40</td>
      <td>2017</td>
    </tr>
    <tr>
      <th>3</th>
      <td>353</td>
      <td>375</td>
      <td>12</td>
      <td>1081.61</td>
      <td>492.97</td>
      <td>1008.97</td>
      <td>1.43</td>
      <td>2017</td>
    </tr>
    <tr>
      <th>4</th>
      <td>257</td>
      <td>175</td>
      <td>11</td>
      <td>1979.68</td>
      <td>582.71</td>
      <td>1899.99</td>
      <td>1.33</td>
      <td>2017</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Change date format, count a number of rides
df1 = df[['month', 'year', 'dstid']].groupby(['year', 'month']).count().reset_index()
months = {1:('01',31), 2:('02',28), 3:('03',31), 4:('04',30), 5:('05',31), 6:('06',30),
          7:('07',31), 8:('08',31), 9:('09',30), 10:('10',31), 11:('11',30), 12:('12',31)}
for ind, row in df1.iterrows():
    df1.at[ind, 'mon'] = months[row['month']][0]
    df1.at[ind, 'date'] = ''
    df1.at[ind, 'uber_count'] = months[row['month']][1]
df1['date'] = df1['year'].astype(str) + df1['mon']
df1['uber_count'] = df1['dstid'] * df1['uber_count']
df1 = df1.drop(df1.columns[[0, 1, 2, 3]], axis=1)
```


```python
# Export to csv
df1.to_csv('uber_monthly.csv')
```


```python
df1.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>date</th>
      <th>uber_count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>201601</td>
      <td>4336528.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>201602</td>
      <td>4105444.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>201603</td>
      <td>4731468.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>201604</td>
      <td>4583160.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>201605</td>
      <td>4918088.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
sns.pointplot(x='month', y='mean_travel_time', hue='year',
            data=(df[['mean_travel_time', 'month', 'year']].groupby(['month', 'year']).count().reset_index()), ci=None, markers='.')
plt.grid(True)
plt.ylabel('Average number of rides')
```




    Text(0,0.5,'Average number of rides')




![png](output_7_1.png)

