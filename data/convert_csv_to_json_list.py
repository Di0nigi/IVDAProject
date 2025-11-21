import pandas as pd
import json

# Read the CSV file
csv_path = 'processed_data.csv'
df = pd.read_csv(csv_path)

# Convert to list format where attributes are in a list
items = []
for _, row in df.iterrows():
    item = {
        'id': int(row['id']),
        'Edition name': None if pd.isna(row['Edition name']) else row['Edition name'],
        'Author': None if pd.isna(row['author']) else row['author'],
        'attributes': [
            None if pd.isna(row['Audience']) else row['Audience'],
            None if pd.isna(row['Philological statement']) else row['Philological statement'],
            None if pd.isna(row['Value of witnesses']) else row['Value of witnesses'],
            None if pd.isna(row['Sponsor/Funding body']) else row['Sponsor/Funding body'],
            None if pd.isna(row['Account of textual variance']) else row['Account of textual variance'],
            None if pd.isna(row['URL']) else row['URL'],
            None if pd.isna(row['Manager or Editor']) else row['Manager or Editor']
        ]
    }
    items.append(item)

# Write to JSON file
output_path = 'digEds_cat_list.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(items, f, indent=2, ensure_ascii=False)

print(f"✓ Converted {len(items)} items from CSV to JSON (list format)")
print(f"✓ Output saved to: {output_path}")
