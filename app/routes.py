from flask import Blueprint, render_template, request, redirect, url_for, session, flash, send_file
from app.models import User, Book, BookRequest, Stats
import functools
import qrcode
from io import BytesIO
import os

# Blueprints
auth_bp = Blueprint('auth', __name__)
library_bp = Blueprint('library', __name__)
admin_bp = Blueprint('admin', __name__)

USER_TAGS = ['Student', 'Teacher', 'Librarian', 'Parent', 'Academic', 'Researcher']

# Login required decorator
def login_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in first', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in first', 'error')
            return redirect(url_for('auth.login'))
        
        user = User.find_by_username(session['username'])
        if not user or not user['is_admin']:
            flash('Admin access required', 'error')
            return redirect(url_for('library.catalog'))
        return f(*args, **kwargs)
    return decorated_function

# AUTH ROUTES
@auth_bp.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('library.home'))
    return redirect(url_for('library.home'))

@library_bp.route('/home')
def home():
    stats = Stats.get_dashboard_stats() if 'user_id' in session else None
    return render_template('home.html', stats=stats)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        tags = request.form.getlist('tags')
        
        if not username or not password or not email:
            flash('All fields are required', 'error')
            return redirect(url_for('auth.signup'))
        
        if User.find_by_username(username):
            flash('Username already exists', 'error')
            return redirect(url_for('auth.signup'))
        
        User.create(username, password, email, is_admin=False, tags=tags)
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('signup.html', user_tags=USER_TAGS)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.verify_password(username, password)
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['is_admin'] = user['is_admin']
            # Track visitor
            Stats.track_visitor(username)
            flash(f'Welcome back, {username}!', 'success')
            return redirect(url_for('library.catalog'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'success')
    return redirect(url_for('auth.login'))

# LIBRARY ROUTES
@library_bp.route('/catalog')
@login_required
def catalog():
    books = Book.load_all()
    user = User.find_by_username(session['username'])
    return render_template('catalog.html', books=books, user=user)

@library_bp.route('/book/<int:book_id>')
@login_required
def book_detail(book_id):
    book = Book.find_by_id(book_id)
    if not book:
        flash('Book not found', 'error')
        return redirect(url_for('library.catalog'))
    return render_template('book_detail.html', book=book)

@library_bp.route('/borrow/<int:book_id>', methods=['POST'])
@login_required
def borrow_book(book_id):
    book = Book.find_by_id(book_id)
    if not book:
        flash('Book not found', 'error')
    elif not book['available']:
        flash('Book is already borrowed', 'error')
    else:
        Book.borrow(book_id, session['username'])
        flash(f'You have borrowed "{book["title"]}"', 'success')
    
    return redirect(url_for('library.catalog'))

@library_bp.route('/return/<int:book_id>', methods=['POST'])
@login_required
def return_book(book_id):
    book = Book.find_by_id(book_id)
    if not book:
        flash('Book not found', 'error')
    elif book['available']:
        flash('This book is not borrowed', 'error')
    elif book['borrowed_by'] != session['username']:
        flash('You did not borrow this book', 'error')
    else:
        Book.return_book(book_id)
        flash(f'You have returned "{book["title"]}"', 'success')
    
    return redirect(url_for('library.catalog'))

@library_bp.route('/request-book', methods=['GET', 'POST'])
@login_required
def request_book():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        reason = request.form.get('reason', '')
        
        if not title or not author:
            flash('Title and author are required', 'error')
            return redirect(url_for('library.request_book'))
        
        BookRequest.create(session['username'], title, author, reason)
        flash('Book request submitted successfully!', 'success')
        return redirect(url_for('library.catalog'))
    
    return render_template('request_book.html')

@library_bp.route('/wishlist')
@login_required
def wishlist():
    user = User.find_by_username(session['username'])
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('library.catalog'))
    
    wishlist_ids = user.get('wishlist', [])
    books = Book.load_all()
    wishlist_books = [b for b in books if b['id'] in wishlist_ids]
    return render_template('wishlist.html', books=wishlist_books)

