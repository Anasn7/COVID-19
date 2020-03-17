import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from datetime import timedelta
import plotly.express as px
import plotly.io as pio
import os


# import data from github repo https://github.com/CSSEGISandData/COVID-19
url_Confirmed = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'
url_Death = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv'
url_Recovered = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv'
df_Confirmed = pd.read_csv(url_Confirmed,index_col=0,parse_dates=[0])
df_Death = pd.read_csv(url_Death,index_col=0,parse_dates=[0])
df_Recovered = pd.read_csv(url_Recovered,index_col=0,parse_dates=[0])

#function to plot h bar chart
def plt_bar (df, title, xlabel, ylabel, color ):
    fig = plt.figure(dpi=128, figsize=(14,6))
    plt.barh(df[xlabel], df[ylabel], color =color)
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.title(title)
    #plt.yscale('log',basey=10) 
    for i, v in enumerate(df[ylabel]):
        plt.text(v + 300, i + .10, str(v))
    plt.gca().invert_yaxis()
    # plt.legend(fontsize=10)
    plt.show()
    plt.savefig(last_date+"/"+title)


# data integration 

# calculate total by using the last column as total
df_Confirmed["Sum"] = df_Confirmed[df_Confirmed.columns[-1]]
df_Death["Sum"] = df_Death[df_Death.columns[-1]]
df_Recovered["Sum"] = df_Recovered[df_Recovered.columns[-1]]

# create a list of headers as the headers are changable in a daily basis
column_list = list(df_Confirmed)
removed_items=['Lat', 'Long']
for item in removed_items:
    column_list.remove(item)

# lets aggregate by country as the data provided by country states 

pivot_Confirmed = df_Confirmed.groupby(['Country/Region']).sum().reset_index()
pivot_Confirmed = pivot_Confirmed.drop(["Lat","Long"] ,axis=1)
pivot_Death = df_Death.groupby(['Country/Region']).sum().reset_index()
pivot_Death = pivot_Death.drop(["Lat","Long"] ,axis=1)
pivot_Recovered = df_Recovered.groupby(['Country/Region']).sum().reset_index()
pivot_Recovered = pivot_Recovered.drop(["Lat","Long"] ,axis=1)

# total per country
total_confirmed = pivot_Confirmed[['Country/Region','Sum']]
total_Death = pivot_Death[['Country/Region','Sum']]
total_Recovered = pivot_Recovered[['Country/Region','Sum']]



# let's also study the spread rate of all the world vs. china by dividing the dataframes into china and other countries

# Worldwide
df_Confirmed_ww = pivot_Confirmed
df_Confirmed_ww = df_Confirmed_ww.set_index('Country/Region').drop("China", axis=0).reset_index()
df_Confirmed_ww = df_Confirmed_ww.sum(axis=0).drop(["Country/Region","Sum"]).reset_index()
df_Confirmed_ww = df_Confirmed_ww.rename(columns={"index": "Date", 0: "Confirmed_Cases_WW"})
df_Confirmed_ww['Date'] = pd.to_datetime(df_Confirmed_ww['Date'])

df_Death_ww = pivot_Death
df_Death_ww = df_Death_ww.set_index('Country/Region').drop("China", axis=0).reset_index()
df_Death_ww = df_Death_ww.sum(axis=0).drop(["Country/Region","Sum"]).reset_index()
df_Death_ww = df_Death_ww.rename(columns={"index": "Date", 0: "Deaths_WW"})
df_Death_ww['Date'] = pd.to_datetime(df_Death_ww['Date'])

df_Recovered_ww = pivot_Recovered
df_Recovered_ww = df_Recovered_ww.set_index('Country/Region').drop("China", axis=0).reset_index()
df_Recovered_ww = df_Recovered_ww.sum(axis=0).drop(["Country/Region","Sum"]).reset_index()
df_Recovered_ww = df_Recovered_ww.rename(columns={"index": "Date", 0: "Recovered_Cases_WW"})
df_Recovered_ww['Date'] = pd.to_datetime(df_Recovered_ww['Date'])

# China
df_Confirmed_ch = pivot_Confirmed.set_index('Country/Region')
df_Confirmed_ch = df_Confirmed_ch.loc['China'].drop(["Sum"], axis=0).reset_index()
df_Confirmed_ch = df_Confirmed_ch.rename(columns={"index": "Date", "China": "Confirmed_Cases_CH"})
df_Confirmed_ch['Date'] = pd.to_datetime(df_Confirmed_ch['Date'])

df_Death_ch = pivot_Death.set_index('Country/Region')
df_Death_ch = df_Death_ch.loc['China'].drop(["Sum"], axis=0).reset_index()
df_Death_ch = df_Death_ch.rename(columns={"index": "Date", "China": "Deaths_CH"})
df_Death_ch['Date'] = pd.to_datetime(df_Death_ch['Date'])

