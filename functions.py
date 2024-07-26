import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import plotly.express as px
import json
import plotly.graph_objects as go


from constants import mapper_flemish_co2, ELEC_CO2_INTENSITY

# def check_scale_factors(tmp):
#     #tmp = df[df.scenario_name == 'current situation'].copy()
#     if tmp.scenario_name.nunique() > 1:
#         print('your data has more than one situation. This function only works with a single renovated situation, e.g. current situation')
#     else:
        
#         tmp = tmp.replace({'clu_lab':{'0_0':'a','0_1':'b','0_2':'c','1_0':'d','1_1':'e','1_2':'f',
#                             '2_0':'g','2_1':'h','2_2':'i'},
#                 'building_type':{'GESLOTEN':'gesloten\n bebouwing','OPEN':'open \n bebouwing','HALF_OPEN':'half-open\n bebouwing'},
#                 'CONSTR_PERIOD':{'pre 45':'pre 1945','45-70':'1945-1970','71-90':'1971-1990','91-05':'1991-2005','06-12':'2006-2012','12-20':'2012-2020'}})
        
#         tmp['bouwperiode'] = pd.Categorical(tmp.CONSTR_PERIOD.values,categories =['pre 1945','1945-1970','1971-1990','1991-2005','2006-2012','2012-2020']  )
#         tmp['gebouwtype'] = pd.Categorical(tmp.building_type.values,categories = ['open \n bebouwing','half-open\n bebouwen','gesloten\n bebouwing'])

#         return (
#         (ggplot(tmp,aes(x='clu_lab',y='scale_kadaster'))
#         +geom_col()
#         +facet_grid('building_type~bouwperiode')
#         +theme_minimal()
#         +theme(figure_size=(10,7))
#         +ylab('Aantal gebouwen [-]')
#         +xlab('Woningvariant')
#         ))
    
def map_epc(epc, co2, mapper = mapper_flemish_co2,):
     superior_dict = {'epc': None,
                      'co2': None}
     i = 0
     epcmapper = {0: 'A', 
                  1: 'B',
                  2: 'C',
                  3: 'D',
                  4: 'E',
                  5: 'F'}
     for key, val in mapper.items():
          if (val['E'][0] <= epc <= val['E'][1]) & (superior_dict['epc'] is None):
               superior_dict['epc'] = i
          if (val['co2'][0] <= co2 <= val['co2'][1]) & (superior_dict['co2'] is None):
               superior_dict['co2'] = i
          i+=1
     #print(superior_dict)
     mappable = max(superior_dict['epc'], superior_dict['co2'])
     #print(mappable)
     return epcmapper[mappable]


def mod_solar(pv_production, pv_injection, total_co2, epc_ind, total_floor_area, co2_flag = False, co2_intensity = ELEC_CO2_INTENSITY):
     pv_self_consumption = pv_production - pv_injection
     if co2_flag == True:
        total_co2 = total_co2 - pv_injection * co2_intensity
    
     epc_ind = epc_ind + pv_injection * 2.5 / total_floor_area

     return total_co2, epc_ind

def mod_solar_df(df, co2_flag = False, co2_intensity = ELEC_CO2_INTENSITY):
     if co2_flag == True:
          df['total_co2_mapped'] = df.total_co2 + df.electricity_injected * co2_intensity

     df['epc_ind_mapped'] = df.epc_ind + df.electricity_injected * 2.5 / df.total_floor_area

     return df