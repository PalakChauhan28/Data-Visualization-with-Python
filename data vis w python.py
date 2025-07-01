#!/usr/bin/env python
# coding: utf-8

import dash
import more_itertools
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from dash import dash_table

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
app.title = "Automobile Statistics Dashboard"

# List of years 
year_list = [i for i in range(1980, 2024, 1)]

#---------------------------------------------------------------------------------------
# Create the layout of the app
app.layout = html.Div([
    #TASK 2.1 Add title to the dashboard
    html.H1("Automobile Sales Statistics Dashboard",
            style={'textAlign': 'center', 'color': '#f4d03f ', 'font-size': 24}),  # Include style for title

    #TASK 2.2: Add two dropdown menus
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(id='dropdown-statistics',
                     options=[
                         {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                         {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
                     ],
                     value='Select Statistics',
                     placeholder='Select a report type',
                     style={'width': '80%',
                            'padding': '3px',
                            'fontSize': '20px',
                            'textAlignLast': 'center'})
    ]),
    
    html.Div(dcc.Dropdown(id='select-year',
                          options=[{'label': i, 'value': i} for i in year_list],
                          value='Select-year',
                          placeholder='Select-year',
                          style={'width': '80%',
                                 'padding': '3px',
                                 'fontSize': '20px',
                                 'textAlignLast': 'center'})
             ),
    
    html.Div([
        #TASK 2.3: Add a division for output display
        html.Div(id='output-container', className='chart-grid', style={'display': 'flex'})
    ])
])

#TASK 2.4: Creating Callbacks
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value'))
def update_input_container(selected_stat):
    if selected_stat == 'Yearly Statistics':
        return False
    else:
        return True

@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'),
     Input(component_id='select-year', component_property='value')])
     
def update_output_container(report_type, selected_year):
    if report_type == 'Recession Period Statistics':
        print('in the works')

    # Yearly Statistic Report Plots 
    elif (selected_year and report_type == 'Yearly Statistics'):
        # Filter data for the selected year
        yearly_data = data[data['Year'] == int(selected_year)]

        # Plot 1: Yearly Automobile sales using line chart for the whole period
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(
                yas,
                x='Year',
                y='Automobile_Sales',
                title='Average Automobile Sales Over the Years'
            )
        )

        # Plot 2: Total Monthly Automobile sales using line chart
        mas = data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(
            figure=px.line(
                mas,
                x='Month',
                y='Automobile_Sales',
                title='Total Monthly Automobile Sales'
            )
        )

        # Plot 3: Bar chart - average number of vehicles sold during the given year
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(
            figure=px.bar(
                avr_vdata,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title='Average Vehicles Sold by Vehicle Type in the year {}'.format(selected_year)
            )
        )

        # Plot 4: Pie chart - Total Advertisement Expenditure for each vehicle
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(
            figure=px.pie(
                exp_data,
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title='Total Advertisement Expenditure for Each Vehicle'
            )
        )

        return [
            html.Div(className='chart-item', children=[
                html.Div(children=Y_chart1),
                html.Div(children=Y_chart2)
            ], style={'display': 'flex'}),

            html.Div(className='chart-item', children=[
                html.Div(children=Y_chart3),
                html.Div(children=Y_chart4)
            ], style={'display': 'flex'})
        ]

    else:
        return html.Div("Please select appropriate inputs.")

# Run the Dash app
if __name__ == '__main__':
    app.run(debug=True)



