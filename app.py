"""
Employee Management Application
A Flask-based CRUD application for managing employees
"""
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from config import app_config
from db import db
from routes.empleados import empleados_bp
from routes.perfiles import perfiles_bp
from routes.sectores import sectores_bp

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = app_config.SECRET_KEY
app.config['UPLOAD_FOLDER'] = app_config.UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = app_config.MAX_FILE_SIZE

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app.register_blueprint(empleados_bp)
app.register_blueprint(perfiles_bp)
app.register_blueprint(sectores_bp)

@app.route('/uploads/<path:nombreFoto>')
def uploads(nombreFoto):
    """Serve uploaded files with security check"""
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], nombreFoto)
    except Exception as e:
        logger.error(f"Error serving file: {e}")
        flash('File not found', 'error')
        return redirect(url_for('empleados.index'))


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    logger.warning(f"404 error: {request.url}")
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    logger.error(f"500 error: {error}")
    flash('An internal server error occurred', 'error')
    return redirect(url_for('empleados.index'))


@app.teardown_appcontext
def close_db(error):
    """Close database connection"""
    if db:
        db.close()



if __name__ == '__main__':
    app.run(debug=app_config.DEBUG, host='0.0.0.0', port=5000)
 