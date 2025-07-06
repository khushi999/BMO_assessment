import pandas as pd

# Load the converted CSV file
df = pd.read_csv("lctr-doie-api-eng (1).csv")

# Group by the 'Field Id' (JSON path) and 'Field name', and count number of rules per field
rule_counts = df.groupby(['Field Id', 'Field name']).size().reset_index(name='Number of Rules')

# Save to CSV
rule_counts.to_csv("Validation_rules_count_from_csv.csv", index=False)

print("rule count per field saved to 'Validation_rules_count_from_csv.csv'")
