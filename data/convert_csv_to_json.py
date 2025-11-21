import pandas as pd
import json

# Read the CSV file
csv_path = 'digEds_cat.csv'
df = pd.read_csv(csv_path)

# Convert to list of dictionaries with id, Edition name, and attributes for authoritativeness and renown
items = []
for _, row in df.iterrows():
    item = {
        'id': int(row['id']),
        'Edition name': None if pd.isna(row['Edition name']) else row['Edition name'],
        'Audience': None if pd.isna(row['Audience']) else row['Audience'],
        'Philological statement': None if pd.isna(row['Philological statement']) else row['Philological statement'],
        'Value of witnesses': None if pd.isna(row['Value of witnesses']) else row['Value of witnesses'],
        'Sponsor/Funding body': None if pd.isna(row['Sponsor/Funding body']) else row['Sponsor/Funding body'],
        'Account of textual variance': None if pd.isna(row['Account of textual variance']) else row['Account of textual variance'],
        'URL': None if pd.isna(row['URL']) else row['URL'],
        'Manager or Editor': None if pd.isna(row['Manager or Editor']) else row['Manager or Editor']
    }
    items.append(item)

# Write to JSON file
output_path = 'digEds_cat.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(items, f, indent=2, ensure_ascii=False)

print(f"✓ Converted {len(items)} items from CSV to JSON")
print(f"✓ Output saved to: {output_path}")
