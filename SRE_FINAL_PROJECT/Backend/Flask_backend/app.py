from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from random import choice
from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy import inspect
from sqlalchemy.sql import text
import os
import pandas as pd
from sentence_transformers import SentenceTransformer, util
import torch
from dotenv import load_dotenv
import logging
from prometheus_flask_exporter import PrometheusMetrics

# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
metrics = PrometheusMetrics(app)


# Load environment variables
load_dotenv()

# Paths relative to Flask_backend/
DB_PATH = os.getenv("DB_PATH", os.path.join(os.path.dirname(__file__), "../Database/law_enforcement.db"))
DATASET_PATH = os.getenv("DATASET_PATH", os.path.join(os.path.dirname(__file__), "../Dataset/ipc_sections_updated.csv"))
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", os.path.join(os.path.dirname(__file__), "Uploads/Evidence"))
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)

class ResourceLoader:
    _df = None
    _embeddings = None
    _model = None

    @staticmethod
    def get_df():
        if ResourceLoader._df is None:
            logger.info("Loading dataset...")
            if not os.path.exists(DATASET_PATH):
                raise FileNotFoundError(f"Dataset file not found at: {DATASET_PATH}")
            ResourceLoader._df = pd.read_csv(DATASET_PATH)
            logger.info("Dataset loaded successfully!")
        return ResourceLoader._df

    @staticmethod
    def get_embeddings():
        if ResourceLoader._embeddings is None:
            embeddings_path = os.path.join(os.path.dirname(__file__), "embeddings.pt")
            if not os.path.exists(embeddings_path):
                raise FileNotFoundError(f"Embeddings file not found at: {embeddings_path}. Please generate it beforehand.")
            logger.info("Loading precomputed embeddings...")
            ResourceLoader._embeddings = torch.load(embeddings_path)
            logger.info("Precomputed embeddings loaded!")
        return ResourceLoader._embeddings

    @staticmethod
    def get_model():
        if ResourceLoader._model is None:
            logger.info("Loading NLP model from cache...")
            model_path = os.getenv("SENTENCE_TRANSFORMERS_HOME", "/app/model")

            if not os.path.isdir(model_path) or len(os.listdir(model_path)) == 0:
                logger.error(f"Pre-cached model not found at: {model_path}. Falling back to download.")
                ResourceLoader._model = SentenceTransformer("all-MiniLM-L6-v2", device='cpu')
            else:
                ResourceLoader._model = SentenceTransformer(model_path, device='cpu')
                logger.info("NLP model loaded from cache successfully!")

            logger.info("NLP model initialized!")
        return ResourceLoader._model

# Allowed file extensions for evidence
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Models
class Evidence(db.Model):
    __tablename__ = 'evidence'
    evidence_id = db.Column(db.Integer, primary_key=True)
    complaint_id = db.Column(db.Integer, nullable=False)
    police_id = db.Column(db.Integer, db.ForeignKey('police.badge_id'), nullable=True)
    lawyer_id = db.Column(db.String(20), db.ForeignKey('lawyers.lawyer_id'), nullable=True)
    submitter_type = db.Column(db.String(10), nullable=False, default='police')
    file_path = db.Column(db.String(200), nullable=False)
    upload_date = db.Column(db.DateTime, default=db.func.current_timestamp())

