from flask import render_template, current_app
from . import core

@core.route('/')
def index():
    """Homepage that lists all projects."""
    return render_template('core/index.html')
