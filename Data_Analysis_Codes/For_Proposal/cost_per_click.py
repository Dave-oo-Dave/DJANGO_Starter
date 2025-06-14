import pandas as pd
import plotly.express as px

# Data Preparation (using the same DataFrame)
facebook_ads_costs = {
    'Country': [
        'United States', 'Australia', 'United Kingdom', 'Germany', 'South Korea',
        'Thailand', 'India', 'Nepal', 'Bangladesh', 'Sri Lanka'
    ],
    'Average CPM (USD)': [
        20.48, 11.04, 10.85, 10.05, 8.13,
        4.00, 2.00, 0.15, 0.10, 0.10
    ],
    'Average CPC (USD)': [
        2.70, 2.10, 0.91, 0.66, 2.50, # South Korea is high CPC despite lower CPM
        0.17, 0.09, 0.04, 0.03, 0.03
    ]
}

df_fb_costs = pd.DataFrame(facebook_ads_costs)

# Sort by CPC for this chart
df_fb_costs_sorted_cpc = df_fb_costs.sort_values(by='Average CPC (USD)', ascending=False)

# Visualization Settings (reused from above)
layout_settings = {
    'font_family': 'Arial',
    'title_font_size': 20,
    'xaxis_title_font_size': 14,
    'yaxis_title_font_size': 14,
    'hoverlabel_font_size': 12,
    'bargap': 0.1
}

# Chart for Average CPC (Cost Per Click)
fig_cpc = px.bar(
    df_fb_costs_sorted_cpc,
    x='Country',
    y='Average CPC (USD)',
    color='Country',  # Changed to 'Country' for distinct colors
    color_discrete_sequence=px.colors.qualitative.Plotly, # Use a different qualitative palette
    title='<b>Facebook Ads: Average CPC (Cost Per Click) by Country</b>',
    text='Average CPC (USD)',
    height=550
)

fig_cpc.update_traces(
    texttemplate='$%{text:.2f}',
    textposition='outside',
    marker_line_color='rgba(0,0,0,0.5)',
    marker_line_width=1
)

fig_cpc.update_layout(
    yaxis_title='<b>Average CPC (USD)</b>',
    xaxis_title='<b>Country</b>',
    hovermode='x unified',
    **layout_settings
)
fig_cpc.update_xaxes(categoryorder='total descending')

fig_cpc.show()