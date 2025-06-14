import pandas as pd
import plotly.express as px

# Estimated User Distribution Data based on discussion
user_distribution_data_revised = {
    'User Type': ['Foreign Tourists', 'Local Tourists', 'Hotels and Resorts', 'Vehicle Owners'],
    'Percentage': [20, 60, 10, 10], # Adjusted percentages based on the discussion
    'Color': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'] # Distinct colors
}

df_users_revised = pd.DataFrame(user_distribution_data_revised)

# Create Pie Chart for Revised User Distribution
fig_users_revised = px.pie(
    df_users_revised,
    names='User Type',
    values='Percentage',
    title='<b>Estimated App User Distribution (Considering Specific Needs)</b>',
    color='User Type',
    color_discrete_map=dict(zip(df_users_revised['User Type'], df_users_revised['Color'])),
    hole=0.4 # Donut chart for better aesthetics
)

fig_users_revised.update_traces(
    textinfo='percent+label', # Show percentage and label
    pull=[0.05 if user == 'Foreign Tourists' else 0 for user in df_users_revised['User Type']], # Slightly pull out Foreign Tourists slice
    textfont_size=14,
    marker=dict(line=dict(color='#FFFFFF', width=2)) # White border around slices
)

fig_users_revised.update_layout(
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.2, # Position legend below the chart
        xanchor='center',
        x=0.5
    ),
    font_family='Arial',
    title_font_size=24,
    hoverlabel_font_size=14
)

fig_users_revised.show()