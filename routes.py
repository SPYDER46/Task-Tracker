from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_required, current_user
from .models import get_tasks, add_task, delete_task

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
def homepage():
    tasks = get_tasks(current_user.team)
    return render_template('index.html', tasks=tasks)

@main_bp.route('/add', methods=['POST'])
@login_required
def add():
    task_data = (
        current_user.team,
        request.form['date'],
        request.form['project_phase'],
        request.form['project'],
        request.form['module'],
        request.form['task'],
        request.form['sub_task'],
        request.form['assigned_to'],
        float(request.form['hours'])
    )
    add_task(task_data)
    flash('Task added successfully!', 'success')
    return redirect(url_for('main.homepage'))

@main_bp.route('/delete/<int:task_id>', methods=['POST'])
@login_required
def delete(task_id):
    delete_task(task_id, current_user.team)
    flash('Task deleted!', 'success')
    return redirect(url_for('main.homepage'))