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
    width=600,  # Increase the width of the plot
    height=650,  # Increase the height of the plot,
    title=dict(
        text="Current Temperature",
        x=0.5,  # Center the title
        y=0.97,  # Adjust the position of the title
        font=dict(
            size=32,  # Increase the font size
            color="black",  # Set the font color
            family="Arial",
         )
    )
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
            title="Temp. (°C)",  # Updated colorbar title
            titleside="top",
            tickmode="array",
            ticks="outside",
            titlefont=dict(
                size=20,  # Increase the font size of colorbar title
            ),
            tickfont=dict(
                size=16,  # Increase the font size of colorbar ticks
            ),
            ypad=30  # Increase the margin between the title and the colorbar
        ),
    ),
    hovertemplate="Temperature: %{marker.color:.2f}°C<extra></extra>"  # Hovertemplate with °C after the temperature value
)

heatmap_fig = go.Figure(data=heatmap_data, layout=heatmap_layout)
