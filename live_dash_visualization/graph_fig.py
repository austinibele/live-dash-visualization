import plotly.graph_objs as go
from .config import N_SENSORS

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


# Create plot layout
layout = go.Layout(
    xaxis=dict(
        title="Time",
        titlefont=dict(
            size=20,  # Increase the font size of x-axis title
            color="black",  # Set the font color of x-axis title
            family="Arial"  # Set the font family of x-axis title
        )
    ),
    yaxis=dict(
        title="Temp. (°C)",
        titlefont=dict(
            size=20,  # Increase the font size of y-axis title
            color="black",  # Set the font color of y-axis title
            family="Arial"  # Set the font family of y-axis title
        )
    ),
    showlegend=True,
    legend=dict(
        font=dict(
            size=18,  # Increase the font size of legend
            color="black",  # Set the font color of legend
            family="Arial"  # Set the font family of legend
        )
    ),
    width=1050,
    height=700,
    title=dict(
        text="Temperature History",
        x=0.5,  # Center the title
        y=0.97,  # Adjust the position of the title
        font=dict(
            size=32,  # Increase the font size
            color="black",  # Set the font color
            family="Arial"
        )
    )
)


# Create plot figure and heatmap figure
fig = go.Figure(data=plot_data, layout=layout)

