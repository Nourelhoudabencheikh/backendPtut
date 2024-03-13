from apifairy.decorators import other_responses
from flask import Blueprint, abort
from apifairy import authenticate, body, response
from flask import Blueprint, abort, request
from flask_httpauth import HTTPBasicAuth
from api.app import db
from api.models import Patient
from api.schemas import PatientSchema, EmptySchema
from api.auth import token_auth
from api.decorators import paginated_response
import sys

patients = Blueprint('patients', __name__)
patient_schema = PatientSchema()
patients_schema = PatientSchema(many=True)

# Utiliser HTTPBasicAuth pour protéger les endpoints
auth = HTTPBasicAuth()

# Définir les permissions nécessaires pour accéder aux endpoints
# @auth.verify_password
# def verify_password(username, password):
#     patient = Patient.query.filter_by(username=username).first()
#     if patient is None:
#         return False
#     if patient.verify_password(password):
#         return patient
#     return False

# Endpoint pour créer un nouveau patient
@patients.route('/patients', methods=['POST'])
@body(patient_schema)
@authenticate(token_auth)
@response(patient_schema, 201)
def new(args):
    """Créer un nouveau patient"""
    patient = Patient(**args)

    print(patient,file=sys.stderr)
    db.session.add(patient)
    db.session.commit()
    return patient

# Endpoint pour récupérer tous les patients
@patients.route('/patients', methods=['GET'])
@authenticate(token_auth)
@paginated_response(patients_schema)
def all():
    """Récupérer tous les patients"""
    return Patient.select()

# Endpoint pour récupérer un patient par son ID
@patients.route('/patients/<int:id>', methods=['GET'])
@auth.login_required
@response(patient_schema)
@other_responses({404: 'Patient not found'})
def get(id):
    """Récupérer un patient par son ID"""
    return Patient.query.get_or_404(id)

# Endpoint pour mettre à jour un patient
@patients.route('/patients/<int:id>', methods=['PUT'])
@auth.login_required
@response(patient_schema)
def update(id):
    """Mettre à jour un patient"""
    patient = Patient.query.get_or_404(id)
    patient.update(request.get_json())
    db.session.commit()
    return patient

# Endpoint pour supprimer un patient
@patients.route('/patients/<int:id>', methods=['DELETE'])
@auth.login_required
@response(EmptySchema, 204)
@other_responses({404: 'Patient not found'})
def delete(id):
    """Supprimer un patient"""
    patient = Patient.query.get_or_404(id)
    db.session.delete(patient)
    db.session.commit()
    return {}