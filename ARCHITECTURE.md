# Application Architecture Diagram

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        USER BROWSER                         │
└────────────────────────────┬────────────────────────────────┘
                             │ HTTP Requests
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                     FLASK APPLICATION                       │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  app.py - Routes & Controllers                       │   │
│  │  ├── @app.route('/')           → index()             │   │
│  │  ├── @app.route('/create')     → create()            │   │
│  │  ├── @app.route('/store', POST)  → store()           │   │
│  │  ├── @app.route('/edit/<id>')   → edit()             │   │
│  │  ├── @app.route('/update/<id>', POST) → update()     │   │
│  │  └── @app.route('/delete/<id>', POST) → delete()     │   │
│  └──────────────────────────────────────────────────────┘   │
└────┬─────────────────────────┬──────────────────┬───────────┘
     │                         │                  │
     ▼                         ▼                  ▼
┌──────────────────┐   ┌──────────────────┐   ┌──────────────┐
│  config.py       │   │  utils.py        │   │  db.py       │
│  ────────────    │   │  ────────────    │   │  ────────────│
│ • Database conf  │   │ • Validation     │   │ • Connection │
│ • File settings  │   │ • File handling  │   │ • Queries    │
│ • App settings   │   │ • Error messages │   │ • Logging    │
└──────────────────┘   └──────────────────┘   └──────┬───────┘
                                                     │
                                                     ▼
                                        ┌────────────────────────┐
                                        │   MYSQL DATABASE       │
                                        │  ─────────────────     │
                                        │  Database: pythonemp   │
                                        │  Table: empleados      │
                                        │  Columns:              │
                                        │  - id (PK)             │
                                        │  - nombre              │
                                        │  - correo              │
                                        │  - foto                │
                                        │  - created_at          │
                                        │  - updated_at          │
                                        └────────────────────────┘
```

## Request Flow Diagram

```
┌──────────────────┐
│   User Action    │
└────────┬─────────┘
         │
         ▼
    ┌─────────┐
    │ Browser │
    └────┬────┘
         │ HTTP Request
         ▼
    ┌──────────────────────────────────┐
    │     Flask Route Dispatcher       │
    │  (Matches URL to handler)        │
    └────────────┬─────────────────────┘
                 │
        ┌────────┴────────┐
        │                 │
        ▼                 ▼
    ┌─────────────────┐  ┌──────────────────┐
    │ GET Request     │  │ POST Request     │
    │ (View/Render)   │  │ (Modify Data)    │
    └────────┬────────┘  └────────┬─────────┘
             │                    │
             ▼                    ▼
    ┌──────────────────┐  ┌──────────────────────────┐
    │ Render Template  │  │ 1. Validate Input        │
    │ (HTML)           │  │    (utils.py)            │
    └────────┬─────────┘  └────────┬─────────────────┘
             │                     │
             │                     ▼
             │            ┌──────────────────────────┐
             │            │ 2. Handle File Upload    │
             │            │    (if applicable)       │
             │            └────────┬─────────────────┘
             │                     │
             │                     ▼
             │            ┌──────────────────────────┐
             │            │ 3. Database Operation    │
             │            │    (db.py)               │
             │            └────────┬─────────────────┘
             │                     │
             │                     ▼
             │            ┌──────────────────────────┐
             │            │ 4. Execute SQL Query     │
             │            │    (MySQL)               │
             │            └────────┬─────────────────┘
             │                     │
             └─────────┬───────────┘
                       │
                       ▼
           ┌───────────────────────────┐
           │ Generate Response         │
           │ - JSON or HTML            │
           └─────────────┬─────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │ Send to Browser      │
              │ (HTTP Response)      │
              └──────────────┬───────┘
                             │
                             ▼
                      ┌──────────────┐
                      │ User Sees    │
                      │ Updated Page │
                      └──────────────┘
```

## Data Flow - Adding Employee

```
User Input Form
      │
      ├─ Name (text input)
      ├─ Email (email input)
      ├─ Photo (file input)
      │
      ▼