@library_bp.route('/wishlist/add/<int:book_id>', methods=['POST'])
@login_required
def add_to_wishlist(book_id):
    book = Book.find_by_id(book_id)
    if not book:
        flash('Book not found', 'error')
    else:
        if User.add_to_wishlist(session['username'], book_id):
            flash(f'Added "{book["title"]}" to your wishlist', 'success')
        else:
            flash('Book already in your wishlist', 'info')
    
    return redirect(request.referrer or url_for('library.catalog'))

@library_bp.route('/wishlist/remove/<int:book_id>', methods=['POST'])
@login_required
def remove_from_wishlist(book_id):
    book = Book.find_by_id(book_id)
    if not book:
        flash('Book not found', 'error')
    else:
        if User.remove_from_wishlist(session['username'], book_id):
            flash(f'Removed "{book["title"]}" from your wishlist', 'success')
    
    return redirect(request.referrer or url_for('library.catalog'))

@library_bp.route('/maturita')
@login_required
def maturita():
    user = User.find_by_username(session['username'])
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('library.catalog'))
    
    maturita_ids = user.get('maturita_list', [])
    books = Book.load_all()
    maturita_books = [b for b in books if b['id'] in maturita_ids]
    
    # Calculate progress by category
    categories = {
        'world_czech_18': {'min': 2, 'books': []},
        'world_czech_19': {'min': 3, 'books': []},
        'world_20_21': {'min': 4, 'books': []},
        'czech_20_21': {'min': 5, 'books': []}
    }
    
    for book in maturita_books:
        lit_type = book.get('literature_type', '')
        if 'world_czech_18' in lit_type:
            categories['world_czech_18']['books'].append(book)
        if 'world_czech_19' in lit_type:
            categories['world_czech_19']['books'].append(book)
        if 'world_20_21' in lit_type:
            categories['world_20_21']['books'].append(book)
        if 'czech_20_21' in lit_type:
            categories['czech_20_21']['books'].append(book)
    
    # Calculate overall progress
    total_required = 20
    total_progress = len(maturita_books)
    
    return render_template('maturita.html', books=maturita_books, categories=categories, 
                         total_progress=total_progress, total_required=total_required)

@library_bp.route('/maturita/add/<int:book_id>', methods=['POST'])
@login_required
def add_to_maturita(book_id):
    book = Book.find_by_id(book_id)
    if not book:
        flash('Book not found', 'error')
    else:
        if User.add_to_maturita(session['username'], book_id):
            flash(f'Added "{book["title"]}" to your Maturita list', 'success')
        else:
            flash('Book already in your Maturita list', 'info')
    
    return redirect(request.referrer or url_for('library.catalog'))

@library_bp.route('/maturita/remove/<int:book_id>', methods=['POST'])
@login_required
def remove_from_maturita(book_id):
    book = Book.find_by_id(book_id)
    if not book:
        flash('Book not found', 'error')
    else:
        if User.remove_from_maturita(session['username'], book_id):
            flash(f'Removed "{book["title"]}" from your Maturita list', 'success')
    
    return redirect(request.referrer or url_for('library.maturita'))

@library_bp.route('/borrow-electronic/<int:book_id>', methods=['POST'])
@login_required
def borrow_electronic(book_id):
    book = Book.find_by_id(book_id)
    if not book:
        flash('Book not found', 'error')
        return redirect(url_for('library.catalog'))
    
    # Generate the book file content
    content = Book.get_book_file(book_id)
    if not content:
        flash('Could not generate book file', 'error')
        return redirect(url_for('library.catalog'))
    
    # Track e-book download
    Stats.track_e_book_download()
    
    # Create a BytesIO object to send as file
    file = BytesIO(content.encode('utf-8'))
    file.seek(0)
    
    filename = f"{book['title'].replace(' ', '_').lower()}.txt"
    flash(f'Downloaded "{book["title"]}" as electronic copy', 'success')
    
    return send_file(
        file,
        mimetype='text/plain',
        as_attachment=True,
        download_name=filename
    )

