"""Employees routes."""
import logging
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from db import db
from utils import (
    validate_input, validate_file_upload, save_uploaded_file,
    delete_file
)

logger = logging.getLogger(__name__)

empleados_bp = Blueprint('empleados', __name__)


def load_sectores_perfiles():
    """Load sectores and perfiles lists for form selects."""
    sectores_sql = "SELECT id, descripcion FROM sectores ORDER BY descripcion"
    perfiles_sql = "SELECT id, descripcion FROM perfiles ORDER BY descripcion"
    sectores = db.execute_query(sectores_sql) or []
    perfiles = db.execute_query(perfiles_sql) or []
    return sectores, perfiles


def get_employee_stats():
    """Get employee, sector, and profile statistics."""
    try:
        # Count employees
        empleados_count = db.execute_query("SELECT COUNT(*) FROM empleados")
        count_empleados = empleados_count[0][0] if empleados_count else 0

        # Count sectors
        sectores_count = db.execute_query("SELECT COUNT(*) FROM sectores")
        count_sectores = sectores_count[0][0] if sectores_count else 0

        # Count profiles
        perfiles_count = db.execute_query("SELECT COUNT(*) FROM perfiles")
        count_perfiles = perfiles_count[0][0] if perfiles_count else 0

        return {
            'empleados': count_empleados,
            'sectores': count_sectores,
            'perfiles': count_perfiles
        }
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return {'empleados': 0, 'sectores': 0, 'perfiles': 0}


def parse_sector_perfil(form_data):
    """Parse sector and profile ids from form data."""
    raw_sector = form_data.get('txtSector', '').strip()
    raw_perfil = form_data.get('txtPerfil', '').strip()

    if not raw_sector or not raw_perfil:
        return None, None, 'Sector and profile are required'

    try:
        return int(raw_sector), int(raw_perfil), None
    except ValueError:
        return None, None, 'Invalid sector or profile selection'


@empleados_bp.route('/')
@empleados_bp.route('/empleados')
def index():
    """Display list of all employees."""
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
            return redirect(url_for('empleados.index'))

        logger.info(f"Loaded {len(empleados) if empleados else 0} employees")
        return render_template('empleados/index.html', empleados=empleados)
    except Exception as e:
        logger.error(f"Error loading employees: {e}")
        flash('An error occurred while loading employees', 'error')
        return render_template('empleados/index.html', empleados=[])


@empleados_bp.route('/create')
def create():
    """Show create employee form."""
    try:
        sectores, perfiles = load_sectores_perfiles()

        return render_template(
            'empleados/create.html',
            sectores=sectores,
            perfiles=perfiles
        )
    except Exception as e:
        logger.error(f"Error loading create form data: {e}")
        flash('An error occurred while loading the form', 'error')
        return render_template('empleados/create.html', sectores=[], perfiles=[])


@empleados_bp.route('/api/stats')
def api_get_stats():
    """API endpoint to get employee, sector, and profile statistics."""
    stats = get_employee_stats()
    return jsonify(stats)


@empleados_bp.route('/landing')
def landing():
    """Show landing page."""
    try:
        stats = get_employee_stats()
        return render_template('landing.html', stats=stats)
    except Exception as e:
        logger.error(f"Error loading landing page: {e}")
        return render_template('landing.html', stats={'empleados': 0, 'sectores': 0, 'perfiles': 0})


