import pandas as pd
import random
import streamlit as st

# Streamlit page setup
st.set_page_config(page_title="Content Calendar", layout="centered")

st.title("🚗 Render Booking Content Calendar")
st.write("Here's our 1 week TikTok content plan with randomized posting times (6:00 PM - 8:00 PM)")

# Define the content sequence
content_plan = [
    "App Info",
    "Road Safety",
    "Fun Booking Facts",
    "Misc (Emotion Gain)",
    "Seasonal Places to Visit",
    "TikToker Curated Ads",
    "App Review"
]

# Generate random posting times in 5-minute intervals between 6:00 PM and 8:00 PM
def generate_random_time():
    hour = random.choice([6, 7, 8])
    minute = random.choice([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55])
    if hour == 8 and minute > 0:  # To cap max time at exactly 8:00 PM
        hour = 7
    return f"{hour}: {str(minute).zfill(2)} PM"

# Create the calendar
calendar = []
for day in range(1, 31):
    content_type = content_plan[(day - 1) % len(content_plan)]
    post_time = generate_random_time()
    
    # Add High Budget Ads every 7th day
    if day % 7 == 0:
        content_type += " + High Budget Ad/replace for now"
    
    calendar.append({
        "Day": f"Day {day}",
        "Content Type": content_type,
        "Posting Time": post_time
    })

# Create DataFrame
df = pd.DataFrame(calendar)

# Define custom colors using Streamlit's built-in styling
def color_rows(row):
    color_map = {
        "App Info": "#FFD700",               # Gold
        "Road Safety": "#ADD8E6",            # Light Blue
        "Fun Booking Facts": "#90EE90",      # Light Green
        "Misc (Emotion Gain)": "#FFB6C1",    # Light Pink
        "Seasonal Places to Visit": "#FFA07A",# Light Salmon
        "TikToker Curated Ads": "#DDA0DD",   # Plum
        "App Review": "#F0E68C",             # Khaki
        "High Budget Ad/replace for now": "#FF6347"          # Tomato
    }
    for key in color_map:
        if key in row["Content Type"]:
            return [f'background-color: {color_map[key]};'] * len(row)
    return [''] * len(row)

# Display the styled table
st.dataframe(df.style.apply(color_rows, axis=1))
