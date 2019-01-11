import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("911.csv")
df.info()
print(df.head())


print('Top 5 zipcodes: ' + str(df['zip'].value_counts().head(5)))
print('Top 5 township: ' + str(df['twp'].value_counts().head(5)))
print('Titles: ' + str(df['title'].nunique()))

df['Reason'] = df['title'].apply(lambda title: title.split(':')[0])
print('Reasons for calls: ' + str(df['Reason'].value_counts()))

#Countplot for Reason
sns.countplot(x='Reason',data=df)
plt.show()

#type(df['timeStamp'].iloc[0])
df['timeStamp'] = pd.to_datetime(df['timeStamp'])

df['Hour'] = df['timeStamp'].apply(lambda time: time.hour)
df['Month'] = df['timeStamp'].apply(lambda time: time.month)
df['Day of Week'] = df['timeStamp'].apply(lambda time: time.dayofweek)

dmap = {0:'Mon',1:'Tue',2:'Wed',3:'Thu',4:'Fri',5:'Sat',6:'Sun'}
df['Day of Week'] = df['Day of Week'].map(dmap)
print(df['Day of Week'])
#print(df.head())

#Countplot for calls for day of week
sns.countplot(x='Day of Week', data=df, hue='Reason', palette='viridis')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.show()

#Countplot for calls for month
sns.countplot(x='Month', data=df, hue='Reason', palette='viridis')
plt.legend(bbox_to_anchor=(1.05,1), loc=2, borderaxespad=0.)
plt.show()

byMonth = df.groupby('Month').count()
print(byMonth.head())

byMonth['twp'].plot()
plt.show()

sns.lmplot(x='Month', y='twp', data=byMonth.reset_index())
plt.show()

df['Date'] = df['timeStamp'].apply(lambda t: t.date())

#Number of calls for date
df.groupby('Date').count()['twp'].plot()
plt.tight_layout()
plt.show()

#Number of calls for traffic
df[df['Reason'] == 'Traffic'].groupby('Date').count()['twp'].plot()
plt.title('Traffic')
plt.show()

#Number of calls for fire
df[df['Reason'] == 'Fire'].groupby('Date').count()['twp'].plot()
plt.title('Fire')
plt.show()

#Number of calls for ems
df[df['Reason'] == 'EMS'].groupby('Date').count()['twp'].plot()
plt.title('EMS')
plt.show()

print(df.groupby(by=['Day of Week', 'Hour']).count())
dayHour = df.groupby(by=['Day of Week', 'Hour']).count()['Reason'].unstack()
print(dayHour)

#Heatmap- calls(hours/day of week)
plt.figure(figsize=(12, 6))
sns.heatmap(dayHour)
plt.show()

sns.clustermap(dayHour, cmap='viridis')
plt.show()

print(df.groupby(by=['Day of Week', 'Month']).count())
dayMonth = df.groupby(by=['Day of Week', 'Month']).count()['Reason'].unstack()
print(dayMonth)

#Heatmap- calls(month/day of week)
plt.figure(figsize=(12,6))
sns.heatmap(dayMonth)
plt.show()

sns.clustermap(dayMonth, cmap='viridis')
plt.show()