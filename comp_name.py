import re
from app import process_directory

# Access a specific value by index (e.g., the first value)
first_comp_name = comp_name_values[0]

# Print the first comp_name value
# print(first_comp_name)

def extract_company_name(first_comp_name):
    pattern = r"(?i)\b(?:inc|corp|ltd|llc|co)\b|[A-Z][a-zA-Z.&\s]+(?:[,-]\s?[A-Z][a-zA-Z.&\s]+)*"
    # pattern = r"([A-Z][\w]+[ -]+){1,3}(Ltd|ltd|LTD|llc|LLC|Inc|inc|INC|plc|Corp|Group)"

    match = re.search(pattern, first_comp_name)
    if match:
        company_name = match.group()
        return company_name
    else:
        return None
input_dir  = ''
output_dir = 'output.html'
# Access the comp_name column from df1
comp_name_values = process_directory(input_dir,output_dir)['COMPANY_NAME']

# Example usage
# text = "Welcome to OpenAI Inc. We are a technology company specializing in AI solutions."
# company_name = extract_company_name(text)
# print(company_name)
# if __name__ == '__main__':
#     main()