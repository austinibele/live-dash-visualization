import dash
import dash_core_components as dcc
import dash_html_components as html
import requests
import datetime
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from .heatmap_fig import heatmap_fig, heatmap_data, heatmap_layout
from .graph_fig import fig, x_data, y_data
from .config import INTERVAL, N_POINTS

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

@app.callback(
    [dash.dependencies.Output("live-graph", "figure"),
     dash.dependencies.Output("heatmap-graph", "figure")],
    dash.dependencies.Input("interval-component", "n_intervals"),
)
def update_graph(n):
    # Perform GET request to retrieve the latest data
    response = requests.get("http://localhost:5000")
    data = response.json()

    # Extract data from the response
    num_sensors = int(data["num_sensors"])
    temperatures = [float(temp) for temp in data["temperatures"]]
    timestamp = datetime.datetime.strptime(data["time"], "%Y-%m-%d %H:%M:%S")

    # Only update data if the new timestamp is later than the last one
    if len(x_data) == 0 or timestamp > x_data[-1]:
        # Update x and y data lists
        x_data.append(timestamp)
        for i in range(num_sensors):
            y_data[i].append(temperatures[i])

        # Keep only the last N_POINTS
        x_data_trimmed = x_data[-N_POINTS:]

        # Update plot traces with new data
        for i in range(num_sensors):
            fig.data[i].x = x_data_trimmed
            y_data_trimmed = y_data[i][-N_POINTS:]
            fig.data[i].y = y_data_trimmed

        # Determine min and max temperatures
        min_temp = min(temperatures)  # ignore empty lists
        max_temp = max(temperatures)  # ignore empty lists

        # Calculate the range for y-axis
        range_diff = max_temp - min_temp
        y_range = [min_temp - 4.5 * range_diff, max_temp + 4.5 * range_diff]

        fig.update_yaxes(range=y_range)  # Update the y-axis range

        # Update heatmap data and color scale
        new_heatmap_data = go.Scatterpolar(
            r=[0] + [0.7]*(num_sensors - 1),
            theta=[0, 0, 45, 90, 135, 180, 225, 270, 315],
            mode='markers',
            marker=dict(
                color=temperatures,
                colorscale='YlOrRd',
                size=80,
                cmin=min_temp,
                cmax=max_temp,
                colorbar=dict(
                    title="Temp. (°C)<br>&nbsp;",  
                    titleside="top",
                    tickmode="array",
                    ticks="outside",
                    titlefont=dict(
                        size=20,  # Increase the font size of colorbar title
                    ),
                    tickfont=dict(
                        size=16,  # Increase the font size of colorbar ticks
                    ),
                ),
            ),
            hovertemplate="Temperature: %{marker.color:.2f}°C<extra></extra>"  # Hovertemplate with °C after the temperature value
        )
        
        
        new_heatmap_fig = go.Figure(data=new_heatmap_data, layout=heatmap_layout)

    return fig, new_heatmap_fig


@app.callback(
    dash.dependencies.Output('interval-component', 'max_intervals'),
    dash.dependencies.Input('live-update-button', 'n_clicks'),
    dash.dependencies.State('live-update-state', 'children')
)
def switch_interval_state(n_clicks, state):
    if n_clicks is None:  # Button has never been clicked
        return -1  # We're currently updating, so allow max intervals
    elif state == 'updating':
        return 0  # Stop updating
    else:
        return -1  # Resume updating


@app.callback(
    [dash.dependencies.Output('live-update-button', 'children'),
     dash.dependencies.Output('live-update-state', 'children')],
    dash.dependencies.Input('interval-component', 'max_intervals')
)
def update_button_text(max_intervals):
    if max_intervals == 0:
        return "Resume Live Updates", 'paused'
    else:
        return "Pause Live Updates", 'updating'


# Define the app layout
app.layout = dbc.Container(
    [
        html.Div(html.H2("Sigma Sensors Dashboard", style={'color': 'white', 'padding-top': '10px'}), className="title-banner"),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(dcc.Graph(id="live-graph", figure=fig)),
                    width={"size": 7, "order": 1, "offset": 0},
                ),
                dbc.Col(
                    dbc.Card(dcc.Graph(id="heatmap-graph", figure=heatmap_fig)),
                    width={"size": 5, "order": 2, "offset": 0},
                ),
            ],
            justify="center",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Button("Pause Live Updates", id='live-update-button', color="primary", className="mt-4"),
                    width=12, className="d-flex justify-content-center"
                )
            ]
        ),
        html.Div(id='live-update-state', style={'display': 'none'}),
        dcc.Interval(id="interval-component", interval=INTERVAL, n_intervals=0),
    ],
    fluid=True,
)

if __name__ == "__main__":
    app.run_server(debug=True, port=8080)
