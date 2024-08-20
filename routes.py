from flask import Flask, jsonify, render_template, session
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask_restful import Api
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from models import db, User, Incident
from controller.UserController import UserController
from controller.AdminController import AdminController
import config

app = Flask(__name__)
app.secret_key = b'salimtech.nwas'

app.config.from_object(config)

# Initialize the Flask-SQLAlchemy object.
db.init_app(app)
csrf = CSRFProtect(app)
socketio = SocketIO(app)

# Create the Flask-RESTful API manager.
CORS(app, supports_credentials=True, origins=["http://localhost:3000"])

# |--------------------------------------------------------------------------
# | Admin Routes
# |--------------------------------------------------------------------------
app.add_url_rule('/admin/login','admin.login', AdminController.login, methods=['POST'])
app.add_url_rule('/admin/logout','admin.logout', AdminController.logout, methods=['GET'])
app.add_url_rule('/admin/dashboard','admin.dashboard', AdminController.dashboard, methods=['GET', 'POST'])
app.add_url_rule('/admin/profile','admin.profile', AdminController.profileUpdate, methods=['POST'])
app.add_url_rule('/admin/password','admin.password', AdminController.passwordUpdate, methods=['POST'])
app.add_url_rule('/admin/user','admin.user', AdminController.manageUser, methods=['GET','POST'])
app.add_url_rule('/admin/incident','admin.incident', AdminController.manageIncident, methods=['GET','POST'])

# |--------------------------------------------------------------------------
# | User Routes
# |--------------------------------------------------------------------------
app.add_url_rule('/signup','signup', UserController.signup, methods=['GET', 'POST'])
app.add_url_rule('/login','login', UserController.login, methods=['GET', 'POST'])
app.add_url_rule('/user/logout','user.logout', UserController.logout, methods=['GET'])
app.add_url_rule('/user/dashboard','user.dashboard', UserController.dashboard, methods=['GET', 'POST'])
app.add_url_rule('/user/profile','user.profile', UserController.profileUpdate, methods=['POST'])
app.add_url_rule('/user/password','user.password', UserController.passwordUpdate, methods=['POST'])
app.add_url_rule('/user/member','user.member', UserController.member, methods=['GET', 'POST'])
app.add_url_rule('/user/track/<id>/<loc>','user.track', UserController.track, methods=['GET', 'POST'])

@app.route('/', methods=['GET'])
def index():
    pageTitle = "Index Page"
    return render_template('index.html', pageTitle=pageTitle)

@app.route('/get_csrf_token', methods=['GET'])
def get_csrf_token():
    token = generate_csrf()
    response = jsonify({'csrf_token': token})
    return response

@socketio.on('update_location')
def update_location(data):
    if 'user' in session:
        user = User.query.get(session['user']['id'])
        incident = Incident.query.get(data['iid'])
        alarm = incident.to_dict()
        if alarm.raiser.id != user.id:
            try:
                location = alarm.location['member'][user.id] = data['loc']
            except:
                location = alarm.location['member'] = {user.id: data['loc']}
            try:
                incident.location = location
                db.session.commit()
            except:
                db.session.rollback()
        emit('location_update', {'id': user.id, 'location': data['loc']}, broadcast=True)