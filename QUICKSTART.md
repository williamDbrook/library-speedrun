# Quick Start Guide

## Installation & Running

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Initialize Database
```bash
python init_db.py
```

### 3. Start the Application
```bash
python run.py
```

The application will be available at: **http://localhost:5000**

---

## Default Credentials

**Admin Account:**
- Username: `admin`
- Password: `admin123`

---

## How to Use

### For Regular Users

1. **Sign Up**: Create a new account on the signup page
2. **Login**: Enter your credentials
3. **Browse Catalog**: View all available books with details
4. **Borrow Books**: Click "Borrow" on any available book
5. **Return Books**: Click "Return" on books you've borrowed
6. **Request Books**: Submit requests for books to be added to the library

### For Admin Users

1. **Login** with admin credentials
2. **Admin Dashboard**: Access from the top navigation
3. **Add Books**: Click "+ Add New Book" and fill in details
4. **Manage Books**: Edit or delete existing books
5. **Review Requests**: Approve or reject user book requests
   - Approving a request automatically adds the book to the library

---

## Features Overview

✓ User authentication with secure password hashing
✓ Book catalog with search and browse capabilities
✓ Borrowing system (borrow/return books)
✓ Book request system (users can request new books)
✓ Admin dashboard (manage books and requests)
✓ Role-based access control
✓ JSON-based data storage

---

## Project Files

- `run.py` - Main application entry point
- `init_db.py` - Database initialization script
- `app/` - Application code
  - `__init__.py` - Flask app configuration
  - `models.py` - Data models (User, Book, BookRequest)
  - `routes.py` - Route handlers and blueprints
- `templates/` - HTML templates
- `static/` - CSS stylesheets
- `data/` - JSON data files (created at runtime)

---

## Troubleshooting

**Port 5000 already in use?**
Edit `run.py` and change the port:
```python
app.run(debug=True, host='localhost', port=5001)
```

**Data files missing?**
Run `python init_db.py` again to recreate them.

**Templates not loading?**
Make sure you're running the app from the project root directory.

---

## Next Steps

- Customize admin password
- Add more books to the catalog
- Invite other users to join
- Check out the Admin Dashboard to manage requests
