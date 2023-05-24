import plotly.graph_objs as go
from .config import N_SENSORS, HEATMAP_TMIN, HEATMAP_TMAX

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

heatmap_fig = go.Figure(data=heatmap_data, layout=heatmap_layout)


