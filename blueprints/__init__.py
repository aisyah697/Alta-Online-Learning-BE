import json, config, os
from flask import Flask, request
from functools import wraps

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims
from flask_script import Manager
from flask_cors import CORS

app = Flask(__name__)
CORS(
    app,
    origins="*",
    allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
    supports_credentials=True,
    intercept_exceptions=False,
)

if os.environ.get("FLASK_ENV", "Production") == "Production":
    app.config.from_object(config.ProductionConfig)
elif os.environ.get("FLASK_ENV", "Production") == "Testing":
    app.config.from_object(config.TestingConfig)
else:
    app.config.from_object(config.DevelopmentConfig)

jwt = JWTManager(app)

def mentee(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['status'] != "admin":
            return {'status': 'FORBIDDEN', 'message': 'Internal Only'}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper

def admin(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['status'] != "pelapak":
            return {'status': 'FORBIDDEN', 'message': 'Internal Only'}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command("db", MigrateCommand)

@app.before_request
def before_request():
    path = request.path.split('/')
    if request.method == "GET" and path[1] == "img" : 
        return send_from_directory("."+app.config['UPLOAD_MEDIA_AVATAR'], path[2]), 200

#solve cors because in cors used method options in early
@app.before_request
def before_request():
    if request.method != 'OPTIONS':  # <-- required
        pass
    else :
        return {}, 200, {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': 'POST, PUT, GET, DELETE, PATCH', 'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept, Authorization'}

@app.after_request
def after_request(response):
    try:
        requestData = request.get_json()
    except Exception as e:
        requestData = request.args.to_dict()
    if response.status_code == 200:
        app.logger.warning(
            "REQUEST_LOG\t%s",
            json.dumps(
                {
                    "method": request.method,
                    "code": response.status,
                    "uri": request.full_path,
                    "request": requestData,
                    "response": json.loads(response.data.decode("utf-8")),
                }
            ),
        )
    else:
        app.logger.error(
            "REQUEST_LOG\t%s",
            json.dumps(
                {
                    "method": request.method,
                    "code": response.status,
                    "uri": request.full_path,
                    "request": requestData,
                    "response": json.loads(response.data.decode("utf-8")),
                }
            ),
        )
    return response


from blueprints.admin.resources import bp_admin
from blueprints.mentee.resources import bp_mentee
from blueprints.auth.resources import bp_auth
from blueprints.question_altatest.resources import bp_question_altatest
from blueprints.choice_altatest.resources import bp_choice_altatest
from blueprints.altatest.resources import bp_altatest
from blueprints.history_altatest.resources import bp_history_altatest

app.register_blueprint(bp_admin, url_prefix="/admin")
app.register_blueprint(bp_mentee, url_prefix="/mentee")
app.register_blueprint(bp_auth, url_prefix="/auth")
app.register_blueprint(bp_question_altatest, url_prefix="/questionaltatest")
app.register_blueprint(bp_choice_altatest, url_prefix="/choicealtatest")
app.register_blueprint(bp_altatest, url_prefix="/altatest")
app.register_blueprint(bp_history_altatest, url_prefix="/historyaltatest")

db.create_all()