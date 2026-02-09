# Production Deployment Checklist ✅

## Pre-Deployment Testing

### Functionality Tests
- [ ] Test employee list display
- [ ] Test add new employee
  - [ ] Valid form submission
  - [ ] Invalid name (too short)
  - [ ] Invalid email (wrong format)
  - [ ] Missing photo
  - [ ] Oversized photo
  - [ ] Wrong file format
- [ ] Test edit employee
  - [ ] Update name and email
  - [ ] Update photo
  - [ ] Keep existing photo
- [ ] Test delete employee
  - [ ] Confirm deletion works
  - [ ] Photo is deleted
  - [ ] Database is cleaned
- [ ] Test navigation
  - [ ] All links work
  - [ ] Mobile menu works

### Browser Compatibility
- [ ] Test on Chrome
- [ ] Test on Firefox
- [ ] Test on Safari
- [ ] Test on Edge
- [ ] Test on mobile browsers

### Security Testing
- [ ] Try SQL injection attacks
- [ ] Try file upload exploits
- [ ] Try path traversal attacks
- [ ] Check credentials not exposed
- [ ] Verify no debug info in errors
- [ ] Check logs don't expose sensitive data

### Performance Testing
- [ ] Page load time < 2 seconds
- [ ] Image optimization
- [ ] Database query efficiency
- [ ] Memory usage acceptable
- [ ] CPU usage reasonable

---

## Server Preparation

### System Requirements
- [ ] Python 3.7+ installed
- [ ] MySQL 5.7+ running
- [ ] 1GB RAM minimum
- [ ] 1GB free disk space
- [ ] Modern Linux server or Windows Server

### Server Setup
- [ ] SSH access configured
- [ ] Firewall rules set
- [ ] MySQL root password changed
- [ ] Python virtual environment ready
- [ ] Git installed (for version control)

### Create Production Database
```sql
-- Connect to MySQL
mysql -u root -p

-- Create database
CREATE DATABASE pythonemp;
USE pythonemp;

-- Create table
CREATE TABLE empleados (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(120) NOT NULL,
    foto VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create backup user (optional)
CREATE USER 'empapp'@'localhost' IDENTIFIED BY 'strong_password_here';
GRANT ALL PRIVILEGES ON pythonemp.* TO 'empapp'@'localhost';
FLUSH PRIVILEGES;
```

---

## Application Configuration

### Environment Variables
```bash
# Copy .env.example to .env
cp .env.example .env

# Edit .env with production values
nano .env
```

**Production .env values:**
```env
FLASK_ENV=production
SECRET_KEY=<generate-strong-key>  # Use: python -c "import secrets; print(secrets.token_hex(32))"
MYSQL_HOST=localhost
MYSQL_USER=empapp
MYSQL_PASSWORD=strong_password_here
MYSQL_DB=pythonemp
UPLOAD_FOLDER=/var/www/empapp/uploads
MAX_FILE_SIZE=5242880
```

### Generate Strong Secret Key
```bash
python -c "import secrets; print(secrets.token_hex(32))"
# Copy output to SECRET_KEY in .env
```

### File Permissions
```bash
# Set proper permissions
chmod 700 /var/www/empapp
chmod 600 /var/www/empapp/.env
chmod 755 /var/www/empapp/uploads
chmod 755 /var/www/empapp/templates
chmod 755 /var/www/empapp/templates/empleados
```

---

## Dependencies & Installation

### Install Python Packages
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
pip list
```

### Install Production Server
```bash
# Install Gunicorn (recommended)
pip install gunicorn

# Or install Waitress
pip install waitress
```

### Update Requirements
```bash
pip freeze > requirements.txt
```

---

## Web Server Configuration

### Using Nginx (Recommended)

**Create `/etc/nginx/sites-available/empapp`:**
```nginx
upstream empapp_backend {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    client_max_body_size 10M;

    location / {
        proxy_pass http://empapp_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /uploads {
        alias /var/www/empapp/uploads;
        expires 7d;
    }

    location /static {
        alias /var/www/empapp/static;
        expires 30d;
    }
}
```

**Enable the site:**
```bash
sudo ln -s /etc/nginx/sites-available/empapp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Using Apache (Alternative)

**Create `/etc/apache2/sites-available/empapp.conf`:**
```apache
<VirtualHost *:80>
    ServerName your-domain.com
    ServerAlias www.your-domain.com

    ProxyPreserveHost On
    ProxyPass / http://127.0.0.1:8000/
    ProxyPassReverse / http://127.0.0.1:8000/

    <Directory /var/www/empapp/uploads>
        Require all granted
    </Directory>

    ErrorLog ${APACHE_LOG_DIR}/empapp-error.log
    CustomLog ${APACHE_LOG_DIR}/empapp-access.log combined
</VirtualHost>
```

**Enable:**
```bash
sudo a2enmod proxy
sudo a2enmod proxy_http
sudo a2ensite empapp
sudo apache2ctl configtest
sudo systemctl restart apache2
```

---

## SSL/TLS (HTTPS)

### Using Let's Encrypt (Free)

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Generate certificate
sudo certbot certonly --nginx -d your-domain.com -d www.your-domain.com

# Auto-renew setup
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer

