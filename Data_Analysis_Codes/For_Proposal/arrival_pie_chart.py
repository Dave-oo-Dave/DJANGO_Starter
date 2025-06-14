import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# ======================
# DATA PREPARATION
# ======================

# Top countries data with additional categorization
top_countries_data = {
    'Country': ['India', 'U.S.A.', 'China', 'U.K.', 'Bangladesh', 
                'Australia', 'Thailand', 'Sri Lanka', 'Germany', 'South Korea'],
    'Arrivals': [317772, 111216, 101879, 57554, 48848, 
                 43980, 30745, 30226, 29801, 27071],
    'Region': ['SAARC', 'AMERICAS', 'ASIA', 'EUROPE', 'SAARC',
               'OCEANIA', 'ASIA', 'SAARC', 'EUROPE', 'ASIA']
}

# Region distribution data
region_data = {
    'Region': ['ASIA (SAARC)', 'ASIA (OTHERS)', 'EUROPE', 
               'AMERICAS', 'OTHERS', 'OCEANIA'],
    'Percentage': [36.41, 19.79, 18.03, 11.09, 11.48, 4.75],
    'Color': ['#636EFA', '#EF553B', '#00CC96', 
              '#AB63FA', '#FFA15A', '#19D3F3']
}

# Create DataFrames
df_countries = pd.DataFrame(top_countries_data)
df_regions = pd.DataFrame(region_data)

# ======================
# VISUALIZATION SETTINGS
# ======================

# Custom layout settings
layout_settings = {
    'font_family': 'Arial',
    'title_font_size': 24,
    'legend_title_font_size': 16,
    'hoverlabel_font_size': 14,
    # Corrected way to set axis title font size
    'xaxis': {'title_font_size': 18},
    'yaxis': {'title_font_size': 18}
}

# ======================
# CREATE VISUALIZATIONS
# ======================

# 1. Top Countries Bar Chart
fig_countries = px.bar(
    df_countries,
    x='Country',
    y='Arrivals',
    color='Region',
    title='<b>TOP 10 Source Market Countries</b>',
    text='Arrivals',
    color_discrete_sequence=px.colors.qualitative.Bold,
    hover_data={'Region': True, 'Arrivals': ':,'},
    height=600
)

# Update bar chart styling
fig_countries.update_traces(
    texttemplate='%{text:,}',
    textposition='outside',
    marker_line_color='rgba(0,0,0,0.5)',
    marker_line_width=1
)

fig_countries.update_layout(
    yaxis_title='<b>Number of Arrivals</b>',
    xaxis_title='<b>Country</b>',
    hovermode='x unified',
    # Unpack the layout_settings dictionary. 
    # The 'xaxis' and 'yaxis' keys within layout_settings will be handled correctly by update_layout
    **layout_settings 
)

# 2. Region Distribution Pie Chart
fig_regions = px.pie(
    df_regions,
    names='Region',
    values='Percentage',
    title='<b>Regionwise Distribution of Arrivals</b>',
    color='Region',
    color_discrete_map=dict(zip(df_regions['Region'], df_regions['Color'])),
    hole=0.3
)

# Update pie chart styling
fig_regions.update_traces(
    textinfo='percent+label',
    pull=[0.1, 0, 0, 0, 0, 0],
    textfont_size=14,
    marker=dict(line=dict(color='#FFFFFF', width=2))
)

fig_regions.update_layout(
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.2,
        xanchor='center',
        x=0.5
    ),
    **layout_settings
)

# ======================
# DISPLAY VISUALIZATIONS
# ======================

# Create dashboard layout
fig = make_subplots(
    rows=1, cols=2,
    specs=[[{'type': 'xy'}, {'type': 'domain'}]],
    subplot_titles=('Top Source Markets', 'Regional Distribution')
)

# Add charts to dashboard
# When adding `fig_countries.data[0]`, you are only adding the trace data, not the layout settings
# from fig_countries. To properly merge, you'd typically copy relevant layout elements or
# update the main fig's layout directly for axes.
# For simplicity, we will assume the primary axis titles will be handled by the layout settings
# of the main figure or by adjusting the subplot_titles.

fig.add_trace(fig_countries.data[0], row=1, col=1)
# Copy the layout settings from fig_countries to the subplot's axes if needed
fig.update_xaxes(title_text='<b>Country</b>', row=1, col=1)
fig.update_yaxes(title_text='<b>Number of Arrivals</b>', row=1, col=1)


for trace in fig_regions.data:
    fig.add_trace(trace, row=1, col=2)

# Update dashboard layout
fig.update_layout(
    title_text='<b>Tourist Arrivals Analysis</b>',
    title_x=0.5,
    showlegend=True,
    height=600,
    **layout_settings # Apply general layout settings
)

# Show the dashboard
fig.show()

# Alternatively show individual charts
# fig_countries.show()
# fig_regions.show()