@empleados_bp.route('/store', methods=['POST'])
def store():
    """Store new employee in database."""
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
            return redirect(url_for('empleados.create'))

        sector_id, perfil_id, error = parse_sector_perfil(request.form)
        if error:
            flash(error, 'error')
            return redirect(url_for('empleados.create'))

        # Validate and save file
        filename = None
        if foto and foto.filename:
            valid, error = validate_file_upload(foto)
            if not valid:
                flash(error, 'error')
                return redirect(url_for('empleados.create'))

            filename, error = save_uploaded_file(foto)
            if error:
                flash(f'Error uploading file: {error}', 'error')
                return redirect(url_for('empleados.create'))
        else:
            flash('Please select a photo', 'error')
            return redirect(url_for('empleados.create'))

        # Insert into database
        sql = "INSERT INTO empleados (nombre, correo, foto, sector, perfil) VALUES (%s, %s, %s, %s, %s)"
        params = (nombre, correo, filename, sector_id, perfil_id)

        db.execute_update(sql, params)
        flash('Employee added successfully', 'success')
        logger.info(f"Employee added: {nombre}")
        return redirect(url_for('empleados.index'))

    except Exception as e:
        logger.error(f"Error storing employee: {e}")
        flash('An error occurred while adding the employee', 'error')
        return redirect(url_for('empleados.create'))


@empleados_bp.route('/edit/<int:id>')
def edit(id):
    """Show edit employee form."""
    try:
        empleado_sql = "SELECT id, nombre, correo, foto, sector, perfil FROM empleados WHERE id = %s"
        result = db.execute_query(empleado_sql, (id,))

        if not result:
            flash('Employee not found', 'error')
            return redirect(url_for('empleados.index'))

        empleado = result[0]
        sectores, perfiles = load_sectores_perfiles()

        return render_template(
            'empleados/edit.html',
            empleado=empleado,
            sectores=sectores,
            perfiles=perfiles
        )
    except Exception as e:
        logger.error(f"Error loading employee: {e}")
        flash('Error loading employee details', 'error')
        return redirect(url_for('empleados.index'))


@empleados_bp.route('/update/<int:id>', methods=['POST'])
def update(id):
    """Update employee information."""
    try:
        # Verify employee exists
        sql = "SELECT foto FROM empleados WHERE id = %s"
        result = db.execute_query(sql, (id,))

        if not result:
            flash('Employee not found', 'error')
            return redirect(url_for('empleados.index'))

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
            return redirect(url_for('empleados.edit', id=id))

        sector_id, perfil_id, error = parse_sector_perfil(request.form)
        if error:
            flash(error, 'error')
            return redirect(url_for('empleados.edit', id=id))

        # Handle file upload
        filename = old_foto
        if foto and foto.filename:
            valid, error = validate_file_upload(foto)
            if not valid:
                flash(error, 'error')
                return redirect(url_for('empleados.edit', id=id))

            filename, error = save_uploaded_file(foto)
            if error:
                flash(f'Error uploading file: {error}', 'error')
                return redirect(url_for('empleados.edit', id=id))

            # Delete old file
            delete_file(old_foto)

        # Update database
        sql = "UPDATE empleados SET nombre = %s, correo = %s, foto = %s, sector = %s, perfil = %s WHERE id = %s"
        params = (nombre, correo, filename, sector_id, perfil_id, id)
        db.execute_update(sql, params)

        flash('Employee updated successfully', 'success')
        logger.info(f"Employee updated: ID {id}")
        return redirect(url_for('empleados.index'))

    except Exception as e:
        logger.error(f"Error updating employee: {e}")
        flash('An error occurred while updating the employee', 'error')
        return redirect(url_for('empleados.edit', id=id))


@empleados_bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    """Delete employee."""
    try:
        # Get employee info
        sql = "SELECT foto FROM empleados WHERE id = %s"
        result = db.execute_query(sql, (id,))

        if not result:
            flash('Employee not found', 'error')
            return redirect(url_for('empleados.index'))

        foto = result[0][0]

        # Delete from database
        sql = "DELETE FROM empleados WHERE id = %s"
        db.execute_update(sql, (id,))

        # Delete file
        delete_file(foto)

        flash('Employee deleted successfully', 'success')
        logger.info(f"Employee deleted: ID {id}")
        return redirect(url_for('empleados.index'))

    except Exception as e:
        logger.error(f"Error deleting employee: {e}")
        flash('An error occurred while deleting the employee', 'error')
        return redirect(url_for('empleados.index'))
