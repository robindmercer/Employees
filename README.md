# Employee Management System 👥

A modern, secure Flask-based CRUD application for managing employees with file uploads and database integration.

## Features ✨

- **Employee Management**: Create, read, update, and delete employees, assigning profiles and sectors to each employee
- **Photo Uploads**: Secure image upload with validation
- **Email Validation**: Built-in email format validation
- **Responsive Design**: Mobile-friendly interface
- **Error Handling**: Comprehensive error handling and logging
- **Security**: 
  - SQL injection prevention with parameterized queries
  - File upload validation
  - Secure file paths
  - CSRF protection ready
  - Environment variable configuration

## Technology Stack 🛠️

| Technology   | Purpose          |
|--------------|------------------|
| Python 3.7+  | Backend language |
| Flask 2.3+   | Web framework    |
| MySQL        | Database         |
| Jinja2       | Template engine  |
| Tailwind CSS | UI framework     |

## Installation 📦

### Prerequisites
- Python 3.7 or higher
- MySQL server running
- pip (Python package manager)

### Step 1: Clone/Download the Project
```bash
cd c:\Python\emploee
```

### Step 2: Create Virtual Environment (Recommended)
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Install Frontend Dependencies
```bash
npm install
```

### Step 5: Configure Environment Variables
```bash
# Copy the example file
copy .env.example .env

# Edit .env and update your settings:
# MYSQL_HOST=localhost
# MYSQL_USER=root
# MYSQL_PASSWORD=your_password
# MYSQL_DB=pythonemp
# SECRET_KEY=your-secret-key
```

### Step 6: Create Database
```sql
CREATE DATABASE IF NOT EXISTS pythonemp;

CREATE TABLE empleados (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(120) NOT NULL,
    foto VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE sectores(
   id  INT PRIMARY KEY AUTO_INCREMENT,
   descripcion VARCHAR(100),
   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE perfiles(
   id  INT PRIMARY KEY AUTO_INCREMENT,
   descripcion VARCHAR(100),
   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);


```

### Step 7: Create Uploads Directory
```bash
mkdir uploads
```

### Step 8: Build Tailwind CSS
```bash
npm run build:css
```

### Step 9: Run the Application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Project Structure 📁

```
emploee/
├── app.py                  # Main Flask application
├── config.py              # Configuration management
├── db.py                  # Database connection & operations
├── utils.py               # Utility functions & validation
├── requirements.txt       # Python dependencies
├── .env.example            # Environment variables template
├── static/
│   ├── css/
│   │   └── output.css      # Tailwind build output
│   └── src/
│       └── input.css       # Tailwind source
├── uploads/               # Uploaded employee photos
├── templates/
│   ├── header.html        # Navigation header
│   ├── footer.html        # Footer
│   └── empleados/
│       ├── index.html     # Employee list page
│       ├── create.html    # Add employee form
│       └── edit.html      # Edit employee form
└── README.md              # This file
```

## API Routes 🔌

| Method | Route                 | Description            |
|:-|:-|:-|
| GET    | `/`| Display all employees  |
| GET    | `/create`             | Show add employee form |
| POST   | `/store`              | Save new employee      |
| GET    | `/edit/<id>`          | Show edit form         |
| POST   | `/update/<id>`        | Update employee        |
| POST   | `/delete/<id>`        | Delete employee        |
| GET    | `/uploads/<filename>` | Serve uploaded images  |

## Configuration 🔧

### Environment Variables (.env)
```
FLASK_ENV=development          # development or production
SECRET_KEY=your-secret-key     # Flask secret key
MYSQL_HOST=localhost           # Database host
MYSQL_USER=root                # Database user
MYSQL_PASSWORD=                # Database password
MYSQL_DB=pythonemp             # Database name
UPLOAD_FOLDER=uploads          # Upload directory
MAX_FILE_SIZE=5242880          # Max file size (5MB default)
```

### File Upload Settings
- **Allowed Extensions**: JPG, JPEG, PNG, GIF
- **Max File Size**: 5MB (configurable)
- **Storage**: `uploads/` directory

## Validation Rules ✅

### Employee Name
- Required field
- Minimum 2 characters
- Maximum 100 characters

### Email Address
- Required field
- Valid email format
- Maximum 120 characters

### Profile Photo
- Required for new employees
- Allowed formats: JPG, JPEG, PNG, GIF
- Maximum file size: 5MB

## Security Features 🔒

1. **SQL Injection Prevention**: All queries use parameterized statements
2. **File Upload Validation**: Type and size checks
3. **Path Traversal Protection**: Secure file path validation
4. **Error Handling**: User-friendly error messages without exposing system info
5. **Logging**: Comprehensive activity logging
6. **Environment Separation**: Configuration via environment variables
7. **CSRF Protection Ready**: Session-based security

## Logging 📝

Application logs are output to console and can be configured in `app.py`:
```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## Error Handling 🚨

The application includes:
- Database error handling
- File upload error handling
- Input validation errors
- Custom 404 and 500 error pages
- Detailed logging of all errors

## Troubleshooting 🔧

### Database Connection Error
- Check MySQL server is running
- Verify credentials in `.env` file
- Ensure database `pythonemp` exists

### File Upload Error
- Check `uploads/` directory exists and is writable
- Verify file is in allowed format
- Check file size is under 5MB limit

### Port Already in Use
- Change port in `app.py`: `app.run(port=5001)`
- Or kill process using port 5000

## Development 💻

### Running in Development Mode
```bash
export FLASK_ENV=development  # Linux/Mac
set FLASK_ENV=development     # Windows
python app.py
```

### Running in Production
```bash
export FLASK_ENV=production   # Linux/Mac
set FLASK_ENV=production      # Windows
python app.py
```

For production, use a production WSGI server like Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Future Improvements 🚀

- [ ] User authentication and authorization
- [ ] Employee search and filtering
- [ ] Bulk operations (export/import)
- [ ] Soft deletes (archive employees)
- [ ] Activity audit log
- [ ] API endpoints (RESTful API)
- [ ] Email notifications
- [ ] Image optimization and resizing
- [ ] Database backups
- [ ] Unit and integration tests

## Contributing 🤝

Feel free to submit issues and enhancement requests!

## License 📄

This project is open source and available under the MIT License.

## Support 💬

For issues or questions, please create an issue in the repository or contact the development team.

---

**Last Updated**: February 2, 2026
**Version**: 2.0

## Created all md with Copilot
how will you improve this app in all aspects

