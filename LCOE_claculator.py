import pandas as pd

# Function to calculate LCOE
def calculate_lcoe(capital_cost, annual_om_cost, annual_energy_output, discount_rate, lifetime):
    total_cost = capital_cost
    for year in range(1, lifetime + 1):
        total_cost += annual_om_cost / ((1 + discount_rate) ** year)
    total_energy = annual_energy_output * lifetime
    lcoe = total_cost / total_energy
    return lcoe

# Example data for a specific country
capital_cost = 1000  # USD per kW
annual_om_cost = 20  # USD per kW
annual_energy_output = 1500  # kWh per kW
discount_rate = 0.05  # 5%
lifetime = 25  # years

# Calculate LCOE
lcoe = calculate_lcoe(capital_cost, annual_om_cost, annual_energy_output, discount_rate, lifetime)
print(f"The LCOE is ${lcoe:.2f} per kWh")

# Load solar irradiance data (example)
# solar_data = pd.read_csv('solar_irradiance_data.csv')
# print(solar_data.head())
