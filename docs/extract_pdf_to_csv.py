import csv

# Based on the table in the PDF, manually create the categories
categories = [
    {
        'Name': "Author's School of Thought",
        'Attributes used': 'Author, url contents',
        'Output example': 'String eg "Hegelian"',
        'Description': "Author's main philosophical or artistic current"
    },
    {
        'Name': 'Keywords (5)',
        'Attributes used': 'Author, url contents, title',
        'Output example': 'Strings (out of a common pool of keywords, based on the whole corpus)',
        'Description': 'Five Keywords from a common pool across the dataset to connect them based on content and author'
    },
    {
        'Name': 'Authoritativeness',
        'Attributes used': 'Audience, Philological statement, Value of witnesses, citations, Sponsor/founding body, Account of textual variance',
        'Output example': 'String (categorical out of 3: "Moderatly Authoritative", " Authoritative", "Highly Authoritative" )',
        'Description': 'A categorical score based on "Audience, Philological statement, Value of witnesses, citations, Sponsor/founding body, Account of textual variance"'
    },
    {
        'Name': 'Work Description',
        'Attributes used': 'Url contents, Author',
        'Output example': 'String (2-3 sentences)',
        'Description': 'Short description of the paper contents'
    },
    {
        'Name': 'Renown',
        'Attributes used': 'Url contents, citations, Author',
        'Output example': 'String (categorical out 5: "obscure", "lesser known", "known", "well known", "Ubiquitous")',
        'Description': 'A cateorical renown score based on "Url contents, citations, Author"'
    }
]

csv_path = 'categories_from_pdf.csv'

# Write to CSV
with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Name', 'Attributes used', 'Output example', 'Description']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for cat in categories:
        writer.writerow(cat)

print(f"✓ Created CSV with {len(categories)} categories")
print(f"✓ Output saved to: {csv_path}")
print(f"\nCategories:")
for i, cat in enumerate(categories):
    print(f"  {i+1}. {cat['Name']}")

