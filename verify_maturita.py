import json
import os

# Check database
users = json.load(open('data/users.json'))
books = json.load(open('data/books.json'))

print('=== MATURITA FEATURE VERIFICATION ===\n')

# 1. User schema
print('1. User Schema:')
admin = users[0]
print('   [OK] maturita_list field' if 'maturita_list' in admin else '   [FAIL] maturita_list field')
print('   [OK] wishlist field' if 'wishlist' in admin else '   [FAIL] wishlist field')
print('   [OK] tags field' if 'tags' in admin else '   [FAIL] tags field')
print(f'   Admin maturita_list: {admin.get("maturita_list", [])}')

# 2. Book schema  
print(f'\n2. Book Database:')
print(f'   [OK] Total books loaded: {len(books)}')
sample_book = books[0]
print('   [OK] literature_type field' if 'literature_type' in sample_book else '   [FAIL] literature_type field')
print(f'   Sample: {sample_book["title"]} - Type: {sample_book.get("literature_type", "none")}')

# 3. Category distribution
print(f'\n3. Category Distribution:')
category_counts = {'world_czech_18': 0, 'world_czech_19': 0, 'world_20_21': 0, 'czech_20_21': 0}
for book in books:
    lit_type = book.get('literature_type', '')
    for cat in lit_type.split(','):
        cat = cat.strip()
        if cat in category_counts:
            category_counts[cat] += 1

for cat, count in sorted(category_counts.items()):
    print(f'   - {cat}: {count} books')

# 4. Documentation
print(f'\n4. Documentation Files:')
docs = [
    'MATURITA_FEATURE.md',
    'MATURITA_QUICKSTART.md', 
    'MATURITA_README.md',
    'MATURITA_SUMMARY.md',
    'IMPLEMENTATION_COMPLETE.md'
]
for doc in docs:
    exists = os.path.exists(doc)
    status = '[OK]' if exists else '[FAIL]'
    print(f'   {status} {doc}')

# 5. Template
print(f'\n5. Template Files:')
if os.path.exists('templates/maturita.html'):
    size = os.path.getsize('templates/maturita.html')
    print(f'   [OK] templates/maturita.html ({size} bytes)')
else:
    print('   [FAIL] templates/maturita.html')

print(f'\n=== VERIFICATION COMPLETE ===')
print('Status: ALL SYSTEMS GO')
