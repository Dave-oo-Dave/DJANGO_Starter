import pandas as pd
import plotly.express as px

# Data for Facebook Ads budget breakdown PER SAARC COUNTRY
# Based on the estimated allocation from our discussion, using mid-points for charting
saarc_country_budget = {
    'Country': ['Nepal', 'India', 'Bangladesh (or Sri Lanka)'],
    'Budget Allocation (USD)': [37.5, 32.5, 30] # These values sum up to $100
}

df_saarc_budget = pd.DataFrame(saarc_country_budget)

# Create the pie chart
fig = px.pie(
    df_saarc_budget,
    names='Country',
    values='Budget Allocation (USD)',
    title='<b>Facebook Ads Budget Breakdown Per Major SAARC Country ($100/Month)</b>',
    color='Country', # Color slices by Country name
    color_discrete_sequence=px.colors.qualitative.Set2 # Using a different qualitative palette for variety
)

fig.update_traces(
    textinfo='percent+label', # Show percentage and label on slices
    pull=[0.05 if country == 'Nepal' else 0 for country in df_saarc_budget['Country']], # Slightly pull out Nepal for emphasis (current location)
    textfont_size=14,
    marker=dict(line=dict(color='#FFFFFF', width=2)) # White border for slices
)

fig.update_layout(
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.2, # Position legend below the chart
        xanchor='center',
        x=0.5
    ),
    font_family='Arial',
    title_font_size=20,
    hoverlabel_font_size=12
)

fig.show()