df_Recovered_ch = pivot_Recovered.set_index('Country/Region')
df_Recovered_ch = df_Recovered_ch.loc['China'].drop(["Sum"], axis=0).reset_index()
df_Recovered_ch = df_Recovered_ch.rename(columns={"index": "Date", "China": "Recovered_Cases_CH"})
df_Recovered_ch['Date'] = pd.to_datetime(df_Recovered_ch['Date'])

# Visualize the results as timeline series 

# create folder for today's visualization 
last_date = str(df_Death_ch['Date'].iloc[-1].date().strftime("%b %d %Y"))
if not os.path.exists(last_date):
    os.mkdir(last_date)
#Visualize Confirmed cases China vs. worldwide
last_date = str(df_Death_ch['Date'].iloc[-1].date().strftime("%b %d %Y"))
fig = plt.figure(dpi=128, figsize=(10,5))
plt.plot(df_Confirmed_ch['Date'], df_Confirmed_ch['Confirmed_Cases_CH'], color='red', label='Confirmed Cases China')
plt.plot(df_Confirmed_ww['Date'], df_Confirmed_ww['Confirmed_Cases_WW'], color='blue', label='Confirmed Cases Worldwide')
plt.xlabel('Date')
plt.ylabel('Number of confirmed cases')
plt.title('Confirmed cases China vs. Worldwide as of ' + last_date)
plt.xticks(rotation=45)
ax=plt.gca()
ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
x1 = df_Confirmed_ch['Date'].iloc[-1]
y1 = df_Confirmed_ch['Confirmed_Cases_CH'].iloc[-1]
plt.annotate(y1,(x1,y1),(x1-timedelta(days=1),y1+500))
x2 = df_Confirmed_ww['Date'].iloc[-1]
y2 = df_Confirmed_ww['Confirmed_Cases_WW'].iloc[-1]
plt.annotate(y2,(x2,y2),(x2-timedelta(days=2),y2+500))
#ax.xaxis_date()
fig.autofmt_xdate()
plt.legend(fontsize=10)
plt.show()
plt.savefig(last_date+"/Confirmed_Cases_china_vs_ww.png")

#Visualize Death China vs. worldwide
last_date = str(df_Death_ch['Date'].iloc[-1].date().strftime("%b %d %Y"))
fig = plt.figure(dpi=128, figsize=(10,5))
plt.plot(df_Death_ch['Date'], df_Death_ch['Deaths_CH'], color='red', label='Deaths China')
plt.plot(df_Death_ww['Date'], df_Death_ww['Deaths_WW'], color='blue', label='Deaths Worldwide')
plt.xlabel('Date')
plt.ylabel('Number of Deaths')
plt.title('Deaths China vs. Worldwide as of ' + last_date )
plt.xticks(rotation=45)
ax=plt.gca()
ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
x1 = df_Death_ch['Date'].iloc[-1]
y1 = df_Death_ch['Deaths_CH'].iloc[-1]
plt.annotate(y1,(x1,y1),(x1-timedelta(days=0),y1+30))
x2 = df_Death_ww['Date'].iloc[-1]
y2 = df_Death_ww['Deaths_WW'].iloc[-1]
plt.annotate(y2,(x2,y2),(x2-timedelta(days=0),y2+30))
#ax.xaxis_date()
fig.autofmt_xdate()
plt.legend(fontsize=10)
plt.show()
plt.savefig(last_date+"/Deaths_china_vs_ww.png")

#Visualize Recovered Cases China vs. worldwide
last_date = str(df_Death_ch['Date'].iloc[-1].date().strftime("%b %d %Y"))
fig = plt.figure(dpi=128, figsize=(10,5))
plt.plot(df_Recovered_ch['Date'], df_Recovered_ch['Recovered_Cases_CH'], color='red', label='Recovered Cases China')
plt.plot(df_Recovered_ww['Date'], df_Recovered_ww['Recovered_Cases_WW'], color='blue', label='Recovered Cases Worldwide')
plt.xlabel('Date')
plt.ylabel('Number of Recovered Cases')
plt.title('Recovered cases China vs. Worldwide as of ' + last_date )
plt.xticks(rotation=45)
ax=plt.gca()
ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
x1 = df_Recovered_ch['Date'].iloc[-1]
y1 = df_Recovered_ch['Recovered_Cases_CH'].iloc[-1]
plt.annotate(y1,(x1,y1),(x1-timedelta(days=1),y1+600))
x2 = df_Recovered_ww['Date'].iloc[-1]
y2 = df_Recovered_ww['Recovered_Cases_WW'].iloc[-1]
plt.annotate(y2,(x2,y2),(x2-timedelta(days=1),y2+600))
#ax.xaxis_date()
fig.autofmt_xdate()
plt.legend(fontsize=10)
plt.show()
plt.savefig(last_date+"/Recovered_china_vs_ww.png")

