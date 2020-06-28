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

@app.route('/')
def hello():
    return {'status': 'Thanks Ajay, Yopi, Aisyah ----- Semangat :)'}, 200

def mentee_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['status'] != "mentee":
            return {'status': 'FORBIDDEN', 'message': 'Mentee Only'}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['status'] != "admin":
            return {'status': 'FORBIDDEN', 'message': 'Admin Only'}, 403
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
from blueprints.phase.resources import bp_phase
from blueprints.module.resources import bp_module
from blueprints.review_module.resources import bp_review_module
from blueprints.requirement_module.resources import bp_requirement_module
from blueprints.subject.resources import bp_subject
from blueprints.file_subject.resources import bp_file_subject
from blueprints.exam.resources import bp_exam
from blueprints.livecode.resources import bp_livecode
from blueprints.quiz.resources import bp_quiz
from blueprints.question_quiz.resources import bp_question_quiz
from blueprints.choice_quiz.resources import bp_choice_quiz
from blueprints.history_subject.resources import bp_history_subject
from blueprints.history_exam.resources import bp_history_exam
from blueprints.history_module.resources import bp_history_module
from blueprints.history_phase.resources import bp_history_phase

app.register_blueprint(bp_admin, url_prefix="/admin")
app.register_blueprint(bp_mentee, url_prefix="/mentee")
app.register_blueprint(bp_auth, url_prefix="/auth")
app.register_blueprint(bp_question_altatest, url_prefix="/questionaltatest")
app.register_blueprint(bp_choice_altatest, url_prefix="/choicealtatest")
app.register_blueprint(bp_altatest, url_prefix="/altatest")
app.register_blueprint(bp_history_altatest, url_prefix="/historyaltatest")
app.register_blueprint(bp_phase, url_prefix="/phase")
app.register_blueprint(bp_module, url_prefix="/module")
app.register_blueprint(bp_review_module, url_prefix="/reviewmodule")
app.register_blueprint(bp_requirement_module, url_prefix="/requirementmodule")
app.register_blueprint(bp_subject, url_prefix="/subject")
app.register_blueprint(bp_file_subject, url_prefix="/filesubject")
app.register_blueprint(bp_exam, url_prefix="/exam")
app.register_blueprint(bp_livecode, url_prefix="/livecode")
app.register_blueprint(bp_quiz, url_prefix="/quiz")
app.register_blueprint(bp_question_quiz, url_prefix="/questionquiz")
app.register_blueprint(bp_choice_quiz, url_prefix="/choicequiz")
app.register_blueprint(bp_history_subject, url_prefix="/historysubject")
app.register_blueprint(bp_history_exam, url_prefix="/historyexam")
app.register_blueprint(bp_history_module, url_prefix="/historymodule")
app.register_blueprint(bp_history_phase, url_prefix="/historyphase")

db.create_all()
