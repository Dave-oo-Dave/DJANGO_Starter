import pandas as pd
import plotly.express as px

# Data Preparation (assuming df_countries is already defined as in your original code)
top_countries_data = {
    'Country': ['India', 'U.S.A.', 'China', 'U.K.', 'Bangladesh',
               'Australia', 'Thailand', 'Sri Lanka', 'Germany', 'South Korea'],
    'Arrivals': [317772, 111216, 101879, 57554, 48848,
                43980, 30745, 30226, 29801, 27071],
    'Region': ['SAARC', 'AMERICAS', 'ASIA', 'EUROPE', 'SAARC',
              'OCEANIA', 'ASIA', 'SAARC', 'EUROPE', 'ASIA']
}
df_countries = pd.DataFrame(top_countries_data)

# Create bar chart with a different color for each bar (based on 'Country')
fig = px.bar(
    df_countries,
    x='Country',
    y='Arrivals',
    color='Country',  # Changed to 'Country' to color each bar uniquely
    text='Arrivals',
    title='<b>TOP 10 Source Market Countries</b>',
    color_discrete_sequence=px.colors.qualitative.Plotly, # Use a qualitative palette for distinct colors
    hover_data={'Region': True, 'Arrivals': ':,'}
)

fig.update_traces(
    texttemplate='%{text:,}',
    textposition='outside',
    marker_line_color='rgba(0,0,0,0.5)',
    marker_line_width=1
)

fig.update_layout(
    yaxis_title='<b>Number of Arrivals</b>',
    xaxis_title='<b>Country</b>',
    hovermode='x unified',
    font_family='Arial',
    title_font_size=24,
    xaxis_title_font_size=18,
    yaxis_title_font_size=18,
    legend_title_font_size=16,
    hoverlabel_font_size=14
)

fig.show()