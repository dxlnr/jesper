from http import HTTPStatus
from flask import Blueprint

# from db.utils import DatabaseUtils
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

api_blueprint = Blueprint('api_blueprint', __name__)

@api_blueprint.route('/')
def index():
    db_utils = DatabaseUtils()
    session = Session(db_utils.engine)
    session.close()
    return 'Jesper Backend api routes available.'