POST /store
      │
      ├─────────────────────────────────────────┐
      │     app.py → store() function           │
      │                                         │
      │  1. Get form data                       │
      │     _nombre, _correo, _foto             │
      │                                         │
      │  2. Call utils.validate_input()         │
      │     ├─ Check name length                │
      │     └─ Check email format               │
      │                                         │
      │  3. Call utils.validate_file_upload()   │
      │     ├─ Check file type                  │
      │     ├─ Check file size                  │
      │     └─ Return error if invalid          │
      │                                         │
      │  4. Call utils.save_uploaded_file()     │
      │     ├─ Generate unique filename         │
      │     ├─ Save to uploads/ folder          │
      │     └─ Return filename                  │
      │                                         │
      │  5. Call db.execute_update()            │
      │     ├─ INSERT query                     │
      │     ├─ Execute in MySQL                 │
      │     ├─ Handle errors                    │
      │     └─ Log operation                    │
      │                                         │
      │  6. Flash success message               │
      │     flash('Employee added', 'success')  │
      │                                         │
      │  7. Redirect to index                   │
      └─────────────────────────────────────────┘
      │
      ▼
User Sees Success Message & Updated List
```

## Database Schema

```
┌─────────────────────────────────────────────────────┐
│            EMPLEADOS TABLE                          │
├─────────────────────────────────────────────────────┤
│ id           INT PRIMARY KEY AUTO_INCREMENT         │
├─────────────────────────────────────────────────────┤
│ nombre       VARCHAR(100) NOT NULL                  │
├─────────────────────────────────────────────────────┤
│ correo       VARCHAR(120) NOT NULL                  │
├─────────────────────────────────────────────────────┤
│ foto         VARCHAR(255)                           │
├─────────────────────────────────────────────────────┤
│ created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP    │
├─────────────────────────────────────────────────────┤
│ updated_at   TIMESTAMP ON UPDATE CURRENT_TIMESTAMP  │
└─────────────────────────────────────────────────────┘

Sample Data:
┌────┬───────────────┬──────────────────┬─────────────────────────┐
│ id │ nombre        │ correo           │ foto                    │
├────┼───────────────┼──────────────────┼─────────────────────────┤
│ 1  │ John Doe      │ john@example.com │ 20260202140000_john.jpg │
│ 2  │ Jane Smith    │ jane@example.com │ 20260202140500_jane.png │
│ 3  │ Bob Johnson   │ bob@example.com  │ 20260202141000_bob.jpg  │
└────┴───────────────┴──────────────────┴─────────────────────────┘
```

## File Structure

```
emploee/
│
├── 📄 Core Application Files
│   ├── app.py                    ← Main Flask application
│   ├── config.py                 ← Configuration management
│   ├── db.py                     ← Database operations
│   └── utils.py                  ← Validation utilities
│
├── 📦 Configuration & Dependencies
│   ├── requirements.txt           ← Python packages
│   ├── .env.example               ← Environment template
│   └── .env                       ← Your configuration (DO NOT COMMIT)
│
├── 📁 templates/
│   ├── header.html                ← Navigation navbar
│   ├── footer.html                ← Footer with scripts
│   ├── 404.html                   ← Error page
│   │
│   └── 📁 empleados/
│       ├── index.html             ← Employee list
│       ├── create.html            ← Add employee form
│       └── edit.html              ← Edit employee form
│
├── 📁 uploads/                     ← Employee photos (generated)
│   ├── 20260202140000_photo.jpg
│   ├── 20260202140500_photo.png
│   └── .gitkeep
│
├── 📚 Documentation
│   ├── README.md                  ← Full documentation
│   ├── SETUP.md                   ← Installation guide
│   ├── IMPROVEMENTS.md            ← What changed
│   ├── QUICKREF.md                ← Quick reference
│   ├── SUMMARY.md                 ← Summary (this)
│   └── ARCHITECTURE.md            ← Architecture diagrams
│
└── 📝 Git Files
    ├── .gitignore                 ← Files to ignore
    └── .gitkeep                   ← Keep empty directories
