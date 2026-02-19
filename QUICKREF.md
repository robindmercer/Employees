# Quick Reference Guide 📋

## Starting the Application

```bash
# 1. Activate virtual environment (if using one)
venv\Scripts\activate

# 2. Start the app
python app.py

# 3. Open browser
# http://localhost:5000
```

## Key Routes

| URL | Action | Purpose |
|-----|--------|---------|
| `/` | GET | View all employees |
| `/landing` | GET | Dashboard with live stats |
| `/create` | GET | Show add form |
| `/store` | POST | Add new employee |
| `/edit/<id>` | GET | Show edit form |
| `/update/<id>` | POST | Update employee |
| `/delete/<id>` | POST | Delete employee |
| `/api/stats` | GET | JSON: employee/sector/profile counts |

## Configuration

**File**: `.env`

```env
FLASK_ENV=development          # development or production
SECRET_KEY=your-secret-key     # Keep this secret!
MYSQL_HOST=localhost           # Database server
MYSQL_USER=root                # Database user
MYSQL_PASSWORD=                # Database password
MYSQL_DB=pythonemp             # Database name
UPLOAD_FOLDER=uploads          # File upload directory
MAX_FILE_SIZE=5242880          # Max 5MB
```

## File Locations

```
📁 Project Root
├── app.py                     # Main application
├── config.py                  # Settings
├── db.py                      # Database
├── utils.py                   # Validation
├── requirements.txt           # Dependencies
├── .env                       # Configuration (your secrets)
├── .env.example               # Template (safe to commit)
│
├── 📁 routes/
│   └── 📁 __pycache__/
│       ├── __init__.py            # SQL'S
│       ├── empleados.py           # SQL'S
│       ├── perfil.py              # SQL'S
│       └── sectores.py            # SQL'S
│
├── 📁 static/
│   ├── 📁 css/
│   │    └── oputput.css       # CSS form
│   └── 📁 src/ 
│        └── input.css         # CSS form
│
├── 📁 templates/ 
│   ├── header.html            # Navigation
│   ├── footer.html            # Footer
│   ├── landing.html           # Landing page
│   ├── 404.html               # Error page
│   ├── 📁 empleados/
│   │    ├── index.html        # Employee list
│   │    ├── create.html       # Add form
│   │    └── edit.html         # Edit form
│   ├── 📁 perfiles/
│   │    ├── index.html        # Employee list
│   │    └── perfil.html       # Edit form
│   └── 📁 sectores/
│        ├── index.html        # Employee list
│        └── sector.html       # Edit form
│
└── 📁 uploads/               # Employee photos
    └── .gitkeep
```

## Important Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate          # Windows
source venv/bin/activate       # Linux/Mac

# Start application
python app.py

# Check installed packages
pip list

# Install a package
pip install flask

# Generate requirements file
pip freeze > requirements.txt
```

## Database Setup

1. ✅ Run Mysql Server (In mi case i used XAMPP)
2. ✅ Start PhpAdmin to manage database

```sql
-- Create database
CREATE DATABASE pythonemp;

-- Use database
USE pythonemp;

-- Create Tables
CREATE TABLE perfiles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    descripcion VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE sectores (
    id INT PRIMARY KEY AUTO_INCREMENT,
    descripcion VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE empleados (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(120) NOT NULL,
    foto VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Verify table
SELECT * FROM empleados;

-- Clear all employees (if needed)
DELETE FROM empleados;

```

## Validation Rules

| Field | Min | Max | Format |
|-------|-----|-----|--------|
| Name | 2 | 100 | Text |
| Email | - | 120 | valid@email.com |
| Photo | - | 5MB | JPG, PNG, GIF, JPEG |

## Common Errors & Fixes

### "No module named flask"
```bash
pip install -r requirements.txt
```

### "Connection refused" (MySQL)
- Start MySQL server (in mi case XAMPP)
- Check credentials in .env

### "File upload failed"
- Check uploads/ folder exists
- Verify file size < 5MB
- Check file format (jpg/png/gif)

### "Port 5000 already in use"
Edit app.py:
```python
app.run(debug=True, port=5001)  # Use 5001
```

## Live Statistics & Dashboard

**Landing Page** (`/landing`)
- Shows total employee count from database
- Displays active sectors count
- Shows profile definitions count
- System status indicator
- Navigation buttons to manage team

**API Endpoint** (`/api/stats`)
```bash
GET /api/stats

# Response:
{
  "empleados": 25,
  "sectores": 5,
  "perfiles": 12
}
```

**Employee List** (`/`)
- Shows total count at top of page
- Displays all employees in table
- Each employee shows: ID, photo, name, email, profile, sector

## Testing Checklist

- [ ] Can view landing page with live stats
- [ ] Employee count updates when adding/deleting
- [ ] Can view employee list
- [ ] Can add new employee
- [ ] Photo uploads successfully
- [ ] Can edit employee
- [ ] Can delete employee
- [ ] Validation works (try invalid email)
- [ ] Proper error messages show
- [ ] Navigation works
- [ ] Forms work on mobile
- [ ] Database saves correctly
- [ ] API endpoint returns correct JSON

## Security Reminders

🔐 **Do:**
- [ ] Keep .env file secret (never commit)
- [ ] Use strong SECRET_KEY
- [ ] Use strong MySQL password
- [ ] Keep dependencies updated
- [ ] Review error logs
- [ ] Validate all user input

🔒 **Don't:**
- [ ] Commit .env file
- [ ] Expose database password
- [ ] Use default SECRET_KEY in production
- [ ] Trust user input without validation
- [ ] Ignore error logs

## Performance Tips

1. **Database**: Add indexes on frequently queried columns
2. **Images**: Resize images before saving
3. **Caching**: Cache employee list
4. **Compression**: Enable gzip compression
5. **CDN**: Use CDN for Bootstrap/jQuery

## Documentation Files

- **README.md** - Full project documentation
- **SETUP.md** - Installation and setup guide
- **IMPROVEMENTS.md** - What was improved
- **this file** - Quick reference

## Useful Links

- Flask Docs: https://flask.palletsprojects.com
- MySQL Docs: https://dev.mysql.com/doc/
- Bootstrap Docs: https://getbootstrap.com/docs
- Python PEP 8: https://pep8.org

## File Upload Storage

**Location**: `uploads/` directory

**Naming**: `YYYYMMDDHHMISS_originalname.ext`

**Example**: `20260202143055_john_doe.jpg`

## Next Steps

1. ✅ Get app running locally
2. ✅ Test all features
3. ✅ Customize styling
4. ✅ Add more validation
5. ✅ Deploy to production
6. ✅ Set up monitoring

## Need Help?

1. Check error messages in console
2. Review browser console (F12)
3. Check application logs
4. Read README.md
5. Check SETUP.md troubleshooting section

---

**Version**: 2.1 | **Last Updated**: Feb 18, 2026

## Recent Changes (v2.1)

✨ **New Features:**
- Dynamic employee counting from database
- Landing page dashboard with live statistics
- API endpoint for stats (`/api/stats`)
- Employee list shows total count
- Logo now links to landing/dashboard instead of employee list
