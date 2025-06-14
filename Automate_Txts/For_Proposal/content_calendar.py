import pandas as pd

# Define the content types and a rough posting sequence
content_plan = [
    "App Info",
    "Road Safety",
    "Fun Booking Facts",
    "Misc (Emotion Gain)",
    "Seasonal Places to Visit",
    "TikToker Curated Ads",
    "App Review",
    "High Budget Ads"
]

# Define specific posting frequency (can be adjusted)
posting_sequence = [
    "App Info", "Road Safety", "Fun Booking Facts", "Misc (Emotion Gain)", 
    "Seasonal Places to Visit", "TikToker Curated Ads", "App Review"
]

# Fill 30 days by repeating the posting sequence
calendar = []
for day in range(1, 31):
    content_type = posting_sequence[(day - 1) % len(posting_sequence)]
    calendar.append({
        "Day": f"Day {day}",
        "Content Type": content_type
    })

# Add High Budget Ads every 7th day as a special post
for i in range(6, 30, 7):  # Day 7, 14, 21, 28
    calendar[i]["Content Type"] += " + High Budget Ad"

# Create DataFrame
df = pd.DataFrame(calendar)

# Display the table
print(df)

# Optionally, export to Excel
# df.to_excel("content_calendar.xlsx", index=False)
