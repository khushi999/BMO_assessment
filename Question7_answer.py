import json
import pandas as pd
from pandas import json_normalize
import re

# Load and flatten the sample data
with open("Sample_Data.json") as f:
    sample_data = json.load(f)

flat_data = json_normalize(sample_data, sep='.')

# Load the validation rules CSV
rules_df = pd.read_csv("lctr-doie-api-eng (1).csv")

# Filter relevant rule types for this task
rules_to_check = rules_df[rules_df['Rule type'].isin(['Presence', 'Format'])]

errors = []
email_regex = r"[^@]+@[^@]+\.[^@]+"

# Loop through rules and apply checks
for _, rule in rules_to_check.iterrows():
    field = rule['Field Id'].replace("lctr.", "")
    rule_type = rule['Rule type']
    message = rule['Message']

    value = flat_data.get(field, pd.Series([None])).iloc[0]

    # 1. Presence Check
    if rule_type == "Presence":
        if field not in flat_data.columns or pd.isna(value) or value == "":
            errors.append({
                "field": field,
                "error": "Missing or empty field",
                "message": message
            })

    # 2. Format Checks
    elif rule_type == "Format" and value:
        # Date format
        if "date" in field.lower():
            try:
                pd.to_datetime(value)
            except:
                errors.append({
                    "field": field,
                    "error": "Invalid date format",
                    "message": message
                })

        # Numeric format
        elif "amount" in field.lower() or "number" in field.lower():
            try:
                float(value)
            except:
                errors.append({
                    "field": field,
                    "error": "Invalid numeric format",
                    "message": message
                })

        # Email format
        elif "email" in field.lower():
            if not re.match(email_regex, str(value)):
                errors.append({
                    "field": field,
                    "error": "Invalid email format",
                    "message": message
                })

# Output to CSV
error_df = pd.DataFrame(errors)
error_df.to_csv("validation_errors_sample_data.csv", index=False)

print("Validation errors saved to 'validation_errors_sample_data.csv'")
