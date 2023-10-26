# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

dropdown_options = [
    {'label': 'ALL Sites', 'value': 'ALL'},
    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
    {'label': 'KSC LC-39A', 'value' : 'KSC LC-39A'},
    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
    
]

@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        fig = px.pie(spacex_df, names='Launch Site', 
                     title='Total Successful Launches by All Sites')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        fig = px.pie(filtered_df, names='class', 
                     title=f"Total Successful Launches for {selected_site}")
    return fig

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    dcc.Dropdown(
        id='site-dropdown',
        options=dropdown_options,
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),
    html.Br(),
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(
        id='payload-slider',
        min=0, 
        max=10000, 
        step=1000,
        marks={
            0: '0',
            1000: '1000 Kg',
            2000: '2000 Kg',
            3000: '3000 Kg',
            4000: '4000 Kg',
            5000: '5000 Kg',
            6000: '6000 Kg',
            7000: '7000 Kg',
            8000: '8000 Kg',
            9000: '9000 Kg',
            10000: '10000 Kg'
        },
        value=[min_payload, max_payload]
    ),
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id="payload-slider", component_property="value")]
)
def update_scatter_plot(selected_site, payload_range):
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= payload_range[0]) & 
        (spacex_df['Payload Mass (kg)'] <= payload_range[1])
    ]
    
    if selected_site == 'ALL':
        fig = px.scatter(
            filtered_df, 
            x='Payload Mass (kg)', 
            y='class', 
            color="Booster Version Category",
            labels={'class': 'Launch Outcome'},
            title='Correlation between Payload and Success for all Launch Sites'
        )
    else:
        site_df = filtered_df[filtered_df['Launch Site'] == selected_site]
        fig = px.scatter(
            site_df, 
            x='Payload Mass (kg)', 
            y='class', 
            color="Booster Version Category",
            labels={'class': 'Launch Outcome'},
            title=f'Correlation between Payload and Success for {selected_site}'
        )
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
