"""
Employee Management Application
A Flask-based CRUD application for managing employees
"""
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from config import app_config
from db import db
from utils import (
    validate_input, validate_file_upload, save_uploaded_file, 
    delete_file, validate_nombre, validate_correo
)

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



@app.route('/uploads/<path:nombreFoto>')
def uploads(nombreFoto):
    """Serve uploaded files with security check"""
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], nombreFoto)
    except Exception as e:
        logger.error(f"Error serving file: {e}")
        flash('File not found', 'error')
        return redirect(url_for('index'))


## Sectores
@app.route('/sectores')
def sectores_index():
    """Display list of all sectors"""
    try:
        sql = "SELECT id, descripcion FROM sectores ORDER BY id DESC"
        sectores = db.execute_query(sql)
        
        if sectores is None:
            flash('Error loading sectors', 'error')
            return redirect(url_for('index'))
        
        logger.info(f"Loaded {len(sectores) if sectores else 0} sectors")
        return render_template('sectores/index.html', sectores=sectores)
    except Exception as e:
        logger.error(f"Error loading employees: {e}")
        flash('An error occurred while loading employees', 'error')
        return render_template('empleados/index.html', empleados=[])


@app.route('/sectores/create')
def sectores_create():
    """Show create sector form"""
    return render_template('sectores/sector.html', sector=None)


@app.route('/sectores/store', methods=['POST'])
def sectores_store():
    """Store new sector in database"""
    try:
        raw_id = request.form.get('txtId', '').strip()
        descripcion = request.form.get('txtDescripcion', '').strip()

        if not raw_id or not descripcion:
            flash('Sector ID and description are required', 'error')
            return redirect(url_for('sectores_create'))

        try:
            sector_id = int(raw_id)
        except ValueError:
            flash('Sector ID must be a number', 'error')
            return redirect(url_for('sectores_create'))

        sql = "INSERT INTO sectores (id, descripcion) VALUES (%s, %s)"
        db.execute_update(sql, (sector_id, descripcion))

        flash('Sector added successfully', 'success')
        logger.info(f"Sector added: ID {sector_id}")
        return redirect(url_for('sectores_index'))
    except Exception as e:
        logger.error(f"Error storing sector: {e}")
        flash('An error occurred while adding the sector', 'error')
        return redirect(url_for('sectores_create'))


@app.route('/sectores/edit/<int:id>')
def sectores_edit(id):
    """Show edit sector form"""
    try:
        sql = "SELECT id, descripcion FROM sectores WHERE id = %s"
        result = db.execute_query(sql, (id,))

        if not result:
            flash('Sector not found', 'error')
            return redirect(url_for('sectores_index'))

        sector = result[0]
        return render_template('sectores/sector.html', sector=sector)
    except Exception as e:
        logger.error(f"Error loading sector: {e}")
        flash('Error loading sector details', 'error')
        return redirect(url_for('sectores_index'))


@app.route('/sectores/update/<int:id>', methods=['POST'])
def sectores_update(id):
    """Update sector information"""
    try:
        descripcion = request.form.get('txtDescripcion', '').strip()

        if not descripcion:
            flash('Description is required', 'error')
            return redirect(url_for('sectores_edit', id=id))

        sql = "UPDATE sectores SET descripcion = %s WHERE id = %s"
        db.execute_update(sql, (descripcion, id))

        flash('Sector updated successfully', 'success')
        logger.info(f"Sector updated: ID {id}")
        return redirect(url_for('sectores_index'))
    except Exception as e:
        logger.error(f"Error updating sector: {e}")
        flash('An error occurred while updating the sector', 'error')
        return redirect(url_for('sectores_edit', id=id))


@app.route('/sectores/delete/<int:id>', methods=['POST'])
def sectores_delete(id):
    """Delete sector"""
    try:
        sql = "DELETE FROM sectores WHERE id = %s"
        db.execute_update(sql, (id,))

        flash('Sector deleted successfully', 'success')
        logger.info(f"Sector deleted: ID {id}")
        return redirect(url_for('sectores_index'))
    except Exception as e:
        logger.error(f"Error deleting sector: {e}")
        flash('An error occurred while deleting the sector', 'error')
        return redirect(url_for('sectores_index'))


@app.route('/')
@app.route('/empleados')
def index():
    """Display list of all employees"""
    try:
        sql = "SELECT e.id, nombre, correo, foto," 
        sql += " p.descripcion as perfil_descripcion, "
        sql += " s.descripcion as sector_descripcion "
        sql += " FROM empleados e "
        sql += " join perfiles p on p.id =  e.perfil"
        sql += " join sectores s on s.id =  e.sector"
        sql += " ORDER BY e.id DESC"
        empleados = db.execute_query(sql)
        
        if empleados is None:
            flash('Error loading employees', 'error')
            return redirect(url_for('index'))
        
        logger.info(f"Loaded {len(empleados) if empleados else 0} employees")
        return render_template('empleados/index.html', empleados=empleados)
    except Exception as e:
        logger.error(f"Error loading employees: {e}")
        flash('An error occurred while loading employees', 'error')
        return render_template('empleados/index.html', empleados=[])


