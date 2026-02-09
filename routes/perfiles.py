"""Profiles routes."""
import logging
from flask import Blueprint, render_template, redirect, url_for, flash, request
from db import db

logger = logging.getLogger(__name__)

perfiles_bp = Blueprint('perfiles', __name__)


@perfiles_bp.route('/perfiles')
def perfiles_index():
    """Display list of all profiles."""
    try:
        sql = "SELECT id, descripcion FROM perfiles ORDER BY id DESC"
        perfiles = db.execute_query(sql)

        if perfiles is None:
            flash('Error loading profiles', 'error')
            return redirect(url_for('empleados.index'))

        logger.info(f"Loaded {len(perfiles) if perfiles else 0} profiles")
        return render_template('perfiles/index.html', perfiles=perfiles)
    except Exception as e:
        logger.error(f"Error loading profiles: {e}")
        flash('An error occurred while loading profiles', 'error')
        return render_template('empleados/index.html', empleados=[])


@perfiles_bp.route('/perfiles/create')
def perfiles_create():
    """Show create profile form."""
    return render_template('perfiles/perfil.html', perfil=None)


@perfiles_bp.route('/perfiles/store', methods=['POST'])
def perfiles_store():
    """Store new profile in database."""
    try:
        raw_id = request.form.get('txtId', '').strip()
        descripcion = request.form.get('txtDescripcion', '').strip()

        if not raw_id or not descripcion:
            flash('Profile ID and description are required', 'error')
            return redirect(url_for('perfiles.perfiles_create'))

        try:
            perfil_id = int(raw_id)
        except ValueError:
            flash('Profile ID must be a number', 'error')
            return redirect(url_for('perfiles.perfiles_create'))

        sql = "INSERT INTO perfiles (id, descripcion) VALUES (%s, %s)"
        db.execute_update(sql, (perfil_id, descripcion))

        flash('Profile added successfully', 'success')
        logger.info(f"Profile added: ID {perfil_id}")
        return redirect(url_for('perfiles.perfiles_index'))
    except Exception as e:
        logger.error(f"Error storing profile: {e}")
        flash('An error occurred while adding the profile', 'error')
        return redirect(url_for('perfiles.perfiles_create'))


@perfiles_bp.route('/perfiles/edit/<int:id>')
def perfiles_edit(id):
    """Show edit profile form."""
    try:
        sql = "SELECT id, descripcion FROM perfiles WHERE id = %s"
        result = db.execute_query(sql, (id,))

        if not result:
            flash('Profile not found', 'error')
            return redirect(url_for('perfiles.perfiles_index'))

        perfil = result[0]
        return render_template('perfiles/perfil.html', perfil=perfil)
    except Exception as e:
        logger.error(f"Error loading profile: {e}")
        flash('Error loading profile details', 'error')
        return redirect(url_for('perfiles.perfiles_index'))


@perfiles_bp.route('/perfiles/update/<int:id>', methods=['POST'])
def perfiles_update(id):
    """Update profile information."""
    try:
        descripcion = request.form.get('txtDescripcion', '').strip()

        if not descripcion:
            flash('Description is required', 'error')
            return redirect(url_for('perfiles.perfiles_edit', id=id))

        sql = "UPDATE perfiles SET descripcion = %s WHERE id = %s"
        db.execute_update(sql, (descripcion, id))

        flash('Profile updated successfully', 'success')
        logger.info(f"Profile updated: ID {id}")
        return redirect(url_for('perfiles.perfiles_index'))
    except Exception as e:
        logger.error(f"Error updating profile: {e}")
        flash('An error occurred while updating the profile', 'error')
        return redirect(url_for('perfiles.perfiles_edit', id=id))


@perfiles_bp.route('/perfiles/delete/<int:id>', methods=['POST'])
def perfiles_delete(id):
    """Delete profile."""
    try:
        sql = "DELETE FROM perfiles WHERE id = %s"
        db.execute_update(sql, (id,))

        flash('Profile deleted successfully', 'success')
        logger.info(f"Profile deleted: ID {id}")
        return redirect(url_for('perfiles.perfiles_index'))
    except Exception as e:
        logger.error(f"Error deleting profile: {e}")
        flash('An error occurred while deleting the profile', 'error')
        return redirect(url_for('perfiles.perfiles_index'))
