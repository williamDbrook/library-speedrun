import json
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

class User:
    @staticmethod
    def load_all():
        users_file = os.path.join(DATA_DIR, 'users.json')
        if not os.path.exists(users_file):
            return []
        with open(users_file, 'r') as f:
            return json.load(f)
    \
    @staticmethod
    def save_all(users):
        users_file = os.path.join(DATA_DIR, 'users.json')
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(users_file, 'w') as f:
            json.dump(users, f, indent=2)
    
    @staticmethod
    def find_by_username(username):
        users = User.load_all()
        for user in users:
            if user['username'] == username:
                return user
        return None
    
    @staticmethod
    def create(username, password, email, is_admin=False, tags=None):
        if User.find_by_username(username):
            return None
        
        if tags is None:
            tags = []
        
        users = User.load_all()
        user = {
            'id': max([u['id'] for u in users], default=0) + 1,
            'username': username,
            'password': generate_password_hash(password),
            'email': email,
            'is_admin': is_admin,
            'tags': tags,
            'wishlist': [],
            'maturita_list': [],
            'created_at': datetime.now().isoformat()
        }
        users.append(user)
        User.save_all(users)
        return user
    
    @staticmethod
    def update(username, **kwargs):
        users = User.load_all()
        for user in users:
            if user['username'] == username:
                user.update(kwargs)
                User.save_all(users)
                return user
        return None
    
    @staticmethod
    def add_to_wishlist(username, book_id):
        user = User.find_by_username(username)
        if user and book_id not in user.get('wishlist', []):
            user['wishlist'].append(book_id)
            User.update(username, wishlist=user['wishlist'])
            return True
        return False
    
    @staticmethod
    def remove_from_wishlist(username, book_id):
        user = User.find_by_username(username)
        if user and book_id in user.get('wishlist', []):
            user['wishlist'].remove(book_id)
            User.update(username, wishlist=user['wishlist'])
            return True
        return False
    
    @staticmethod
    def add_to_maturita(username, book_id):
        user = User.find_by_username(username)
        if user:
            maturita = user.get('maturita_list', [])
            if book_id not in maturita:
                maturita.append(book_id)
                User.update(username, maturita_list=maturita)
                return True
        return False
    
    @staticmethod
    def remove_from_maturita(username, book_id):
        user = User.find_by_username(username)
        if user and book_id in user.get('maturita_list', []):
            maturita = user['maturita_list']
            maturita.remove(book_id)
            User.update(username, maturita_list=maturita)
            return True
        return False
    
    @staticmethod
    def verify_password(username, password):
        user = User.find_by_username(username)
        if user and check_password_hash(user['password'], password):
            return user
        return None


class Book:
    @staticmethod
    def load_all():
        books_file = os.path.join(DATA_DIR, 'books.json')
        if not os.path.exists(books_file):
            return []
        with open(books_file, 'r') as f:
            return json.load(f)
    
    @staticmethod
    def save_all(books):
        books_file = os.path.join(DATA_DIR, 'books.json')
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(books_file, 'w') as f:
            json.dump(books, f, indent=2)
    
    @staticmethod
    def create(title, author, genre, period, literature_type=None, available=True):
        books = Book.load_all()
        book = {
            'id': max([b['id'] for b in books], default=0) + 1,
            'title': title,
            'author': author,
            'genre': genre,
            'period': period,
            'literature_type': literature_type,
            'available': available,
            'borrowed_by': None,
            'borrowed_date': None,
            'created_at': datetime.now().isoformat()
        }
        books.append(book)
        Book.save_all(books)
        return book
    
    @staticmethod
    def find_by_id(book_id):
        books = Book.load_all()
        for book in books:
            if book['id'] == book_id:
                return book
        return None
    
    @staticmethod
    def update(book_id, **kwargs):
        books = Book.load_all()
        for book in books:
            if book['id'] == book_id:
                book.update(kwargs)
                Book.save_all(books)
                return book
        return None
    
    @staticmethod
    def borrow(book_id, username):
        book = Book.find_by_id(book_id)
        if book and book['available']:
            book['available'] = False
            book['borrowed_by'] = username
            book['borrowed_date'] = datetime.now().isoformat()
            Book.update(book_id, available=False, borrowed_by=username, borrowed_date=book['borrowed_date'])
            return True
        return False
    
    @staticmethod
    def return_book(book_id):
        book = Book.find_by_id(book_id)
        if book and not book['available']:
            Book.update(book_id, available=True, borrowed_by=None, borrowed_date=None)
            return True
        return False
    
    @staticmethod
    def get_book_file(book_id):
        """Generate a text file representation of the book for electronic borrowing"""
        book = Book.find_by_id(book_id)
        if not book:
            return None
        
        content = f"""
╔════════════════════════════════════════════════════════════════════╗
║                      DIGITAL BOOK EDITION                          ║
╚════════════════════════════════════════════════════════════════════╝

Title: {book['title']}
Author: {book['author']}
Genre: {book['genre']}
Time Period: {book['period']}

──────────────────────────────────────────────────────────────────────

CHAPTER 1: Introduction

This is an electronic copy of "{book['title']}" by {book['author']}.

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod
tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim
veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex
ea commodo consequat.

Duis aute irure dolor in reprehenderit in voluptate velit esse cillum
dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non
proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

──────────────────────────────────────────────────────────────────────

CHAPTER 2: Main Content

Sed ut perspiciatis unde omnis iste natus error sit voluptatem
accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae
ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt
explicabo.

Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut
fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem
sequi nesciunt.

──────────────────────────────────────────────────────────────────────

CHAPTER 3: Conclusion

At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis
praesentium voluptatum deleniti atque corrupti quos dolores et quas
molestias excepturi sint occaecati cupiditate non provident.

Similique sunt in culpa qui officia deserunt mollitia animi, id est
laborum et dolorum fuga. Et harum quidem rerum facilis est et expedita
distinctio.

──────────────────────────────────────────────────────────────────────

Downloaded from Library System
"""
        return content


