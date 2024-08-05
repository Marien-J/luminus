

ELECTRICITY_PRICE = {'BE': 0.3778,
                     'FR': 0.2591,
                     'NL': 0.2515, #SOURCE EUROSTAT
                     'DE': 0.4020}

GAS_PRICE = {        'BE': 0.0994, #SOURCE EUROSTAT
                     'FR': 0.1181,
                     'NL': 0.1500,
                     'DE': 0.1145}

INJECTION_PRICE = {        'BE': 0.06, 
                     'FR': 0.06,
                     'NL': 0.06,
                     'DE': 0.06}

OIL_PRICE = 0.09

ELEC_CO2_INTENSITY = {2020: 0.171,
                      2030: 0.134,
                      2040: 0.051} #kg/kWh
ELEC_CO2_INTENSITY_ELECTRIFICATION = {
    2020: 0.171,
                      2030: 0.096,
                      2040: 0.019
}

mapper_flemish_co2 = {
                'A': {'E': [-1000, 100], 'co2': [-1000000, 7]},
                'B': {'E': [100, 200], 'co2': [7,12]},
                'C': {'E': [200, 300], 'co2': [12, 31]},
                'D': {'E': [300, 400], 'co2': [31, 51]},
                'E': {'E': [400, 500], 'co2': [51, 71]},
                'F': {'E': [500, 50000], 'co2': [71, 700000000]},}
mapper_flemish = {
                'A': {'E': [-1000, 100], 'co2': [-1000000, 10000000]},
                'B': {'E': [100, 200], 'co2': [-1000000, 10000000]},
                'C': {'E': [200, 300], 'co2': [-1000000, 10000000]},
                'D': {'E': [300, 400], 'co2': [-1000000, 10000000]},
                'E': {'E': [400, 500], 'co2': [-1000000, 10000000]},
                'F': {'E': [500, 50000], 'co2': [-1000000, 10000000]},}

mapper_french = {
                'A': {'E': [-100000, 71], 'co2': [-100000, 7]},
                'B': {'E': [71, 111], 'co2': [7,12]},
                'C': {'E': [111, 181], 'co2': [12, 31]},
                'D': {'E': [181, 251], 'co2': [31, 51]},
                'E': {'E': [251, 331], 'co2': [51, 71]},
                'F': {'E': [331, 50000], 'co2': [71, 700000000]},}


COLS = [
        'Unnamed: 0',
        'name', 
        'scenario_name', 
        'building_type',
        'electricity_consumption', 
        'gas_consumption', 
        'oil_consumption', 
        'pv_production', 
        'electricity_injected',
        'total_co2',
        'heating_consumption',
        'domestic_hot_water_consumption',
        'total_investment_cost',
        'total_subsidies',
        'total_oil_cost',
        'epc_ind',
        'epc_label',
        'total_floor_area',
        'construction_year',
        'heating_system',
        'scale_kadaster'
        ]