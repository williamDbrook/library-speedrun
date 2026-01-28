import os
import json
from app.models import User, Book

# Clear existing data
data_dir = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(data_dir, exist_ok=True)

# Clear old data files
for file in ['users.json', 'books.json', 'book_requests.json']:
    file_path = os.path.join(data_dir, file)
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Cleared {file}")

# Create admin account with tags
print("\nCreating admin account...")
User.create('admin', 'admin123', 'admin@library.com', is_admin=True, tags=['Teacher', 'Librarian'])
print("[+] Admin account created")
print("  Username: admin")
print("  Password: admin123")
print("  Tags: Teacher, Librarian")

# Add sample books
print("\nAdding sample books...")
books_data = [
    # World & Czech Literature till 1800
    ("Don Quixote", "Miguel de Cervantes", "Fiction", "17th Century", "world_czech_18"),
    ("Hamlet", "William Shakespeare", "Drama", "17th Century", "world_czech_18"),
    
    # World & Czech Literature 1800-1900
    ("Pride and Prejudice", "Jane Austen", "Romance", "19th Century", "world_czech_19"),
    ("The Origin of Species", "Charles Darwin", "Science", "19th Century", "world_czech_19"),
    ("Wuthering Heights", "Emily Brontë", "Fiction", "19th Century", "world_czech_19"),
    ("Crime and Punishment", "Fyodor Dostoevsky", "Fiction", "19th Century", "world_czech_19"),
    
    # World Literature 20th-21st Century
    ("To Kill a Mockingbird", "Harper Lee", "Fiction", "20th Century", "world_20_21"),
    ("1984", "George Orwell", "Fiction", "20th Century", "world_20_21"),
    ("The Great Gatsby", "F. Scott Fitzgerald", "Fiction", "20th Century", "world_20_21"),
    ("Dune", "Frank Herbert", "Science Fiction", "20th Century", "world_20_21"),
    ("The Hobbit", "J.R.R. Tolkien", "Fantasy", "20th Century", "world_20_21"),
    ("Brave New World", "Aldous Huxley", "Fiction", "20th Century", "world_20_21"),
    
    # Czech Literature 20th-21st Century
    ("The Adventures of Baron Münchausen", "Rudolf Raspe", "Fiction", "20th Century", "czech_20_21"),
    ("The Good Soldier Švejk", "Jaroslav Hašek", "Fiction", "20th Century", "czech_20_21"),
    ("Metamorphosis", "Franz Kafka", "Fiction", "20th Century", "world_20_21, czech_20_21"),
    ("The Trial", "Franz Kafka", "Fiction", "20th Century", "world_20_21, czech_20_21"),
    ("Closely Watched Trains", "Bohumil Hrabal", "Fiction", "20th Century", "czech_20_21"),
    ("The Unbearable Lightness of Being", "Milan Kundera", "Fiction", "20th Century", "czech_20_21"),
]

for title, author, genre, period, lit_type in books_data:
    Book.create(title, author, genre, period, literature_type=lit_type)
    print(f"  [+] Added: {title}")

print("\n[+] Database initialized successfully!")
print("\nNew Features:")
print("  * User Tags: Student, Teacher, Librarian, Parent, Academic, Researcher")
print("  * Wishlist: Add/remove books from your wishlist")
print("  * Maturita List: Track required reading with category progress")
print("    - World & Czech Literature (until 1800): 2 minimum")
print("    - World & Czech Literature (1800-1900): 3 minimum")
print("    - World Literature (20th-21st Century): 4 minimum")
print("    - Czech Literature (20th-21st Century): 5 minimum")
print("  * E-Copy: Download books as .txt files")
print("  * Physical Borrow: Generate QR codes for physical library borrowing")
print("\nYou can now start the application with: python run.py")
