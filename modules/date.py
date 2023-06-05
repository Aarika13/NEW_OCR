from ..app import process_directory
from datetime import datetime

dates = [
    "2023-01-01",
    "2023-02-15",
    "2023-03-10",
    "2023-04-20",
    "2023-05-05"
]

# Convert the dates to datetime objects
date_objects = [datetime.strptime(date, "%Y-%m-%d") for date in dates]

# Find the maximum and minimum dates
max_date = max(date_objects)
min_date = min(date_objects)

# Convert back to string format if needed
max_date_str = max_date.strftime("%Y-%m-%d")
min_date_str = min_date.strftime("%Y-%m-%d")

print("Maximum Date:", max_date_str)
print("Minimum Date:", min_date_str)