@app.route('/create')
def create():
    """Show create employee form"""
    return render_template('empleados/create.html')


@app.route('/store', methods=['POST'])
def store():
    """Store new employee in database"""
    try:
        # Get form data
        nombre = request.form.get('txtNombre', '').strip()
        correo = request.form.get('txtCorreo', '').strip()
        foto = request.files.get('txtFoto')
        
        # Validate input
        valid, errors = validate_input(nombre, correo)
        if not valid:
            for error in errors:
                flash(error, 'error')
            return redirect(url_for('create'))
        
        # Validate and save file
        filename = None
        if foto and foto.filename:
            valid, error = validate_file_upload(foto)
            if not valid:
                flash(error, 'error')
                return redirect(url_for('create'))
            
            filename, error = save_uploaded_file(foto)
            if error:
                flash(f'Error uploading file: {error}', 'error')
                return redirect(url_for('create'))
        else:
            flash('Please select a photo', 'error')
            return redirect(url_for('create'))
        
        # Insert into database
        sql = "INSERT INTO empleados (nombre, correo, foto) VALUES (%s, %s, %s)"
        params = (nombre, correo, filename)
        
        db.execute_update(sql, params)
        flash('Employee added successfully', 'success')
        logger.info(f"Employee added: {nombre}")
        return redirect(url_for('index'))
    
    except Exception as e:
        logger.error(f"Error storing employee: {e}")
        flash('An error occurred while adding the employee', 'error')
        return redirect(url_for('create'))


@app.route('/edit/<int:id>')
def edit(id):
    """Show edit employee form"""
    try:
        sql = "SELECT id, nombre, correo, foto FROM empleados WHERE id = %s"
        result = db.execute_query(sql, (id,))
        
        if not result:
            flash('Employee not found', 'error')
            return redirect(url_for('index'))
        
        empleado = result[0]
        return render_template('empleados/edit.html', empleado=empleado)
    except Exception as e:
        logger.error(f"Error loading employee: {e}")
        flash('Error loading employee details', 'error')
        return redirect(url_for('index'))


@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    """Update employee information"""
    try:
        # Verify employee exists
        sql = "SELECT foto FROM empleados WHERE id = %s"
        result = db.execute_query(sql, (id,))
        
        if not result:
            flash('Employee not found', 'error')
            return redirect(url_for('index'))
        
        old_foto = result[0][0]
        
        # Get form data
        nombre = request.form.get('txtNombre', '').strip()
        correo = request.form.get('txtCorreo', '').strip()
        foto = request.files.get('txtFoto')
        
        # Validate input
        valid, errors = validate_input(nombre, correo)
        if not valid:
            for error in errors:
                flash(error, 'error')
            return redirect(url_for('edit', id=id))
        
        # Handle file upload
        filename = old_foto
        if foto and foto.filename:
            valid, error = validate_file_upload(foto)
            if not valid:
                flash(error, 'error')
                return redirect(url_for('edit', id=id))
            
            filename, error = save_uploaded_file(foto)
            if error:
                flash(f'Error uploading file: {error}', 'error')
                return redirect(url_for('edit', id=id))
            
            # Delete old file
            delete_file(old_foto)
        
        # Update database
        sql = "UPDATE empleados SET nombre = %s, correo = %s, foto = %s WHERE id = %s"
        params = (nombre, correo, filename, id)
        db.execute_update(sql, params)
        
        flash('Employee updated successfully', 'success')
        logger.info(f"Employee updated: ID {id}")
        return redirect(url_for('index'))
    
    except Exception as e:
        logger.error(f"Error updating employee: {e}")
        flash('An error occurred while updating the employee', 'error')
        return redirect(url_for('edit', id=id))


@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    """Delete employee"""
    try:
        # Get employee info
        sql = "SELECT foto FROM empleados WHERE id = %s"
        result = db.execute_query(sql, (id,))
        
        if not result:
            flash('Employee not found', 'error')
            return redirect(url_for('index'))
        
        foto = result[0][0]
        
        # Delete from database
        sql = "DELETE FROM empleados WHERE id = %s"
        db.execute_update(sql, (id,))
        
        # Delete file
        delete_file(foto)
        
        flash('Employee deleted successfully', 'success')
        logger.info(f"Employee deleted: ID {id}")
        return redirect(url_for('index'))
    
    except Exception as e:
        logger.error(f"Error deleting employee: {e}")
        flash('An error occurred while deleting the employee', 'error')
        return redirect(url_for('index'))


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
    return redirect(url_for('index'))


@app.teardown_appcontext
def close_db(error):
    """Close database connection"""
    if db:
        db.close()



if __name__ == '__main__':
    app.run(debug=app_config.DEBUG, host='0.0.0.0', port=5000)
 