from flask import Blueprint

job_tracker = Blueprint('job_tracker', __name__)

from . import routes
