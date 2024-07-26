import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def barchart_heating_systems(df, 
                             dataset,#colname to distinguish by. 
                               extrapolation = 'standard archetypes'):
    #grouped_df = df.groupby([df.building_type, df.dataset, df.heating_system]).count().reset_index()
    grouped_df = df.groupby([df.building_type, df.dataset, df.heating_system]).agg({'Unnamed: 0': 'count', 'scale_kadaster': 'sum'}).reset_index()
    if extrapolation == 'extrapolated':
        ycol = 'scale_kadaster'
    else:
        ycol = 'Unnamed: 0'
           
    fig = go.Figure()
    color = {'Heat Pump': 'Green',
            'Gasboiler': 'Red',
            'Oil': 'Grey'}
    for heating_system in grouped_df.heating_system.unique():

            tmp = grouped_df.query(f"(heating_system == '{heating_system}')")
            #fig.add_trace(go.Bar(x = [grouped_df['building_type'], grouped_df['dataset']], y = grouped_df['Unnamed: 0'], name = heating_system))
            fig.add_trace(go.Bar(x = [tmp['building_type'], tmp[dataset]], y = tmp[ycol], marker_color = color[heating_system], name = heating_system, text = heating_system))
    fig.update_layout(yaxis_range=[0,50] if extrapolation != 'extrapolated' else [0, 1e6], showlegend = False)
    fig.update_layout(barmode = 'group',
                        xaxis_title='Building Type',
                         yaxis_title='Count' if extrapolation != 'extrapolated' else 'Extrapolated Count',)
    return fig

def boxplot_investment(combined_df, extrapolation = 'standard archetypes'):
        combined_df = combined_df.sort_values('dataset', ascending = True)
        fig = go.Figure()
        fig.add_trace(go.Box(x=[combined_df['building_type'], combined_df['dataset']], 
                             y = combined_df['total_investment_cost'] if extrapolation != 'extrapolated' else combined_df['total_investment_cost'] * combined_df['scale_kadaster'], ),)
        fig.update_layout(
        xaxis_title='Building Type',
        yaxis_title='Investment [€]',
        boxmode='group'
        )
        return fig

def boxplot_co2(combined_df, extrapolation = 'standard archetypes'):
        combined_df = combined_df.sort_values('dataset', ascending = True)
        fig = go.Figure()

        fig.add_trace(go.Box(x=[combined_df['building_type'], combined_df['dataset']], 
                             y = combined_df['total_co2'] if extrapolation != 'extrapolated' else combined_df['total_co2'] * combined_df['scale_kadaster'], ),)
        fig.update_layout(
        xaxis_title='Building Type',
        yaxis_title='Total CO2 [kg/a]',
        boxmode='group'
        )
        return fig