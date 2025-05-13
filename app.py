import streamlit as st
from functions import calculate_lcoe, get_lon_lat, annual_energy_output, get_solar_irrd, make_choice


st.title("LCOE Calculator")
st.write("This app calculates the Levelized Cost of Energy (LCOE) for Solar energy projects.")
st.write("Please enter the following parameters:")
capital_cost = st.number_input("Capital Cost (USD per kW)", min_value=0.0, value=1000.0)
annual_om_cost = st.number_input("Annual O&M Cost (USD per kW)", min_value=0.0, value=200.0)
Location = st.text_input("Location (Country, City)", "Nigeria, Lagos")
panel_area = st.number_input("Available area (m2)", min_value=0.0, value=1000.0)
daily_sunlight_hours = st.number_input("Average hours of sunlight per day", min_value=0.0, value=10.0)
#start_year = st.number_input("Start Year", min_value=2000, value=2020)
#end_year = st.number_input("End Year", min_value=2000, value=2023)
discount_rate = st.number_input("Discount Rate (%)", min_value=0.0, value=5.0) / 100
lifetime = st.number_input("Lifetime (years)", min_value=1, value=25)   
if st.button("Calculate LCOE"):
    # Get latitude and longitude
    data = get_lon_lat(Location)
    if data == []:
        st.error("Location not found. Please check the input.")
        st.stop()
    # Extract latitude and longitude
    choice = make_choice(data)
    
    start_year=2020
    end_year = start_year
    # Get solar irradiance data
    solar_data = get_solar_irrd(choice, start_year, end_year)
    
    # Calculate annual energy output
    annual_energy = annual_energy_output(solar_data,panel_area,daily_sunlight_hours)
    
    # Calculate LCOE
    lcoe = calculate_lcoe(capital_cost, annual_om_cost, annual_energy, discount_rate, lifetime)
    
    st.write(f"The Levelized Cost of Energy (LCOE) is: ${lcoe:.4f} per kWh")
