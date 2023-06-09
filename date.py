# import easyocr
from app import process_directory
from datetime import datetime
date_s = process_directory(input_dir,output_dir)
input_dir = df2['date']
# output_dir =
# date_s = process_directory(input_dir,output_dir)
def dates():

    # Convert the dates to datetime objects
    date_objects = [datetime.strptime(date, "%Y-%m-%d") for date in date_s]

    # Find the maximum and minimum dates
    max_date = max(date_objects)
    min_date = min(date_objects)

    # Convert back to string format if needed
    max_date_str = max_date.strftime("%Y-%m-%d")
    min_date_str = min_date.strftime("%Y-%m-%d")

    print("Due Date:", max_date_str)
    print("Bill Date:", min_date_str)
