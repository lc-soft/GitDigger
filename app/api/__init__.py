from app import app, csrf
from flask_restful import Api

api = Api(app, decorators=[csrf.exempt])

import issues
import topics
