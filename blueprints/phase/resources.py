import json
import os
import werkzeug
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from blueprints import db, app
from sqlalchemy import desc
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity,
    verify_jwt_in_request,
    jwt_required,
    get_jwt_claims,
)
from blueprints import admin_required

from .model import Phases
from ..module.model import Modules
from ..subject.model import Subjects

bp_phase = Blueprint("phase", __name__)
api = Api(bp_phase)

class PhasesResource(Resource):
    #endpoint for solve CORS
    def option(self, id=None):
        return {"status": "ok"}, 200

    #endpoint for get phases by ID
    @admin_required
    def get(self, id=None):
        #check role admin
        verify_jwt_in_request()
        claims = get_jwt_claims()
        
        if claims["role"] == "super" or claims["role"] == "academic":
            qry_phase = Phases.query.filter_by(status=True).filter_by(id=id).first()

            if qry_phase is not None:
                qry_phase = marshal(qry_phase, Phases.response_fields)

                return qry_phase, 200
            
            return {"status": "Id Phases is not found"}, 404

        else:
            return {"status": "admin isn't at role super admin and academic admin"}, 404

    #endpoint post phase
    @admin_required
    def post(self):
        #check role admin
        verify_jwt_in_request()
        claims = get_jwt_claims()
        
        if claims["role"] == "super":
            parser = reqparse.RequestParser()
            parser.add_argument("name", location="json", required=True)
            parser.add_argument("description", location="json")
            parser.add_argument("status", location="json", type=bool, default=True)
            args = parser.parse_args()

            result = Phases(
                args["name"],
                args["description"],
                args["status"]
            )

            db.session.add(result)
            db.session.commit()

            return marshal(result, Phases.response_fields), 200

        else:
            return {"status": "admin isn't at role super admin"}, 404

    #endpoint for soft delete
    def put(self, id):
        #check id in query or not
        qry_phase = Phases.query.get(id)
        
        if qry_phase is None:
            return {'status': 'Phase is NOT_FOUND'}, 404
        
        #input update status for soft delete
        parser = reqparse.RequestParser()
        parser.add_argument("status", location="json", type=bool)
        args = parser.parse_args()
        
        #change status for soft delete      
        qry_phase.status = args['status']

        db.session.commit()

        return marshal(qry_phase, Phases.response_fields), 200
    
    #endpoint for edit phase
    @admin_required
    def patch(self, id):
        #check role admin
        verify_jwt_in_request()
        claims = get_jwt_claims()
        
        if claims["role"] == "super":
            #check id in query or not
            qry_phase = Phases.query.get(id)
            
            if qry_phase is None:
                return {'status': 'Phase is NOT_FOUND'}, 404
            
            #input update description phase
            parser = reqparse.RequestParser()
            parser.add_argument("description", location="json")
            args = parser.parse_args()
            
            #change description phase     
            if args['description'] is not None:
                qry_phase.description = args['description']

            db.session.commit()

            return marshal(qry_phase, Phases.response_fields), 200

        else:
            return {"status": "admin isn't at role super admin"}, 404

    #Endpoint delete phase by Id
    @admin_required
    def delete(self, id):
        #check role admin
        verify_jwt_in_request()
        claims = get_jwt_claims()
        
        if claims["role"] == "super":
            qry_phase = Phases.query.get(id)

            if qry_phase is not None:
                db.session.delete(qry_phase)
                db.session.commit()

                return {"status": "DELETED SUCCESS"}, 200

            return {"status": "NOT_FOUND"}, 404

        else:
            return {"status": "admin isn't at role super admin"}, 404


class PhasesAll(Resource):
    #endpoint for solve CORS
    def option(self, id=None):
        return {"status": "ok"}, 200

    #endpoint to get all and sort by choice and created_at
    @admin_required
    def get(self):
        #check role admin
        verify_jwt_in_request()
        claims = get_jwt_claims()
        
        if claims["role"] == "super" or claims["role"] == "academic":
            parser = reqparse.RequestParser()
            parser.add_argument('p', type=int, location='args', default=1)
            parser.add_argument('rp', type=int, location='args', default=25)
            parser.add_argument('orderby', location='args', help='invalid status', choices=("id", "created_at"))
            parser.add_argument('sort', location='args', help='invalid status', choices=("asc", "desc"))
            args = parser.parse_args()

            offset = (args['p'] * args['rp']) - args['rp']

            qry_phase = Phases.query

            if args["orderby"] is not None:
                if args['orderby'] == "id":
                    if args["sort"] == "desc":
                        qry_phase = qry_phase.order_by(desc(Phases.id))
                    else:
                        qry_phase = qry_phase.order_by(Phases.id)
                elif args["orderby"] == "created_at":
                    if args["sort"] == "desc":
                        qry_phase = qry_phase.order_by(desc(Phases.created_at))
                    else:
                        qry_phase = qry_phase.order_by(Phases.created_at)

            rows = []
            for row in qry_phase.limit(args['rp']).offset(offset).all():
                if row.status == True:
                    row = marshal(row, Phases.response_fields)
                    rows.append(row)

            return rows, 200

        else:
            return {"status": "admin isn't at role super admin and academic admin"}, 404


