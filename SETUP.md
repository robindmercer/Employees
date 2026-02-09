# Getting Started Guide 🚀

## Quick Start (5 minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Install Frontend Dependencies
```bash
npm install
```

### 3. Set Up Environment
```bash
copy .env.example .env
```

Then edit `.env` with your MySQL credentials:
```
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=pythonemp
```

### 4. Create Database
In MySQL client or phpMyAdmin, run:
```sql
CREATE DATABASE pythonemp;

USE pythonemp;

CREATE TABLE empleados (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(120) NOT NULL,
    foto VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### 5. Build Tailwind CSS
```bash
npm run build:css
```

### 6. Run Application
```bash
python app.py
```

Visit: **http://localhost:5000**

---

## Detailed Installation Guide

### Prerequisites
- Python 3.7+
- MySQL Server
- pip (usually comes with Python)
- Node.js 18+ and npm

### Step 1: Set Up Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Activate it (Linux/Mac)
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

**Dependencies:**
- Flask 2.3.3 - Web framework
- mysql-connector-python 8.1.0 - MySQL driver
- python-dotenv 1.0.0 - Environment variables
- Werkzeug 2.3.7 - WSGI utilities

### Step 3: Install Frontend Dependencies
```bash
npm install
```

### Step 4: Database Setup

**Using MySQL Command Line:**
```bash
mysql -u root -p
```

**Then execute:**
```sql
CREATE DATABASE pythonemp;

USE pythonemp;

CREATE TABLE empleados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(120) NOT NULL,
    foto VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

**Using phpMyAdmin:**
1. Open http://localhost/phpmyadmin
2. Create new database: `pythonemp`
3. Import the SQL from above

### Step 5: Environment Configuration
```bash
# Copy example file
cp .env.example .env  # Linux/Mac
copy .env.example .env  # Windows

# Edit .env file with your settings
```

**Example .env:**
```env
FLASK_ENV=development
SECRET_KEY=your-very-secret-key-change-this
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=
MYSQL_DB=pythonemp
UPLOAD_FOLDER=uploads
MAX_FILE_SIZE=5242880
```

### Step 6: Build Tailwind CSS
```bash
npm run build:css
```

### Step 7: Start the Application
```bash
python app.py
```

**Output should show:**
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

Open browser and go to: **http://localhost:5000**

---

## Troubleshooting

### Error: "No module named 'flask'"
**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### Error: "MySQL server is not running"
**Solution:** 
- **Windows**: Start MySQL from Services or XAMPP Control Panel
- **Linux**: `sudo service mysql start`
- **Mac**: `brew services start mysql`

### Error: "Access denied for user 'root'@'localhost'"
**Solution:** Update `.env` with correct MySQL password
```env
MYSQL_PASSWORD=your_actual_password
```

### Error: "Table 'pythonemp.empleados' doesn't exist"
**Solution:** Run the SQL database creation script (see Step 3 above)

### Error: "Address already in use"
**Solution:** Change port in app.py
```python
app.run(debug=True, port=5001)  # Use 5001 instead of 5000
```

### Upload not working
**Solution:** Ensure uploads directory exists and is writable
```bash
mkdir uploads
# Windows: attrib +w uploads
# Linux/Mac: chmod 755 uploads
```

---

## Testing the Application

### 1. Test Employee List
- Go to http://localhost:5000
- Should show empty list initially

### 2. Test Add Employee
- Click "Add New Employee"
- Fill in:
  - Name: John Doe
  - Email: john@example.com
  - Photo: Select an image
- Click "Add Employee"
- Should appear in the list

### 3. Test Edit Employee
- Click "Edit" on any employee
- Change details
- Click "Update Employee"

### 4. Test Delete Employee
- Click "Delete" on any employee
- Confirm deletion

---

## Production Deployment

### Using Gunicorn
```bash
pip install gunicorn

# Run on port 8000
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Using Waitress
```bash
pip install waitress

# Create serve.py
```python
from waitress import serve
from app import app
serve(app, host='0.0.0.0', port=8000)
```
```

Then run: `python serve.py`

### Security for Production
1. Change `FLASK_ENV=production` in .env
2. Generate strong `SECRET_KEY`
3. Use strong MySQL password
4. Enable HTTPS
5. Set up proper logging
6. Use a reverse proxy (nginx/Apache)

---

## File Structure Reference

```
emploee/
├── app.py                      # Main application
├── config.py                   # Configuration settings
├── db.py                       # Database module
├── utils.py                    # Utility functions
├── requirements.txt            # Python packages
├── .env.example                # Environment template
├── .gitignore                  # Git ignore rules
├── SETUP.md                    # This file
├── README.md                   # Project documentation
├── uploads/                    # Uploaded photos
│   └── .gitkeep
└── templates/
    ├── header.html             # Navigation
    ├── footer.html             # Footer
    ├── 404.html                # Error page
    └── empleados/
        ├── index.html          # Employee list
        ├── create.html         # Add form
        └── edit.html           # Edit form
```

---

## Next Steps 📚

- Read [README.md](README.md) for full documentation
- Customize styling in `templates/header.html`
- Add more validation in `utils.py`
- Set up logging and monitoring
- Deploy to production server

---

## Getting Help 💬

If you encounter issues:
1. Check the Troubleshooting section above
2. Review error messages in browser console (F12)
3. Check application logs
4. Verify database connection with: `python -c "from db import db; print('Connected!')" `

Happy coding! 🎉