# Update Nginx to use SSL
# Update server_name and add SSL configuration
```

### Update Nginx for SSL
```nginx
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name your-domain.com www.your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # ... rest of configuration
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    listen [::]:80;
    server_name your-domain.com www.your-domain.com;
    return 301 https://$server_name$request_uri;
}
```

---

## Application Server Startup

### Using Gunicorn

**Create `/etc/systemd/system/empapp.service`:**
```ini
[Unit]
Description=Employee Management App
After=network.target mysql.service

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/empapp
Environment="PATH=/var/www/empapp/venv/bin"
ExecStart=/var/www/empapp/venv/bin/gunicorn \
    --workers 4 \
    --worker-class sync \
    --bind 127.0.0.1:8000 \
    --timeout 60 \
    --access-logfile /var/log/empapp/access.log \
    --error-logfile /var/log/empapp/error.log \
    app:app

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Enable and start:**
```bash
sudo mkdir -p /var/log/empapp
sudo chown www-data:www-data /var/log/empapp
sudo systemctl daemon-reload
sudo systemctl enable empapp.service
sudo systemctl start empapp.service
sudo systemctl status empapp.service
```

### Using Waitress

**Create `/var/www/empapp/serve.py`:**
```python
from waitress import serve
from app import app

if __name__ == '__main__':
    serve(app, host='127.0.0.1', port=8000, threads=4)
```

**Run:**
```bash
python serve.py
```

---

## Logging & Monitoring

### Application Logs
```bash
# View real-time logs
sudo journalctl -u empapp.service -f

# View Nginx logs
sudo tail -f /var/log/nginx/empapp-error.log
sudo tail -f /var/log/nginx/empapp-access.log
```

### Set Up Logging
Create `/var/www/empapp/logging_config.py`:
```python
import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    handler = RotatingFileHandler(
        '/var/log/empapp/application.log',
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    return handler
```

### System Monitoring
```bash
# Check resource usage
top
free -h
df -h

# Check services
sudo systemctl status empapp.service
sudo systemctl status mysql.service
sudo systemctl status nginx.service
```

---

## Database Backup

### Automated Daily Backup
```bash
# Create backup script: /usr/local/bin/backup-empapp.sh
#!/bin/bash
BACKUP_DIR="/backups/empapp"
DATE=$(date +%Y%m%d_%H%M%S)
mysqldump -u empapp -p'password' pythonemp > \
  "${BACKUP_DIR}/pythonemp_${DATE}.sql"

# Compress
gzip "${BACKUP_DIR}/pythonemp_${DATE}.sql"

# Keep only last 30 days
find "${BACKUP_DIR}" -name "*.sql.gz" -mtime +30 -delete
```

**Add to crontab:**
```bash
sudo crontab -e

# Add:
0 2 * * * /usr/local/bin/backup-empapp.sh
```

### Manual Backup
```bash
# Export database
mysqldump -u empapp -p pythonemp > backup.sql

# Import backup
mysql -u empapp -p pythonemp < backup.sql
```

---

## Security Hardening

### MySQL Security
```bash
# Remove default user
mysql -u root -p
DROP USER ''@'localhost';
DROP USER ''@'hostname';
DROP DATABASE test;
FLUSH PRIVILEGES;
```

### File Permissions
```bash
# Restrict web root
sudo chmod 755 /var/www/empapp
sudo chmod 644 /var/www/empapp/*.py
sudo chmod 644 /var/www/empapp/.env
sudo chmod 755 /var/www/empapp/templates
sudo chmod 755 /var/www/empapp/uploads
```

### Firewall Rules
```bash
# For UFW (Ubuntu)
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw enable
```

---

## Final Checks

### Pre-Launch Verification
- [ ] All tests pass
- [ ] Secret key changed
- [ ] Database configured
- [ ] File permissions set
- [ ] SSL certificate installed
- [ ] Nginx/Apache running
- [ ] Application server running
- [ ] Database backups configured
- [ ] Monitoring active
- [ ] Logs configured
- [ ] Firewall configured
- [ ] Domain pointing to server
- [ ] Email notifications ready (optional)

### Launch Checklist
- [ ] Announce launch
- [ ] Monitor logs closely
- [ ] Test all features once more
- [ ] Have rollback plan ready
- [ ] Document deployment
- [ ] Train users (if needed)
- [ ] Set up support process
- [ ] Monitor performance
- [ ] Check error logs daily

---

## Rollback Plan

If something goes wrong:

```bash
# 1. Stop application
sudo systemctl stop empapp.service

# 2. Restore from backup
mysql -u empapp -p pythonemp < backup_latest.sql

# 3. Check git history
git log
git checkout <previous-commit>

# 4. Restart
sudo systemctl start empapp.service

# 5. Verify
curl http://localhost:5000
```

---

## Post-Deployment

### Regular Maintenance
- [ ] Weekly: Check logs
- [ ] Weekly: Monitor performance
- [ ] Monthly: Update dependencies
- [ ] Monthly: Backup verification
- [ ] Quarterly: Security audit
- [ ] Yearly: Full system review

### Update Dependencies
```bash
pip list --outdated
pip install --upgrade package-name
pip freeze > requirements.txt
# Test thoroughly
# Deploy updates
```

---

## Contact & Support

- **Admin**: your-email@example.com
- **Support**: support@example.com
- **Emergency**: emergency@example.com

---

**✅ Deployment Ready!**

Once all checkboxes are complete, your application is production-ready.

**Last Updated**: February 2, 2026
**Version**: 2.0
