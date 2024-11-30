import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output  # Add this line
import dash_bootstrap_components as dbc  # Import this

from dash_bootstrap_templates import load_figure_template

load_figure_template(["cyborg", "darkly"])

import pandas as pd
import plotly.express as px

import pandas as pd
from typing import List
from sqlmodel import SQLModel,select, Session

from database import Station, StationMeasurements, engine


def sqlmodel_to_df(objects: List[SQLModel]) -> pd.DataFrame:
    records = [obj.dict() for obj in objects]
    return pd.DataFrame.from_records(records)

with Session(engine) as session:
    statement = select(StationMeasurements)
    results = session.exec(statement).all()
    measurements_df = sqlmodel_to_df(results)
    
    statement = select(Station)
    results = session.exec(statement).all()
    stations_df = sqlmodel_to_df(results)
    
measurements_df['station'] = measurements_df['stationid'].map(stations_df.set_index('stationid')['stationname'])

print(measurements_df.head())


external_scripts = [
    {
        'href': 'https://fonts.googleapis.com/css2?family=Source+Sans+3&display=swap',
        'rel': 'stylesheet'
    }
]



# Create a Dash app
external_stylesheets = [dbc.themes.DARKLY]  # Use a dark theme
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, external_scripts=external_scripts,assets_folder='assets')

# Layout of the app
app.layout = dbc.Container(
    children=[
        html.H1(children='Temperature Histogram'),

        dcc.Dropdown(
            id='measure-dropdown',
            options=[
                {'label': 'Temperature', 'value': 'temperature'},
                {'label': 'Humidity', 'value': 'humidity'},
                {'label': 'Wind Speed', 'value': 'windspeedBft'},
                {'label': 'Feel Temperature', 'value': 'feeltemperature'},
                {'label': 'Ground Temperature', 'value': 'groundtemperature'},
                {'label': 'Wind Gusts', 'value': 'windgusts'},
                {'label': 'Sun Power', 'value': 'sunpower'}
                # Add more measures as needed
            ],
            value='temperature',  # Default selected value
            clearable=False,
            className='mb-4 custom-dropdown',
            # style={
            #     'backgroundColor': '#2A2A2A',  # Dark background
            #     'color': 'white',              # Text color
            #     'borderColor': '#444',         # Border color
            # }

        ),

        dcc.Graph(id='bar-chart')
    ],
    fluid=True,
    className='bg-dark',
    style={'fontFamily': 'Source Sans 3'}  # Set the default font family

)

@app.callback(
    Output('bar-chart', 'figure'),
    Input('measure-dropdown', 'value')
)
def update_bar_chart(selected_measure):
    fig = px.bar(
        measurements_df,
        x='station',
        y=selected_measure,
        title=f'{selected_measure.capitalize()} by Station'
    )

    fig.update_layout(
        font_family="Source Sans 3"
    )
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)