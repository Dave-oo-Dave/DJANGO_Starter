import pandas as pd
import plotly.express as px

# Data for Google Ads budget breakdown PER SAARC COUNTRY
saarc_country_budget_google = {
    'Country': ['Nepal', 'India', 'Bangladesh (or Sri Lanka)'],
    'Budget Allocation (USD)': [35, 40, 25] # Sums to $100
}

df_saarc_google = pd.DataFrame(saarc_country_budget_google)

# Create the pie chart for Country breakdown
fig_country_google = px.pie(
    df_saarc_google,
    names='Country',
    values='Budget Allocation (USD)',
    title='<b>Google Ads Budget Breakdown Per Major SAARC Country ($100/Month)</b>',
    color='Country',
    color_discrete_sequence=px.colors.qualitative.Safe # Another qualitative palette
)

fig_country_google.update_traces(
    textinfo='percent+label',
    pull=[0.05 if country == 'Nepal' else 0 for country in df_saarc_google['Country']],
    textfont_size=14,
    marker=dict(line=dict(color='#FFFFFF', width=2))
)

fig_country_google.update_layout(
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

fig_country_google.show()