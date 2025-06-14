import pandas as pd
import plotly.express as px

# Data for Google Ads budget breakdown by Ad Type
google_ads_ad_type_budget = {
    'Ad Type': ['Google App Campaigns (UACs)', 'Targeted Search Campaigns'],
    'Budget Allocation (USD)': [80, 20]
}

df_google_ad_type = pd.DataFrame(google_ads_ad_type_budget)

# Create the pie chart for Ad Type breakdown
fig_ad_type_google = px.pie(
    df_google_ad_type,
    names='Ad Type',
    values='Budget Allocation (USD)',
    title='<b>Google Ads Budget Breakdown by Ad Type for SAARC Countries ($100/Month)</b>',
    color='Ad Type',
    color_discrete_sequence=px.colors.qualitative.D3 # A different palette
)

fig_ad_type_google.update_traces(
    textinfo='percent+label',
    pull=[0.05 if ad_type == 'Google App Campaigns (UACs)' else 0 for ad_type in df_google_ad_type['Ad Type']],
    textfont_size=14,
    marker=dict(line=dict(color='#FFFFFF', width=2))
)

fig_ad_type_google.update_layout(
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.2,
        xanchor='center',
        x=0.5
    ),
    font_family='Arial',
    title_font_size=20,
    hoverlabel_font_size=12
)

fig_ad_type_google.show()