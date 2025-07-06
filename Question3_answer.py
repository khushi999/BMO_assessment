import json
import pandas as pd
from pandas import json_normalize
import requests

# Opening the sample LCTR JSON file to read data
with open("Sample_Data.json", "r") as f:
    data = json.load(f)

# Using pandas to flatten the nested JSON structure
# sep="_" will separate nested keys using underscores
# max_level=3 limits how deep the flattening goes
flat_data = json_normalize(
    data,
    sep="_",
    max_level = 3
)

# Printing the first few rows to verify the structure
print(flat_data.head())

# Saving the flattened data into a CSV for further use
flat_data.to_csv("flattened_lctr_data.csv", index=False)