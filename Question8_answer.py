import json
import pandas as pd
import re
import sys
from pandas import json_normalize

def validate_lctr_json(json_path, rules_csv_path="lctr-doie-api-eng (1).csv"):
    # Load and flatten the JSON input
    with open(json_path) as f:
        data = json.load(f)

    flat_data = json_normalize(data, sep='.')

    # Load validation rules
    rules_df = pd.read_csv(rules_csv_path)
    rules_to_check = rules_df[rules_df['Rule type'].isin(['Presence', 'Format'])]

    errors = []
    email_regex = r"[^@]+@[^@]+\.[^@]+"

    # Loop through rules
    for _, rule in rules_to_check.iterrows():
        field = rule['Field Id'].replace("lctr.", "")
        rule_type = rule['Rule type']
        message = rule['Message']
        value = flat_data.get(field, pd.Series([None])).iloc[0]

        # Presence Check
        if rule_type == "Presence":
            if field not in flat_data.columns or pd.isna(value) or value == "":
                errors.append({
                    "field": field,
                    "error": "Missing or empty field",
                    "message": message
                })

        # Format Check
        elif rule_type == "Format" and value:
            if "date" in field.lower():
                try:
                    pd.to_datetime(value)
                except:
                    errors.append({
                        "field": field,
                        "error": "Invalid date format",
                        "message": message
                    })
            elif "amount" in field.lower() or "number" in field.lower():
                try:
                    float(value)
                except:
                    errors.append({
                        "field": field,
                        "error": "Invalid numeric format",
                        "message": message
                    })
            elif "email" in field.lower():
                if not re.match(email_regex, str(value)):
                    errors.append({
                        "field": field,
                        "error": "Invalid email format",
                        "message": message
                    })

    # Save errors
    error_df = pd.DataFrame(errors)
    output_file = f"validation_errors_{json_path.split('.')[0]}_Q8.csv"
    error_df.to_csv(output_file, index=False)
    print(f"✅ Validation complete. Errors saved to: {output_file}")

# ---- MAIN ----
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python Question8_answer.py <path_to_json_file>")
    else:
        json_file = sys.argv[1]
        validate_lctr_json(json_file)