class BookRequest:
    @staticmethod
    def load_all():
        requests_file = os.path.join(DATA_DIR, 'book_requests.json')
        if not os.path.exists(requests_file):
            return []
        with open(requests_file, 'r') as f:
            return json.load(f)
    
    @staticmethod
    def save_all(requests):
        requests_file = os.path.join(DATA_DIR, 'book_requests.json')
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(requests_file, 'w') as f:
            json.dump(requests, f, indent=2)
    
    @staticmethod
    def create(username, title, author, reason=''):
        requests = BookRequest.load_all()
        request = {
            'id': max([r['id'] for r in requests], default=0) + 1,
            'username': username,
            'title': title,
            'author': author,
            'reason': reason,
            'status': 'pending',
            'created_at': datetime.now().isoformat()
        }
        requests.append(request)
        BookRequest.save_all(requests)
        return request
    
    @staticmethod
    def find_by_id(request_id):
        requests = BookRequest.load_all()
        for req in requests:
            if req['id'] == request_id:
                return req
        return None
    
    @staticmethod
    def update_status(request_id, status):
        requests = BookRequest.load_all()
        for req in requests:
            if req['id'] == request_id:
                req['status'] = status
                BookRequest.save_all(requests)
                return req
        return None


class Stats:
    @staticmethod
    def get_stats_file():
        return os.path.join(DATA_DIR, 'stats.json')
    
    @staticmethod
    def load_stats():
        stats_file = Stats.get_stats_file()
        if not os.path.exists(stats_file):
            return {
                'total_visitors': 0,
                'monthly_visits': {},
                'e_book_downloads': 0,
                'last_updated': datetime.now().isoformat()
            }
        try:
            with open(stats_file, 'r') as f:
                return json.load(f)
        except:
            return {
                'total_visitors': 0,
                'monthly_visits': {},
                'e_book_downloads': 0,
                'last_updated': datetime.now().isoformat()
            }
    
    @staticmethod
    def save_stats(stats):
        stats_file = Stats.get_stats_file()
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(stats_file, 'w') as f:
            json.dump(stats, f, indent=2)
    
    @staticmethod
    def track_visitor(username):
        """Track a visitor login"""
        stats = Stats.load_stats()
        current_month = datetime.now().strftime('%Y-%m')
        
        if current_month not in stats['monthly_visits']:
            stats['monthly_visits'][current_month] = []
        
        visitor = {
            'username': username,
            'timestamp': datetime.now().isoformat()
        }
        
        if visitor not in stats['monthly_visits'][current_month]:
            stats['monthly_visits'][current_month].append(visitor)
        
        stats['last_updated'] = datetime.now().isoformat()
        Stats.save_stats(stats)
    
    @staticmethod
    def track_e_book_download():
        """Track an e-book download"""
        stats = Stats.load_stats()
        stats['e_book_downloads'] = stats.get('e_book_downloads', 0) + 1
        stats['last_updated'] = datetime.now().isoformat()
        Stats.save_stats(stats)
    
    @staticmethod
    def get_current_month_visitors():
        """Get number of unique visitors in current month"""
        stats = Stats.load_stats()
        current_month = datetime.now().strftime('%Y-%m')
        visitors = stats['monthly_visits'].get(current_month, [])
        
        # Get unique usernames
        unique_visitors = list(set([v['username'] for v in visitors]))
        return len(unique_visitors)
    
    @staticmethod
    def get_borrowed_books_count():
        """Count books currently borrowed"""
        books = Book.load_all()
        return sum(1 for book in books if not book.get('available', True))
    
    @staticmethod
    def get_active_users_count():
        """Count active users (non-admin)"""
        users = User.load_all()
        return sum(1 for user in users if not user.get('is_admin', False))
    
    @staticmethod
    def get_dashboard_stats():
        """Get all stats for admin dashboard"""
        stats = Stats.load_stats()
        current_month = datetime.now().strftime('%Y-%m')
        
        return {
            'total_users': len(User.load_all()),
            'active_users': Stats.get_active_users_count(),
            'current_month_visitors': Stats.get_current_month_visitors(),
            'total_books': len(Book.load_all()),
            'borrowed_books': Stats.get_borrowed_books_count(),
            'available_books': len(Book.load_all()) - Stats.get_borrowed_books_count(),
            'e_book_downloads': stats.get('e_book_downloads', 0),
            'last_updated': stats.get('last_updated', 'Never')
        }