@library_bp.route('/borrow-physical/<int:book_id>', methods=['POST'])
@login_required
def borrow_physical(book_id):
    book = Book.find_by_id(book_id)
    if not book:
        flash('Book not found', 'error')
        return redirect(url_for('library.catalog'))
    
    if not book['available']:
        flash('Book is already borrowed', 'error')
        return redirect(url_for('library.catalog'))
    
    # Generate QR code with borrowing info
    qr_data = f"LIBRARY_BORROW|book_id:{book_id}|user:{session['username']}|title:{book['title']}"
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save QR code to BytesIO
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    
    # Mark book as borrowed
    Book.borrow(book_id, session['username'])
    flash(f'Physical borrow initiated for "{book["title"]}". Bring the QR code to the library!', 'success')
    
    filename = f"borrow_qr_{book_id}_{session['username']}.png"
    return send_file(
        img_io,
        mimetype='image/png',
        as_attachment=True,
        download_name=filename
    )

# ADMIN ROUTES
@admin_bp.route('/admin')
@admin_required
def admin_dashboard():
    books = Book.load_all()
    requests = BookRequest.load_all()
    pending_requests = [r for r in requests if r['status'] == 'pending']
    stats = Stats.get_dashboard_stats()
    return render_template('admin_dashboard.html', books=books, pending_requests=pending_requests, stats=stats)

@admin_bp.route('/admin/add-book', methods=['GET', 'POST'])
@admin_required
def add_book():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        genre = request.form.get('genre')
        period = request.form.get('period')
        literature_types = request.form.getlist('literature_type')
        literature_type = ', '.join(literature_types) if literature_types else None
        
        if not all([title, author, genre, period]):
            flash('All fields are required', 'error')
            return redirect(url_for('admin.add_book'))
        
        Book.create(title, author, genre, period, literature_type=literature_type)
        flash('Book added successfully!', 'success')
        return redirect(url_for('admin.admin_dashboard'))
    
    return render_template('add_book.html')

@admin_bp.route('/admin/edit-book/<int:book_id>', methods=['GET', 'POST'])
@admin_required
def edit_book(book_id):
    book = Book.find_by_id(book_id)
    if not book:
        flash('Book not found', 'error')
        return redirect(url_for('admin.admin_dashboard'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        genre = request.form.get('genre')
        period = request.form.get('period')
        literature_types = request.form.getlist('literature_type')
        literature_type = ', '.join(literature_types) if literature_types else None
        
        if not all([title, author, genre, period]):
            flash('All fields are required', 'error')
            return redirect(url_for('admin.edit_book', book_id=book_id))
        
        Book.update(book_id, title=title, author=author, genre=genre, period=period, literature_type=literature_type)
        flash('Book updated successfully!', 'success')
        return redirect(url_for('admin.admin_dashboard'))
    
    return render_template('edit_book.html', book=book)

@admin_bp.route('/admin/delete-book/<int:book_id>', methods=['POST'])
@admin_required
def delete_book(book_id):
    books = Book.load_all()
    books = [b for b in books if b['id'] != book_id]
    Book.save_all(books)
    flash('Book deleted successfully!', 'success')
    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/admin/request/<int:request_id>/approve', methods=['POST'])
@admin_required
def approve_request(request_id):
    book_req = BookRequest.find_by_id(request_id)
    if book_req:
        Book.create(book_req['title'], book_req['author'], 'User Requested', 'Unknown')
        BookRequest.update_status(request_id, 'approved')
        flash(f'Request approved and book added!', 'success')
    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/admin/request/<int:request_id>/reject', methods=['POST'])
@admin_required
def reject_request(request_id):
    BookRequest.update_status(request_id, 'rejected')
    flash('Request rejected', 'success')
    return redirect(url_for('admin.admin_dashboard'))
