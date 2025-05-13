import requests
from keys import API_KEY

asso_name = "solarUni" #replace with your association name
#API key for geocode.maps.co

#get longitude and latitude values using api 
def get_lon_lat(place):
    location = place
    url = f"https://geocode.maps.co/search?q={location}&api_key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error: {response.status_code}")

# extract lat and lon values
def make_choice(data):
    choice = {"lat":"", "lon":""}
    if len(data) != 0:
        choice["lat"]+=data[0]["lat"]
        choice["lon"]+=data[0]["lon"]
    return choice

#get solar irrdnce fro api for
def get_solar_irrd(choice,start_year, end_year):
    # Define the API endpoint
    solar_url = f"https://power.larc.nasa.gov/api/temporal/daily/point?start={start_year}&end={end_year}&latitude={choice["lat"]}&longitude={choice["lon"]}&community=sb&parameters=ALLSKY_SFC_SW_DWN&format=json&user={asso_name}&header=true&time-standard=utc"
    
    # Make the GET request
    response = requests.get(solar_url)
    
    # Check the status code
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        return data
    else:
        print(f"Error: {response.status_code}")


#Annual energy output calculator
def annual_energy_output(data, panel_area, daily_sunlight_hours):
    irr_vals = data["properties"]["parameter"]["ALLSKY_SFC_SW_DWN"]
    av_days = 0
    irr = 0 #in Wh
    days = list(irr_vals.keys())[:-1]
    for d in days:
        if irr_vals[d] > 0:
            irr += (irr_vals[d] * daily_sunlight_hours * panel_area) #12 for 12 hours of sunlight
            av_days+=1
    if av_days == 0:
        return 0
    irr = irr + (irr/av_days) * (365 - av_days)
    irr /= 1000
    return irr

#Lcoe calculator
def calculate_lcoe(capital_cost, annual_om_cost, annual_energy_output, discount_rate, lifetime):
    '''
    capital_cost in curr/KW
    annual_om_cost (annual operation and maintenance cost) in curr/KW
    annual_energy_output in KWhr
    lifetime in yrs
    '''
    total_cost = capital_cost
    for year in range(1, lifetime + 1):
        total_cost += annual_om_cost / ((1 + discount_rate) ** year)
    total_energy = annual_energy_output * lifetime
    if total_energy == 0:
        return 0
    lcoe = total_cost / total_energy
    return lcoe