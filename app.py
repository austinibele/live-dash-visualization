import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import requests
import datetime
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

# Logging Interval 
INTERVAL = 500 #ms
# Display last N seconds
DISPLAY_N_SECONDS = 30
# Number of points to display
N_POINTS = int((INTERVAL/1000)*DISPLAY_N_SECONDS)
# Number of sensors
N_SENSORS = 9
# Circle diameter for heatmap
CIRCLE_DIAMETER = 100
# Heatmap minimum temperature
HEATMAP_TMIN = 79.5
# Heatmap maximum temperature
HEATMAP_TMAX = 80.5

# Create initial empty data lists
x_data = []
y_data = [[] for _ in range(N_SENSORS)]

# Create plot traces for each temperature
plot_data = []
for i in range(N_SENSORS):
    trace = go.Scatter(
        x=x_data,
        y=y_data[i],
        mode="lines",
        name=f"Sensor {i+1}",
        line=dict(width=2),
    )
    plot_data.append(trace)

# Create heatmap figure layout
heatmap_layout = go.Layout(
    polar=dict(
        radialaxis=dict(
          visible=True,
          ticks='',
          showticklabels=False,
          range=[0, 1]  # Range should be adjusted based on the data
        ),
        angularaxis=dict(
            ticks='',
            showticklabels=False,
            )),
    showlegend=False,
    width=700,  # Increase the width of the plot
    height=700  # Increase the height of the plot
)


# Create heatmap data, initially with no temperatures
heatmap_data = go.Scatterpolar(
    r=[0] + [0.7]*(N_SENSORS - 1),
    theta=[0, 0, 45, 90, 135, 180, 225, 270, 315],
    mode='markers',
    marker=dict(
        color=[0, 0, 0, 0, 0, 0, 0, 0, 0],  # Initially no temperatures
        colorscale='YlOrRd',
        size=80,
        cmin=HEATMAP_TMIN,
        cmax=HEATMAP_TMAX,
        colorbar=dict(
            title="Temperature",
            titleside="top",
            tickmode="array",
            ticks="outside",
        ),
    ),
    hovertemplate="Temperature: %{marker.color}<extra></extra>"  # custom hovertemplate
)

# Create plot layout
layout = go.Layout(
    xaxis=dict(title="Time"),
    yaxis=dict(title="Temperature"),
    showlegend=True,
    width=1120,
    height=700
)

# Create plot figure and heatmap figure
fig = go.Figure(data=plot_data, layout=layout)
heatmap_fig = go.Figure(data=heatmap_data, layout=heatmap_layout)

# Define the app layout
app.layout = dbc.Container(
    [
        html.H1("Sigma Sensors Dashboard", className="text-center mb-4", style={"paddingTop": "20px"}),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(id="live-graph", figure=fig),
                    width={"size": 7, "order": 1, "offset": 0},
                ),
                dbc.Col(
                    dcc.Graph(id="heatmap-graph", figure=heatmap_fig),
                    width={"size": 5, "order": 2, "offset": 0},
                ),
            ],
            justify="center",
        ),
        dcc.Interval(id="interval-component", interval=INTERVAL, n_intervals=0),
    ],
    fluid=True,
)



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


if __name__ == "__main__":
    app.run_server(debug=True, port=8080)
