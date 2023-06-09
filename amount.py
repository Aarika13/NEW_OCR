# from app import process_directory, extracted_data
# # print(df2)
# output_dir = extracted_data()
# df2 = process_directory(input, output)
# # amount = process_directory(df2['AMOUNT'])

from app import process_directory, extract_amount
def extract_amount(amount):
    try:
        amt = float(amount)
        if amt > max_amt:
            amount = amt
            return amount
    except Exception as e:
#         pass
# Define the input and output directories
input_dir = "path_to_input_directory"
output_dir = "path_to_output_directory"

# Call the process_directory function with the input and output directories
df2 = process_directory(input_dir,output_dir)

# Access the 'AMOUNT' column from df2 and apply the extract_amount function
df2['AMOUNT'] = df2['AMOUNT'].apply(extract_amount)

# Print the updated df2 dataframe
print(df2)
