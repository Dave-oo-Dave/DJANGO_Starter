import pandas as pd
import plotly.express as px

# Data for Facebook Ads budget breakdown (based on previous estimation)
budget_breakdown_data = {
    'Ad Type': ['App Install Campaigns', 'Video Views / Traffic Campaigns'],
    'Budget Allocation (USD)': [75, 25] # Using the mid-points of the estimated ranges
}

df_budget = pd.DataFrame(budget_breakdown_data)

# Create the pie chart
fig = px.pie(
    df_budget,
    names='Ad Type',
    values='Budget Allocation (USD)',
    title='<b>Facebook Ads Budget Breakdown for SAARC Countries ($100/Month)</b>',
    color='Ad Type', # Color slices by Ad Type
    color_discrete_sequence=px.colors.qualitative.Pastel # A pleasant qualitative palette for the slices
)

fig.update_traces(
    textinfo='percent+label', # Show percentage and label on slices
    pull=[0.05 if ad_type == 'App Install Campaigns' else 0 for ad_type in df_budget['Ad Type']], # Slightly pull out the larger slice for emphasis
    textfont_size=14,
    marker=dict(line=dict(color='#FFFFFF', width=2)) # White border for slices for better separation
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