class PhaseNestedById(Resource):
    #endpoint for solve CORS
    def option(self, id=None):
        return {"status": "ok"}, 200

    @admin_required
    def get(self, id=None):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        
        if claims["role"] == "super" or claims["role"] == "academic":
            qry_phase = Phases.query.get(id)
            
            if qry_phase is not None:
                phase = marshal(qry_phase, Phases.response_fields)

                if phase["status"] == True:
                    qry_module = Modules.query.filter_by(phase_id=phase["id"]).all()
                    
                    modules = []
                    for module in qry_module:
                        if module.status == True and (module.admin_id == claims["id"] or claims["role"] == "super"):
                            module = marshal(module, Modules.response_fields)
                            qry_subject = Subjects.query.filter_by(module_id=module["id"]).all()
                            
                            subjects = []
                            for subject in qry_subject:
                                if subject.status == True:
                                    subject = marshal(subject, Subjects.response_fields)
                                    subjects.append(subject)

                            module["subject"] = subjects

                            modules.append(module)
                    
                    phase["module"] = modules
                
                return phase, 200

            else:
                return {"status": "phase is not found"}, 404

        else:
            return {"status": "admin isn't at role super admin and academic admin"}, 404


class PhaseNestedAll(Resource):
    #endpoint for solve CORS
    def option(self, id=None):
        return {"status": "ok"}, 200

    @admin_required
    def get(self, id=None):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        
        if claims["role"] == "super" or claims["role"] == "academic":
            parser = reqparse.RequestParser()
            parser.add_argument('p', type=int, location='args', default=1)
            parser.add_argument('rp', type=int, location='args', default=25)
            parser.add_argument('orderby', location='args', help='invalid status', choices=("id", "created_at"))
            parser.add_argument('sort', location='args', help='invalid status', choices=("asc", "desc"))
            args = parser.parse_args()

            offset = (args['p'] * args['rp']) - args['rp']

            qry_phase = Phases.query

            if args["orderby"] is not None:
                if args['orderby'] == "id":
                    if args["sort"] == "desc":
                        qry_phase = qry_phase.order_by(desc(Phases.id))
                    else:
                        qry_phase = qry_phase.order_by(Phases.id)
                elif args["orderby"] == "created_at":
                    if args["sort"] == "desc":
                        qry_phase = qry_phase.order_by(desc(Phases.created_at))
                    else:
                        qry_phase = qry_phase.order_by(Phases.created_at)

            phases = []
            for phase in qry_phase.limit(args['rp']).offset(offset).all():
                if phase.status == True:
                    phase = marshal(phase, Phases.response_fields)

                    qry_module = Modules.query.filter_by(phase_id=phase["id"]).all()
                    modules = []
                    for module in qry_module:
                        if module.status == True and (module.admin_id == claims["id"] or claims["role"] == "super"):
                            module = marshal(module, Modules.response_fields)

                            qry_subject = Subjects.query.filter_by(module_id=module["id"]).all()
                            subjects = []
                            for subject in qry_subject:
                                if subject.status == True:
                                    subject = marshal(subject, Subjects.response_fields)
                                    subjects.append(subject)

                            module["subject"] = subjects

                            modules.append(module)
                    
                    phase["module"] = modules

                    phases.append(phase)
            
            return phases, 200

        else:
            return {"status": "admin isn't at role super admin and academic admin"}, 404


class PhasesAllStatus(Resource):
    #endpoint for solve CORS
    def option(self, id=None):
        return {"status": "ok"}, 200

    #endpoint to get all status of choice 
    @admin_required
    def get(self):
        qry_phase = Phases.query

        rows = []
        for row in qry_phase:
            row = marshal(row, Phases.response_fields)
            rows.append(row)

        if rows == []:
            return {"status": "data not found"}, 404

        return rows, 200


api.add_resource(PhasesAll, "")
api.add_resource(PhasesResource, "", "/<id>")
api.add_resource(PhaseNestedById, "", "/nested/<id>")
api.add_resource(PhaseNestedAll, "", "/nested")
api.add_resource(PhasesAllStatus, "", "/all")