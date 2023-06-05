# only use regex..let it be
from ..app import process_directory

import re

def extract_company_name(text):
    pattern = r"(?i)\b(?:inc|corp|ltd|llc|co)\b|[A-Z][a-zA-Z.&\s]+(?:[,-]\s?[A-Z][a-zA-Z.&\s]+)*"
    # pattern = r"([A-Z][\w]+[ -]+){1,3}(Ltd|ltd|LTD|llc|LLC|Inc|inc|INC|plc|Corp|Group)"

    match = re.search(pattern, text)
    if match:
        company_name = match.group()
        return company_name
    else:
        return None

# Example usage
text = "Welcome to OpenAI Inc. We are a technology company specializing in AI solutions."
company_name = extract_company_name(text)
print(company_name)
