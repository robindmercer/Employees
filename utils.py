"""
Validation and utility functions
"""
import os
import re
from datetime import datetime
from config import app_config
import logging

logger = logging.getLogger(__name__)


def is_allowed_file(filename):
    """Check if file extension is allowed"""
    if '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in app_config.ALLOWED_EXTENSIONS


def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_nombre(nombre):
    """Validate employee name"""
    if not nombre or len(nombre.strip()) == 0:
        return False, "Name cannot be empty"
    if len(nombre.strip()) < 2:
        return False, "Name must be at least 2 characters"
    if len(nombre.strip()) > 100:
        return False, "Name cannot exceed 100 characters"
    return True, None


def validate_correo(correo):
    """Validate email"""
    if not correo or len(correo.strip()) == 0:
        return False, "Email cannot be empty"
    if not validate_email(correo):
        return False, "Invalid email format"
    if len(correo.strip()) > 120:
        return False, "Email cannot exceed 120 characters"
    return True, None


def validate_file_upload(file):
    """Validate uploaded file"""
    if not file or file.filename == '':
        return False, "No file selected"
    
    if not is_allowed_file(file.filename):
        allowed = ', '.join(app_config.ALLOWED_EXTENSIONS)
        return False, f"File type not allowed. Allowed: {allowed}"
    
    # Check file size
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    
    if file_size > app_config.MAX_FILE_SIZE:
        max_size_mb = app_config.MAX_FILE_SIZE / (1024 * 1024)
        return False, f"File size exceeds {max_size_mb}MB limit"
    
    return True, None


def save_uploaded_file(file):
    """Save uploaded file with unique name"""
    try:
        if not is_allowed_file(file.filename):
            return None, "Invalid file type"
        
        # Generate unique filename
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")
        original_name = file.filename.rsplit('.', 1)[0]
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{timestamp}_{original_name}.{ext}"
        
        filepath = os.path.join(app_config.UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        logger.info(f"File saved: {filename}")
        return filename, None
    except Exception as e:
        logger.error(f"Error saving file: {e}")
        return None, str(e)


def delete_file(filename):
    """Delete uploaded file"""
    try:
        if not filename:
            return True, None
        
        filepath = os.path.join(app_config.UPLOAD_FOLDER, filename)
        
        # Security check: ensure file is in uploads folder
        real_path = os.path.realpath(filepath)
        upload_path = os.path.realpath(app_config.UPLOAD_FOLDER)
        
        if not real_path.startswith(upload_path):
            logger.warning(f"Path traversal attempt detected: {filepath}")
            return False, "Invalid file path"
        
        if os.path.exists(filepath):
            os.remove(filepath)
            logger.info(f"File deleted: {filename}")
            return True, None
        return True, None
    except Exception as e:
        logger.error(f"Error deleting file: {e}")
        return False, str(e)


def validate_input(nombre, correo):
    """Validate all input fields"""
    errors = []
    
    valid, error = validate_nombre(nombre)
    if not valid:
        errors.append(error)
    
    valid, error = validate_correo(correo)
    if not valid:
        errors.append(error)
    
    return len(errors) == 0, errors
