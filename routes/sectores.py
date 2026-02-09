"""Sectors routes."""
import logging
from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import db

logger = logging.getLogger(__name__)

sectores_bp = Blueprint('sectores', __name__)


@sectores_bp.route('/sectores')
def sectores_index():
    """Display list of all sectors."""
    try:
        sql = "SELECT id, descripcion FROM sectores ORDER BY id DESC"
        sectores = db.execute_query(sql)

        if sectores is None:
            flash('Error loading sectors', 'error')
            return redirect(url_for('empleados.index'))

        logger.info(f"Loaded {len(sectores) if sectores else 0} sectors")
        return render_template('sectores/index.html', sectores=sectores)
    except Exception as e:
        logger.error(f"Error loading employees: {e}")
        flash('An error occurred while loading employees', 'error')
        return render_template('empleados/index.html', empleados=[])


@sectores_bp.route('/sectores/create')
def sectores_create():
    """Show create sector form."""
    return render_template('sectores/sector.html', sector=None)


@sectores_bp.route('/sectores/store', methods=['POST'])
def sectores_store():
    """Store new sector in database."""
    try:
        raw_id = request.form.get('txtId', '').strip()
        descripcion = request.form.get('txtDescripcion', '').strip()

        if not raw_id or not descripcion:
            flash('Sector ID and description are required', 'error')
            return redirect(url_for('sectores.sectores_create'))

        try:
            sector_id = int(raw_id)
        except ValueError:
            flash('Sector ID must be a number', 'error')
            return redirect(url_for('sectores.sectores_create'))

        sql = "INSERT INTO sectores (id, descripcion) VALUES (%s, %s)"
        db.execute_update(sql, (sector_id, descripcion))

        flash('Sector added successfully', 'success')
        logger.info(f"Sector added: ID {sector_id}")
        return redirect(url_for('sectores.sectores_index'))
    except Exception as e:
        logger.error(f"Error storing sector: {e}")
        flash('An error occurred while adding the sector', 'error')
        return redirect(url_for('sectores.sectores_create'))


@sectores_bp.route('/sectores/edit/<int:id>')
def sectores_edit(id):
    """Show edit sector form."""
    try:
        sql = "SELECT id, descripcion FROM sectores WHERE id = %s"
        result = db.execute_query(sql, (id,))

        if not result:
            flash('Sector not found', 'error')
            return redirect(url_for('sectores.sectores_index'))

        sector = result[0]
        return render_template('sectores/sector.html', sector=sector)
    except Exception as e:
        logger.error(f"Error loading sector: {e}")
        flash('Error loading sector details', 'error')
        return redirect(url_for('sectores.sectores_index'))


@sectores_bp.route('/sectores/update/<int:id>', methods=['POST'])
def sectores_update(id):
    """Update sector information."""
    try:
        descripcion = request.form.get('txtDescripcion', '').strip()

        if not descripcion:
            flash('Description is required', 'error')
            return redirect(url_for('sectores.sectores_edit', id=id))

        sql = "UPDATE sectores SET descripcion = %s WHERE id = %s"
        db.execute_update(sql, (descripcion, id))

        flash('Sector updated successfully', 'success')
        logger.info(f"Sector updated: ID {id}")
        return redirect(url_for('sectores.sectores_index'))
    except Exception as e:
        logger.error(f"Error updating sector: {e}")
        flash('An error occurred while updating the sector', 'error')
        return redirect(url_for('sectores.sectores_edit', id=id))


@sectores_bp.route('/sectores/delete/<int:id>', methods=['POST'])
def sectores_delete(id):
    """Delete sector."""
    try:
        sql = "DELETE FROM sectores WHERE id = %s"
        db.execute_update(sql, (id,))

        flash('Sector deleted successfully', 'success')
        logger.info(f"Sector deleted: ID {id}")
        return redirect(url_for('sectores.sectores_index'))
    except Exception as e:
        logger.error(f"Error deleting sector: {e}")
        flash('An error occurred while deleting the sector', 'error')
        return redirect(url_for('sectores.sectores_index'))