```

## Security Layers

```
┌──────────────────────────────────────────────────┐
│         SECURITY IMPLEMENTATION                  │
├──────────────────────────────────────────────────┤
│                                                  │
│  Layer 1: Input Validation                       │
│  ┌────────────────────────────────────────────┐  │
│  │ Client-side (HTML5 + JavaScript)           │  │
│  │ Server-side (utils.py validation)          │  │
│  │ Returns detailed error messages            │  │
│  └────────────────────────────────────────────┘  │
│                                                  │
│  Layer 2: File Upload Security                   │
│  ┌────────────────────────────────────────────┐  │
│  │ Type validation (JPG/PNG/GIF only)         │  │
│  │ Size validation (< 5MB)                    │  │
│  │ Secure filename generation                 │  │
│  │ Path traversal prevention                  │  │
│  └────────────────────────────────────────────┘  │
│                                                  │
│  Layer 3: Database Security                      │
│  ┌────────────────────────────────────────────┐  │
│  │ Parameterized queries (no SQL injection)   │  │
│  │ Connection pooling                         │  │
│  │ Transaction management                     │  │
│  │ Error handling with rollback               │  │
│  └────────────────────────────────────────────┘  │
│                                                  │
│  Layer 4: Application Security                   │
│  ┌────────────────────────────────────────────┐  │
│  │ Environment variables (.env)               │  │
│  │ No hardcoded credentials                   │  │
│  │ Strong secret key support                  │  │
│  │ CSRF protection ready                      │  │
│  └────────────────────────────────────────────┘  │
│                                                  │
│  Layer 5: Logging & Monitoring                   │
│  ┌────────────────────────────────────────────┐  │
│  │ Comprehensive logging                      │  │
│  │ Error tracking                             │  │
│  │ Security event logging                     │  │
│  │ No sensitive data in logs                  │  │
│  └────────────────────────────────────────────┘  │
│                                                  │
└──────────────────────────────────────────────────┘
```

## Deployment Architecture

```
┌────────────────────────────────────────────────────┐
│           PRODUCTION DEPLOYMENT                    │
├────────────────────────────────────────────────────┤
│                                                    │
│  Internet / Users                                  │
│      │                                             │
│      ▼                                             │
│  ┌─────────────┐                                   │
│  │  Firewall   │                                   │
│  └──────┬──────┘                                   │
│         │                                          │
│         ▼                                          │
│  ┌──────────────────┐                              │
│  │  Nginx/Apache    │  (Reverse Proxy)             │
│  │  (Port 80/443)   │  (Load Balancer)             │
│  └────────┬─────────┘                              │
│           │                                        │
│           ▼                                        │
│  ┌──────────────────────────────────────┐          │
│  │  Gunicorn/Waitress                   │          │
│  │  (WSGI Application Server)           │          │
│  │  ├─ Worker 1                         │          │
│  │  ├─ Worker 2                         │          │
│  │  └─ Worker 3                         │          │
│  └────────┬─────────────────────────────┘          │
│           │                                        │
│           ▼                                        │
│  ┌──────────────────────────────────────┐          │
│  │  Flask Application (app.py)          │          │
│  │  ├─ config.py                        │          │
│  │  ├─ db.py                            │          │
│  │  ├─ utils.py                         │          │
│  │  └─ templates/                       │          │
│  └────────┬────────────────────┬────────┘          │
│           │                    │                   │
│           ▼                    ▼                   │
│  ┌──────────────┐    ┌──────────────────┐          │
│  │   MySQL      │    │  File Storage    │          │
│  │  Database    │    │  (uploads/)      │          │
│  └──────────────┘    └──────────────────┘          │
│                                                    │
└────────────────────────────────────────────────────┘
```

## Development vs Production

```
DEVELOPMENT MODE                PRODUCTION MODE
─────────────────               ─────────────────

FLASK_ENV=development           FLASK_ENV=production
│                               │
├─ Debug: ON                    ├─ Debug: OFF
├─ Auto-reload: ON              ├─ Auto-reload: OFF
├─ Full errors: YES             ├─ User-friendly errors: YES
├─ Console logging: YES         ├─ File logging: YES
├─ Single worker: YES           ├─ Multiple workers: YES
├─ Port: 5000                   ├─ Reverse proxy: Nginx
├─ Local development            ├─ Live server
│                               │
    python app.py                  gunicorn -w 4 app:app
```

---

This diagram set provides a complete visual understanding of your application architecture!
