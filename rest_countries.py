# Below is an api endpoint to show you all countries that speak spanish. Dive into the data and answer the following
# questions:

# 1) Display the common name, currency symbol, population and timezone of each country that is NOT landlocked and is in
# the South American continent.

# 2) using the latitude and longitude of the data from the query above, diplay the country information on a world map (using code below)


import requests
import json

url = 'https://restcountries.com/v3.1/lang/spanish'

# make the call to the API

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
req  = requests.get(url, headers = headers)
print("status code:", req.status_code)
#create an output file so you can see the json response that was returned by the API call
webpage = req.json()

outfile = open("country_data.json","w")
json.dump(webpage, outfile, indent= 4)
outfile.close()
infile = open("country_data.json", "r")
data = json.load(infile)



# Create a list of country names, longitudes, latitudes and population for all countries.
# NOTE: It is important to use these names for the map to work correctly.
names = []
lons = []
lats = []
population = []




# populate this list with the data from the api call using a loop and print out information
# per requirements in 1)

for country in data:
    if country['landlocked'] == False and "South America" in country['continents']:
        print(f"Common Name: {country['name']['common']}")
        for val in country['currencies'].values():
            print(f"Currency: {val['symbol']}")
        print(f"Population: {country['population']:,}")
        print(f"Timezone: {country['timezones'][0]}\n")

        names.append(country['name']['common'])
        population.append(country['population'])
        lats.append(country['latlng'][0])
        lons.append(country['latlng'][1])


infile.close()




#Plotly World Map (NOTE: NO CODING NEEDED HERE!)

from plotly.graph_objs import Scattergeo, Layout
from plotly import offline


data = [{
    'type': 'scattergeo',
    'lon': lons,
    'lat': lats,
    'text':names,
    'marker':{
        'size':[p/3_000_000 for p in population],
        'color':population,
        'colorscale':'Viridis',
        'reversescale':True,
        'colorbar':{'title':'Population'}
    },
}]

my_layout = Layout(title='South American Countries that are not landlocked')

fig = {'data':data, 'layout':my_layout}

offline.plot(fig,filename='south_america.html')