class Account(db.Model):
    __tablename__ = 'accounts'
    account_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=True)
    phoneno = db.Column(db.String(15), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    civilian = db.relationship('Civilian', backref='account', uselist=False)
    lawyer = db.relationship('Lawyer', backref='account', uselist=False)
    police = db.relationship('Police', backref='account', uselist=False)

class Civilian(db.Model):
    __tablename__ = 'civilians'
    civilian_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.account_id'), nullable=False)
    cases = db.relationship('Case', backref='civilian')

class Lawyer(db.Model):
    __tablename__ = 'lawyers'
    lawyer_id = db.Column(db.String(20), primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.account_id'), nullable=False)
    case = db.relationship('Case', backref='lawyer', uselist=False)
    court_location_id = db.Column(db.Integer, db.ForeignKey('court_locations.court_id'))

class Police(db.Model):
    __tablename__ = 'police'
    badge_id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.account_id'), nullable=False)
    police_station_id = db.Column(db.Integer, db.ForeignKey('police_stations.ps_id'))
    case_assignments = db.relationship('CaseAssign', backref='police')
    case_solved = db.relationship('CaseSolved', backref='police')

class LawyerInfo(db.Model):
    __tablename__ = 'lawyer_info'
    info_id = db.Column(db.Integer, primary_key=True)
    bar_id = db.Column(db.String(20), db.ForeignKey('lawyers.lawyer_id'), nullable=False)
    branch_name = db.Column(db.String(100))
    state = db.Column(db.String(100))
    court_location = db.Column(db.String(100))
    judiciary = db.Column(db.String(100))
    judiciary_id = db.Column(db.String(50))
    lawyer = db.relationship('Lawyer', backref='info', uselist=False)

class PoliceInfo(db.Model):
    __tablename__ = 'police_station_info'
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(100), nullable=False)
    pin_code = db.Column(db.Integer, nullable=False)
    station_number = db.Column(db.Integer, nullable=False)
    station_location = db.Column(db.String(200), nullable=False)
    police_id = db.Column(db.String(20), nullable=False)

class Case(db.Model):
    __tablename__ = 'cases'
    case_id = db.Column(db.Integer, db.ForeignKey('incidents.incident_id'), primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    civilian_id = db.Column(db.Integer, db.ForeignKey('civilians.civilian_id'))
    lawyer_id = db.Column(db.String(20), db.ForeignKey('lawyers.lawyer_id'))

class CaseAssign(db.Model):
    __tablename__ = 'case_assign'
    assign_id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.case_id'))
    police_id = db.Column(db.String(20), db.ForeignKey('police.badge_id'))

class CaseSolved(db.Model):
    __tablename__ = 'case_solved'
    solved_id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.case_id'))
    police_id = db.Column(db.String(20), db.ForeignKey('police.badge_id'))

class PoliceStation(db.Model):
    __tablename__ = 'police_stations'
    ps_id = db.Column(db.Integer, primary_key=True)
    station_name = db.Column(db.String(100), nullable=False)
    police = db.relationship('Police', backref='station', uselist=False)
    master_id = db.Column(db.Integer, db.ForeignKey('police_master.pm_id'))

class PoliceMaster(db.Model):
    __tablename__ = 'police_master'
    pm_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    stations = db.relationship('PoliceStation', backref='master')

class CourtLocation(db.Model):
    __tablename__ = 'court_locations'
    court_id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    master_id = db.Column(db.Integer, db.ForeignKey('lawyer_master.lm_id'))
    lawyers = db.relationship('Lawyer', backref='court_location')

class LawyerMaster(db.Model):
    __tablename__ = 'lawyer_master'
    lm_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    courts = db.relationship('CourtLocation', backref='master')

class Incident(db.Model):
    __tablename__ = 'incidents'
    incident_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(15))
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    incident_date = db.Column(db.String(20), nullable=False)
    timestamp = db.Column(db.String(50))

class Support(db.Model):
    __tablename__ = 'support'
    support_id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.account_id'), nullable=True)

# Routes
@app.route('/api/evidence', methods=['POST'])
def submit_evidence():
    if 'evidenceFile' not in request.files:
        return jsonify({'message': 'No file part in the request'}), 400
    
    file = request.files['evidenceFile']
    complaint_id = request.form.get('complaintId')
    submitter_id = request.form.get('submitterId')
    submitter_type = request.form.get('submitterType')

    if not all([complaint_id, submitter_id, submitter_type, file]):
        return jsonify({'message': 'Complaint ID, Submitter ID, Submitter Type, and evidence file are required'}), 400
    
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'message': 'File type not allowed. Allowed types: png, jpg, jpeg, pdf, txt'}), 400

    try:
        complaint_id = int(complaint_id)
        
        if submitter_type == 'police':
            police_id = int(submitter_id)
            police = db.session.get(Police, police_id)
            if not police:
                return jsonify({'message': 'Invalid Police ID'}), 404
            case_assignment = CaseAssign.query.filter_by(case_id=complaint_id, police_id=police_id).first()
            if not case_assignment:
                return jsonify({'message': 'This case is not assigned to you'}), 403
            lawyer_id = None
        elif submitter_type == 'lawyer':
            lawyer_id = submitter_id
            lawyer = db.session.get(Lawyer, lawyer_id)
            if not lawyer:
                return jsonify({'message': 'Invalid Lawyer ID'}), 404
            case = Case.query.filter_by(case_id=complaint_id, lawyer_id=lawyer_id).first()
            if not case:
                return jsonify({'message': 'This case is not assigned to you'}), 403
            police_id = None
        else:
            return jsonify({'message': 'Invalid submitter type'}), 400

        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        evidence = Evidence(
            complaint_id=complaint_id,
            police_id=police_id,
            lawyer_id=lawyer_id,
            submitter_type=submitter_type,
            file_path=file_path
        )
        db.session.add(evidence)
        db.session.commit()

        return jsonify({
            'message': 'Evidence submitted successfully',
            'evidence': {
                'evidence_id': evidence.evidence_id,
                'complaint_id': evidence.complaint_id,
                'police_id': evidence.police_id,
                'lawyer_id': evidence.lawyer_id,
                'submitter_type': evidence.submitter_type,
                'file_path': evidence.file_path,
                'upload_date': evidence.upload_date.isoformat(),
                'details': f"File: {filename}, Case ID: {evidence.complaint_id}, Submitted by: {submitter_type.capitalize()}"
            }
        }), 201

    except ValueError:
        return jsonify({'message': 'Complaint ID must be numeric'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error submitting evidence: {str(e)}'}), 500

@app.route('/api/evidence/case/<int:case_id>', methods=['GET'])
def get_evidence_by_case(case_id):
    try:
        evidence_list = Evidence.query.filter_by(complaint_id=case_id).all()
        evidence_data = [{
            'evidence_id': evidence.evidence_id,
            'complaint_id': evidence.complaint_id,
            'police_id': evidence.police_id,
            'lawyer_id': evidence.lawyer_id,
            'submitter_type': evidence.submitter_type,
            'file_path': evidence.file_path,
            'upload_date': evidence.upload_date.isoformat(),
            'details': f"File: {os.path.basename(evidence.file_path)}, Case ID: {evidence.complaint_id}, Submitted by: {evidence.submitter_type.capitalize()}"
        } for evidence in evidence_list]
        return jsonify(evidence_data), 200
    except Exception as e:
        return jsonify({'message': f'Error fetching evidence: {str(e)}'}), 500

@app.route('/api/lawyer/cases/<string:lawyer_id>', methods=['GET'])
def get_lawyer_cases(lawyer_id):
    try:
        assigned_cases = Case.query.filter_by(lawyer_id=lawyer_id).all()
        assigned_cases_data = [{
            'case_id': case.case_id,
            'title': case.title,
            'description': case.description,
            'lawyer_id': case.lawyer_id
        } for case in assigned_cases]
        return jsonify({'assignedCases': assigned_cases_data}), 200
    except Exception as e:
        return jsonify({'message': f'Error fetching cases: {str(e)}'}), 500

@app.route("/api/civilian/login", methods=["POST"])
def login():
    data = request.json
    username = data.get('idOrUsername')
    password = data.get('password')
    if not username or not password:
        return jsonify({"message": "Username and Password required"}), 400
    account = Account.query.filter_by(username=username).first()
    if not account or not check_password_hash(account.password_hash, password):
        return jsonify({"message": "Invalid credentials"}), 401
    civilian = Civilian.query.filter_by(account_id=account.account_id).first()
    if not civilian:
        return jsonify({"message": "No civilian profile found"}), 404
    return jsonify({
        "message": "Login successful",
        "account_id": account.account_id,
        "civilian_id": civilian.civilian_id,
        "userType": "Civilian"
    }), 200

@app.route("/api/lawyer/login", methods=["POST"])
def lawyer_login():
    data = request.json
    lawyer_id = data.get('idOrUsername')
    password = data.get('password')
    if not lawyer_id or not password:
        return jsonify({"message": "Lawyer ID and Password required"}), 400
    lawyer = Lawyer.query.filter_by(lawyer_id=lawyer_id).first()
    if not lawyer:
        return jsonify({"message": "No lawyer profile found"}), 404
    account = Account.query.filter_by(account_id=lawyer.account_id).first()
    if not account or not check_password_hash(account.password_hash, password):
        return jsonify({"message": "Invalid credentials"}), 401
    return jsonify({
        "message": "Lawyer login successful",
        "userType": "Lawyer"
    }), 200

@app.route('/api/police/cases/<int:badge_id>', methods=['GET'])
def get_police_cases(badge_id):
    try:
        assigned_cases = db.session.query(Case, CaseAssign).\
            join(CaseAssign, Case.case_id == CaseAssign.case_id).\
            filter(CaseAssign.police_id == badge_id).all()
        resolved_cases = db.session.query(Case, CaseSolved).\
            join(CaseSolved, Case.case_id == CaseSolved.case_id).\
            filter(CaseSolved.police_id == badge_id).all()

        assigned_cases_data = [{
            'case_id': case.Case.case_id,
            'title': case.Case.title,
            'description': case.Case.description,
            'lawyer_id': case.Case.lawyer_id
        } for case in assigned_cases]

        resolved_cases_data = [{
            'case_id': case.Case.case_id,
            'title': case.Case.title,
            'description': case.Case.description,
            'lawyer_id': case.Case.lawyer_id
        } for case in resolved_cases]

        return jsonify({
            'assignedCases': assigned_cases_data,
            'resolvedCases': resolved_cases_data
        }), 200
    except Exception as e:
        return jsonify({'message': f'Error fetching cases: {str(e)}'}), 500

@app.route("/api/police/complaint", methods=["POST"])
def register_police_complaint():
    data = request.json
    badge_id = data.get('badge_id')
    if not badge_id:
        return jsonify({'message': 'Police badge ID required'}), 400
    police = Police.query.filter_by(badge_id=badge_id).first()
    if not police:
        return jsonify({'message': 'Invalid police ID'}), 401

    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    description = data.get('description')
    location = data.get('location')
    address = data.get('address')
    incident_date = data.get('incidentDate')
    timestamp = data.get('timestamp')

    if not all([description, location, incident_date]):
        return jsonify({'message': 'Description, location, and incident date are required'}), 400

    try:
        incident = Incident(
            name=name, email=email, phone=phone, description=description,
            location=location, address=address, incident_date=incident_date,
            timestamp=timestamp
        )
        db.session.add(incident)
        db.session.flush()

        lawyers = Lawyer.query.all()
        if not lawyers:
            return jsonify({'message': 'No lawyers available to assign'}), 500
        random_lawyer = choice(lawyers)

        case = Case(
            case_id=incident.incident_id,
            title=f"Case: {name or 'Unnamed'} - {incident_date}",
            description=description,
            lawyer_id=random_lawyer.lawyer_id
        )
        db.session.add(case)
        db.session.flush()

        case_assign = CaseAssign(case_id=case.case_id, police_id=badge_id)
        db.session.add(case_assign)
        db.session.commit()

        return jsonify({
            'message': 'Complaint registered and case assigned successfully',
            'incident_id': incident.incident_id,
            'case_id': case.case_id,
            'lawyer_id': random_lawyer.lawyer_id
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error registering complaint: {str(e)}'}), 500

@app.route("/api/police/login", methods=["POST"])
def police_login():
    data = request.json
    badge_id = data.get('idOrUsername')
    password = data.get('password')
    if not badge_id or not password:
        return jsonify({"message": "Badge ID and Password required"}), 400
    police = Police.query.filter_by(badge_id=badge_id).first()
    if not police:
        return jsonify({"message": "No police profile found"}), 404
    account = Account.query.filter_by(account_id=police.account_id).first()
    if not account or not check_password_hash(account.password_hash, password):
        return jsonify({"message": "Invalid credentials"}), 401
    return jsonify({
        "message": "Police login successful",
        "userType": "Police",
        "badge_id": str(police.badge_id)
    }), 200

@app.route("/api/civilian/signup", methods=["POST"])
def signup():
    data = request.json
    username = data.get('username')
    phoneno = data.get('phoneno')
    password = data.get('password')
    if not username or not password:
        return jsonify({'message': 'Username and Password required'}), 400
    existing_user = Account.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'message': 'User with same username exists!'}), 409
    hashed_password = generate_password_hash(password)
    account = Account(username=username, phoneno=phoneno, password_hash=hashed_password)
    db.session.add(account)
    db.session.commit()
    civilian = Civilian(username=username, account_id=account.account_id)
    db.session.add(civilian)
    db.session.commit()
    return jsonify({"message": "Signup successful"}), 201

@app.route("/api/lawyer/signup", methods=["POST"])
def lawyer_signup():
    data = request.json
    lawyer_id = data.get('id')
    phoneno = data.get('phoneno')
    password = data.get('password')
    email = data.get('email')
    
    if not all([lawyer_id, password, email, phoneno]):
        return jsonify({'message': 'All fields (Bar ID, Email, Phone Number, and Password) are required'}), 400
    
    if not phoneno.isdigit() or len(phoneno) != 10:
        return jsonify({'message': 'Phone number must be a 10-digit number'}), 400
    
    if '@' not in email or '.' not in email:
        return jsonify({'message': 'Please enter a valid email address'}), 400
    
    existing_email = Account.query.filter_by(email=email).first()
    if existing_email:
        return jsonify({'message': 'An account with this email already exists'}), 409
    
    existing_account = Account.query.filter_by(username=lawyer_id).first()
    if existing_account:
        return jsonify({'message': 'This Bar ID is already registered'}), 409
    
    existing_lawyer = Lawyer.query.filter_by(lawyer_id=lawyer_id).first()
    if existing_lawyer:
        return jsonify({'message': 'This Bar ID is already registered as a lawyer'}), 409
    
    try:
        hashed_password = generate_password_hash(password)
        account = Account(email=email, phoneno=phoneno, password_hash=hashed_password, username=lawyer_id)
        db.session.add(account)
        db.session.commit()
        
        lawyer = Lawyer(lawyer_id=lawyer_id, account_id=account.account_id)
        db.session.add(lawyer)
        db.session.commit()
        
        return jsonify({"message": "Lawyer signup successful"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error during signup: {str(e)}'}), 500

@app.route("/api/police/signup", methods=["POST"])
def police_signup():
    data = request.json
    badge_id = data.get('id')
    phoneno = data.get('phoneno')
    password = data.get('password')
    email = data.get('email')
    
    if not all([badge_id, password, email, phoneno]):
        return jsonify({'message': 'All fields (Badge ID, Email, Phone Number, and Password) are required'}), 400
    
    try:
        badge_id = int(badge_id)
        if badge_id <= 0:
            return jsonify({'message': 'Badge ID must be a positive number'}), 400
    except ValueError:
        return jsonify({'message': 'Badge ID must be a valid number'}), 400
    
    existing_email = Account.query.filter_by(email=email).first()
    if existing_email:
        return jsonify({'message': 'An account with this email already exists'}), 409
    
    existing_account = Account.query.filter_by(username=str(badge_id)).first()
    if existing_account:
        return jsonify({'message': 'This Badge ID is already registered'}), 409
    
    existing_police = Police.query.filter_by(badge_id=badge_id).first()
    if existing_police:
        return jsonify({'message': 'This Badge ID is already registered as a police officer'}), 409
    
    try:
        hashed_password = generate_password_hash(password)
        account = Account(email=email, phoneno=phoneno, password_hash=hashed_password, username=str(badge_id))
        db.session.add(account)
        db.session.commit()
        
        police = Police(badge_id=badge_id, account_id=account.account_id)
        db.session.add(police)
        db.session.commit()
        
        return jsonify({"message": "Police signup successful"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error during signup: {str(e)}'}), 500

@app.route('/api/lawyerInfo', methods=['POST'])
def add_lawyer_info():
    data = request.json
    bar_id = data.get('barId')
    branch_name = data.get('branchName')
    state = data.get('state')
    court_location = data.get('courtLocation')
    judiciary = data.get('judiciary')
    judiciary_id = data.get('judiciaryId')

    if not all([bar_id, state]):
        return jsonify({'message': 'Bar ID and State are required', 'success': False}), 400

    lawyer = Lawyer.query.filter_by(lawyer_id=bar_id).first()
    if not lawyer:
        return jsonify({'message': 'Lawyer not found. Please sign up first.', 'success': False}), 404

    try:
        existing_branch = LawyerInfo.query.filter_by(bar_id=bar_id, branch_name=branch_name).first()
        if existing_branch:
            return jsonify({'message': 'Court Branch already registered for this lawyer', 'success': False}), 400
        
        table_name = f"lawyer_info_{branch_name.replace(' ', '_').lower()}"
        metadata = MetaData()
        
        inspector = inspect(db.engine)
        if not inspector.has_table(table_name):
            new_table = Table(
                table_name, metadata,
                Column('info_id', Integer, primary_key=True),
                Column('bar_id', String(20), nullable=False),
                Column('branch_name', String(100)),
                Column('state', String(100)),
                Column('court_location', String(100)),
                Column('judiciary', String(100)),
                Column('judiciary_id', String(50))
            )
            metadata.create_all(db.engine)
            print(f"Created new table: {table_name}")

        with db.engine.connect() as connection:
            insert_stmt = text(
                f"INSERT INTO {table_name} (bar_id, branch_name, state, court_location, judiciary, judiciary_id) "
                f"VALUES (:bar_id, :branch_name, :state, :court_location, :judiciary, :judiciary_id)"
            )
            connection.execute(
                insert_stmt,
                {"bar_id": bar_id, "branch_name": branch_name, "state": state, 
                 "court_location": court_location, "judiciary": judiciary, "judiciary_id": judiciary_id}
            )
            connection.commit()
        
        return jsonify({'message': f'Court Registered Successfully in {table_name}', 'success': True}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error adding lawyer info: {str(e)}', 'success': False}), 500

@app.route('/api/policeInfo', methods=['POST'])
def add_police_info():
    data = request.json
    state = data.get('state')
    pin_code = data.get('pinCode')
    station_number = data.get('stationNumber')
    station_location = data.get('stationLocation')
    police_id = data.get('policeId')

    if not all([state, pin_code, station_number, station_location, police_id]):
        return jsonify({'message': 'All fields are required', 'success': False}), 400

    try:
        pin_code = int(pin_code)
        station_number = int(station_number)
    except (ValueError, TypeError):
        return jsonify({'message': 'Pin Code and Station Number must be numeric', 'success': False}), 400

    if not isinstance(state, str) or not isinstance(station_location, str) or not isinstance(police_id, str):
        return jsonify({'message': 'State, Station Location, and Police ID must be strings', 'success': False}), 400

    police = Police.query.filter_by(badge_id=police_id).first()
    if not police:
        return jsonify({'message': 'Police not found', 'success': False}), 404

    try:
        existing_station = PoliceInfo.query.filter_by(station_number=station_number).first()
        if existing_station:
            return jsonify({'message': 'Station number already registered', 'success': False}), 400

        table_name = f"police_station_{station_number}"
        metadata = MetaData()

        inspector = inspect(db.engine)
        if not inspector.has_table(table_name):
            new_table = Table(
                table_name, metadata,
                Column('id', Integer, primary_key=True),
                Column('state', String(100), nullable=False),
                Column('pin_code', Integer, nullable=False),
                Column('station_number', Integer, nullable=False),
                Column('station_location', String(200), nullable=False),
                Column('police_id', String(20), nullable=False)
            )
            metadata.create_all(db.engine)
            print(f"Created new table: {table_name}")

        with db.engine.connect() as connection:
            insert_stmt = text(
                f"INSERT INTO {table_name} (state, pin_code, station_number, station_location, police_id) "
                f"VALUES (:state, :pin_code, :station_number, :station_location, :police_id)"
            )
            connection.execute(
                insert_stmt,
                {"state": state, "pin_code": pin_code, "station_number": station_number, 
                 "station_location": station_location, "police_id": police_id}
            )
            connection.commit()

        return jsonify({'message': f'Police-Station info registered successfully in {table_name}', 'success': True}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error adding police-station info: {str(e)}', 'success': False}), 500

@app.route("/api/support", methods=["POST"])
def help_support():
    try:
        data = request.json
        if not data:
            return jsonify({'message': 'No data provided', 'success': False}), 400
        message = data.get('question')
        if not message:
            return jsonify({'message': 'Question is required', 'success': False}), 400
        account_id = data.get('account_id')
        info = Support(message=message, account_id=account_id)
        db.session.add(info)
        db.session.commit()
        return jsonify({
            'message': 'Question added successfully',
            'success': True,
            'support_id': info.support_id
        }), 201
    except db.exc.IntegrityError as e:
        db.session.rollback()
        return jsonify({'message': 'Database integrity error', 'success': False, 'error': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error processing request', 'success': False, 'error': str(e)}), 500

# NLP Routes
def get_relevant_sections(query, top_n=5):
    df = ResourceLoader.get_df()
    embeddings = ResourceLoader.get_embeddings()
    model = ResourceLoader.get_model()
    
    if not query.strip():
        return df[["Section", "Offense", "Punishment"]].to_dict(orient="records")
    
    try:
        query_embedding = model.encode(query, convert_to_tensor=True)
        similarity_scores = util.pytorch_cos_sim(query_embedding, embeddings).squeeze()
        top_indices = similarity_scores.argsort(descending=True)[:top_n]
        results = df.iloc[top_indices][["Section", "Offense", "Punishment"]].copy()
        results = results[~results["Offense"].str.startswith("IPC Section")]
        return results.to_dict(orient="records")
    except Exception as e:
        print(f"Error in get_relevant_sections: {str(e)}")
        return []

@app.route("/nlp/search", methods=["POST"])
def search_sections():
    try:
        data = request.json
        query = data.get("query", "")
        print(f"Received search query: {query}")
        results = get_relevant_sections(query)
        print(f"Returning {len(results)} results")
        return jsonify(results), 200
    except Exception as e:
        print(f"Error in search_sections: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/nlp/test', methods=['GET'])
def test():
    return jsonify({'message': 'Combined Backend with NLP is running!'}), 200

# Migration function
def migrate_evidence_table():
    with app.app_context():
        inspector = db.inspect(db.engine)
        if 'evidence' in inspector.get_table_names():
            columns = inspector.get_columns('evidence')
            police_id_nullable = any(col['name'] == 'police_id' and col['nullable'] for col in columns)
            
            if not police_id_nullable:
                print("Migrating evidence table...")
                db.engine.execute(text("ALTER TABLE evidence RENAME TO evidence_old"))
                db.create_all()
                migrate_sql = """
                INSERT INTO evidence (evidence_id, complaint_id, police_id, lawyer_id, submitter_type, file_path, upload_date)
                SELECT evidence_id, complaint_id, police_id, lawyer_id, 
                       COALESCE(submitter_type, 'police'), file_path, upload_date
                FROM evidence_old
                """
                db.engine.execute(text(migrate_sql))
                db.engine.execute(text("DROP TABLE evidence_old"))
                print("Evidence table migrated successfully.")
            else:
                print("Evidence table schema is already up-to-date.")
        else:
            db.create_all()
            print("Created evidence table")

# Initialize database at startup
with app.app_context():
    db.create_all()
    migrate_evidence_table()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)