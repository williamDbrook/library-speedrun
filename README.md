## Postup
- Postupoval jsem tím že jsem používal dlouhé prompty s kompletním kontextem pro to co chci

## Jaký model?
- Použil jsem Claude Haiku 4.5

## Kolik to stálo?
- ~122,000 - 142,000 Tokenů

## Jake jsem spokojený
- Velmi stránka je hezká a funkční 


##  Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Initialize Database
```bash
python init_db.py
```

This creates:
- Admin account (username: `admin`, password: `admin123`)
- 8 sample books
- JSON data files

### 3. Start the Server
```bash
python run.py
```

Visit: **http://localhost:5000**

## 🔑 Default Admin Account
- **Username**: `admin`
- **Password**: `admin123`
- **Role**: Admin with Teacher and Librarian tags

