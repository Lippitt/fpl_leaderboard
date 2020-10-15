import requests
import pandas as pd
import numpy as np
import warnings
#--------------------------------
    

#--------------------------------

warnings.filterwarnings('ignore')

#--------------------------------

# get the json file
url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
r = requests.get(url)
json = r.json()

# initialise dataframes
elements = pd.DataFrame(json['elements'])
element_types = pd.DataFrame(json['element_types'])
teams = pd.DataFrame(json['teams'])

# create dataframe with data we want to work with

data = elements[['first_name','second_name','element_type','team','total_points']]

# rearranging and editing dataframe
data.sort_values(by=['total_points'], inplace=True, ascending=False)

data['name'] = data['first_name'] + ' ' + data['second_name']
data['position'] = data.element_type.map(element_types.set_index('id').singular_name_short)
data['team'] = data.team.map(teams.set_index('id').name)
data['badge'] = 'assets/Leeds.png'

data.drop(data.index[data['total_points'] < 10], inplace = True)

for i,row in data.iterrows():
    data.loc[i, 'badge'] = '<img src="assets/'+row['team']+'.png" width ="70">'

del data['first_name']
del data['second_name']
del data['element_type']
del data['team']

data = data[['badge','name','position','total_points']]



# create graphs & charts around dataframe
barplot = data.plot.bar(x='name', y='total_points')

#write dataframe to html and save any graphs/tables
html = data.to_html(escape=False)
html_file = open('table.html','w',encoding='utf-8')
html_file.write('<link rel="stylesheet" type="text/css" href="styling.css">' + html)
html_file.close()
