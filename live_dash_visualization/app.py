import dash
import dash_core_components as dcc
import dash_html_components as html
import requests
import datetime
import dash_bootstrap_components as dbc
from .heatmap_fig import heatmap_fig
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
            
        # Update the heatmap figure with the new temperatures
        heatmap_fig.data[0].marker.color = temperatures

    return fig, heatmap_fig


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
        dcc.Interval(id="interval-component", interval=INTERVAL, n_intervals=0),
    ],
    fluid=True,
)


if __name__ == "__main__":
    app.run_server(debug=True, port=8080)