# Visualize Percentage of Recovered,Death to total Cases in china and world wide

total_Cases_china = df_Confirmed_ch['Confirmed_Cases_CH'].iloc[-1]
total_Recovered_china = df_Recovered_ch['Recovered_Cases_CH'].iloc[-1]
total_Death_china = df_Death_ch['Deaths_CH'].iloc[-1]

percentage_Recovered = 100*total_Recovered_china/total_Cases_china
percentage_Death = 100*total_Death_china/total_Cases_china
percentage_Active_Cases = 100-percentage_Recovered-percentage_Death

labels = ['Recovered', 'Deaths', 'Active']
sizes = [percentage_Recovered, percentage_Death, percentage_Active_Cases]
colors = ['#50f27b', '#cccccc', '#f54c4c']
exploded = [0, 0.05, 0]
last_date = str(df_Death_ch['Date'].iloc[-1].date().strftime("%b %d %Y"))
fig = plt.figure(dpi=128, figsize=(10,5))
plt.title('COVID 19 in China as of ' + last_date, fontsize=16, horizontalalignment= 'center', pad=30 )
plt.legend(fontsize=10)
# Equal aspect ratio ensures that pie is drawn as a circle
plt.axis('equal')
my_pie,_,_ = plt.pie(sizes, labels=labels, explode = exploded, colors=colors, startangle=90, radius = 1.2, autopct="%1.1f%%", pctdistance=0.75)
plt.setp(my_pie, width=0.6, edgecolor='white')
plt.tight_layout()
plt.show()
plt.savefig(last_date+"/chinaPieChart.png")

# Worldwide percentage

total_Cases_ww = df_Confirmed_ww['Confirmed_Cases_WW'].iloc[-1]
total_Recovered_ww = df_Recovered_ww['Recovered_Cases_WW'].iloc[-1]
total_Death_ww = df_Death_ww['Deaths_WW'].iloc[-1]

percentage_Recovered = 100*total_Recovered_ww/total_Cases_ww
percentage_Death = 100*total_Death_ww/total_Cases_ww
percentage_Active_Cases = 100-percentage_Recovered-percentage_Death

labels = ['Recovered', 'Deaths', 'Active']
sizes = [percentage_Recovered, percentage_Death, percentage_Active_Cases]
colors = ['#50f27b', '#cccccc', '#f54c4c']
exploded = [0, 0.05, 0]
last_date = str(df_Death_ch['Date'].iloc[-1].date().strftime("%b %d %Y"))
fig = plt.figure(dpi=128, figsize=(10,5))
plt.title('COVID 19 in Worldwide excluding China as of ' + last_date, fontsize=14, horizontalalignment= 'center', pad=30 )
plt.legend(fontsize=10)
# Equal aspect ratio ensures that pie is drawn as a circle
plt.axis('equal')
my_pie,_,_ = plt.pie(sizes, labels=labels, explode = exploded, colors=colors, startangle=90, radius = 1.2, autopct="%1.1f%%", pctdistance=0.75, labeldistance=1.05)
plt.setp(my_pie, width=0.6, edgecolor='white')
plt.tight_layout()
plt.show()
plt.savefig(last_date+"/WW_PieChart.png")




# Displaying countries with more than 1000 confirmed cases

# top_ten_cases = total_confirmed.nlargest(10,'Sum').rename(columns={"Sum": "Confirmed cases"})
more_than_1000 = total_confirmed[total_confirmed.Sum > 1000].rename(columns={"Sum": "Confirmed cases"}).sort_values(by=['Confirmed cases'],ascending=False)
last_date = str(df_Death_ch['Date'].iloc[-1].date().strftime("%b %d %Y"))
plt_bar(more_than_1000, 'Countries with more than 1000 COVID-19 cases as of '+last_date,'Country/Region', 'Confirmed cases', '#f54c4c')


# All the cases around the world
total_cases = total_Cases_ww+total_Cases_china
total_recovered = total_Recovered_china+total_Recovered_ww
total_death = total_Death_ww+total_Death_china
data = dict(
    number=[total_cases, total_recovered, total_death],
    category=["Total Cases", "Total Recovered", "Deaths"])
pio.renderers.default = "browser" 
fig = px.funnel(data, x='number', y='category', width=2000, height=1000)
fig.update_layout(
    title={
        'text' : 'COVID-19 Statistics worldwide as of '+ last_date,
        'xanchor': 'center',
        'x':0.5,
        'yanchor': 'top'},
    font=dict(
        #family="Courier New, monospace",
        size=22,
        color="#000000"
    )
    )
fig.show()
fig.write_image(last_date+"/Worldwide totals.png")

