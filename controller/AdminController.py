from flask import render_template, request, flash, redirect, url_for, session
from models import User, Admin, Setting, Incident, db
from flask_wtf.csrf import generate_csrf
from werkzeug.security import generate_password_hash
import time, re

class AdminController():
    def dashboard():
        pageTitle = "Admin Dashboard"
        widget = {}
        if 'admin' in session:
            widget['users'] = User.query.all()
            admin = Admin.query.get(session['admin']['id'])
            return render_template('admin/dashboard.html', pageTitle=pageTitle, admin=admin, widget=widget)
        flash('Please login first!', ('warning'))
        return redirect(url_for('login')+'#admin')
    
    def track():
        pageTitle = "Track Page"    
        user = False
        if 'user' in session:
            user = User.query.get(session['user']['id'])
            return render_template('track.html', pageTitle=pageTitle, user=user)
        flash('Please login first!', ('warning'))
        return redirect(url_for('login'))
    
    def profileUpdate():
        if 'admin' in session:
            admin = Admin.query.get(session['admin']['id'])
            # Create variables for easy access
            name = request.form['name']
            email = request.form['email']
            contact = request.form['contact']
            if not name or not contact or not email:
                msg = ['Please fill out the form!', 'error']
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email) or len(email) > 30:
                msg = ['Invalid email address!', 'error']
            elif not contact or len(contact) != 11:
                msg = ['Invalid phone number!', 'error']
            else:
                admin.name = name
                admin.email = email
                admin.mobile = contact
                try: 
                    db.session.commit()
                    msg = ['Profile updated successfully!', 'success']
                except:
                    db.session.rollback()
                    msg = ['Unable to update profile, please try again later!', 'error']
                session['admin'] = admin.to_dict()
            flash(msg[0], (msg[1]))
            return redirect(url_for('admin.dashboard'))
        flash('Please login first!', ('warning'))
        return redirect(url_for('login')+'#admin')
    
    def passwordUpdate():
        if "admin" in session:
            admin = Admin.query.get(session['admin']['id'])
            # Create variables for easy access
            opass = request.form['opass']
            npass = request.form['npass']
            cpass = request.form['cpass']
            if not opass or not npass or not cpass:
                msg = ['Please fill out the form!', 'error']
            elif npass != cpass:
                msg = ['Two password does not match!', 'error']
            elif not admin.check_password(opass):
                msg = ['Old password does not match!', 'error']
            else:
                password = generate_password_hash(npass)
                admin.password = password
                try: 
                    db.session.commit()
                    msg = ['Password updated successfully!', 'success']
                except: 
                    db.session.rollback()
                    msg = ['Unable to update password, please try again later!', 'error']
                session['admin'] = admin.to_dict()
            flash(msg[0], (msg[1]))
            return redirect(url_for('admin.dashboard'))
        flash('Please login first!', ('warning'))
        return redirect(url_for('login')+'#admin')

    def manageUser():
        if "admin" in session:
            # admin = Admin.query.get(session['admin']['id'])
            users = User.query.all()
            pageTitle = "Manage User"
            community = db.session.query(Setting.data_values).filter_by(data_keys='community').all()
            if request.method == 'POST' and 'addUser' in request.form:
                surname = request.form['surname']
                othername = request.form['othername']
                mobile = request.form['contact']
                role = False if request.form['role'] == '0' else True
                community = request.form['community']
                # Check if account exists using MySQL
                checkMobile = User.query.filter_by(mobile=mobile).first()
                checkCommunity = User.query.filter_by(community=community, role=role).first()
                # Validation checks
                if not surname or not othername or not mobile:
                    msg = ['Please fill out the form!', 'error']
                elif not mobile or len(mobile) != 11:
                    msg = ['Invalid phone number!', 'error']
                elif checkMobile:
                    msg = ['This phone number has been taken, please try another one', 'error']
                elif checkCommunity and role:
                    msg = [f"{community} already have coordinator, change role to member", 'error']
                else:
                    password = generate_password_hash(surname)
                    user = User(role=role, surname=surname, othername=othername, mobile=mobile, community=community, password=password)
                    try:
                        db.session.add(user)
                        db.session.commit()
                        msg = ['New user added successfully!', 'success']
                    except: 
                        db.session.rollback()
                        msg = ['Unable to add new user, please try again later!', 'error']
                flash(msg[0], (msg[1]))
                return redirect(request.referrer)
            if request.method == 'GET' and 'editUser' in request.args:
                id = request.args['uid']
                data = User.query.filter_by(id=id).first(); data.to_dict()
                isRole = 'checked' if data.role else ''; notRole = '' if data.role else 'checked'
                html = f'''
                <form class="" method="post">
                    <input type="hidden" name="csrf_token" value="{generate_csrf()}">
                    <input type="hidden" name="uid" value="{data.id}">
                    <div class="form-group">
                        <label>Surname:</label>
                        <input type="text" name="surname" class="form-control" placeholder="Enter Surname" value="{data.surname}">
                    </div>
                    <div class="form-group">
                        <label>Othername:</label>
                        <input type="text" name="othername" class="form-control" placeholder="Enter Othername" value="{data.othername}">
                    </div>
                    <div class="form-group">
                        <label>Phone Number:</label>
                        <input type="tel" name="contact" class="form-control" placeholder="Enter Phone Number" value="{data.mobile}">
                    </div>
                    <div class="form-group">
                        <label>Community Role:</label>
                        <div class="form-control">
                            <label>
                                <input type="radio" name="role" value="0" {notRole}> Member
                            </label>
                            <label>
                                <input type="radio" name="role" value="1" {isRole}> Coordinator
                            </label>
                        </div>
                    </div>
                    <div class="form-group">
                        <label>Community:</label>
                        <select name="community" class="form-control">
                            <option value="{data.community}">{data.community}</option>'''
                for com in community:
                    if com[0] == data.community: continue
                    html += f'''<option value="{com[0]}">{com[0]}</option>'''
                html += '''
                        </select>
                    </div>
                    <div class="form-group">
                        <button class="btn btn-primary pull-right" name="updateUser" type="submit">Update</button>
                        <button class="btn btn-danger" data-dismiss="modal">Cancel</button>
                    </div>
                </form>'''
                return html
            if request.method == 'POST' and 'updateUser' in request.form:
                uid = request.form['uid']
                surname = request.form['surname']
                othername = request.form['othername']
                mobile = request.form['contact']
                role = False if request.form['role'] == '0' else True
                community = request.form['community']
                # Check if account exists using MySQL
                checkCommunity = db.session.query(User).filter(User.community==community, User.role==role, User.id != uid).first()
                checkMobile = db.session.query(User).filter(User.mobile==mobile, User.id != uid).first()
                # Validation checks
                if not surname or not othername or not mobile:
                    msg = ['Please fill out the form!', 'error']
                elif not mobile or len(mobile) != 11:
                    msg = ['Invalid phone number!', 'error']
                elif checkMobile:
                    msg = ['This phone number has been taken, please try another one', 'error']
                elif checkCommunity and role:
                    msg = [f"{community} already have coordinator, change role to member", 'error']
                else:
                    user = User.query.get(int(uid))
                    user.surname = surname
                    user.othername = othername
                    user.mobile = mobile; user.role = role
                    user.community = community
                    try:
                        db.session.commit()
                        msg = ['Updated successfully!', 'success']
                    except: 
                        db.session.rollback()
                        msg = ['Unable to update, please try again later!', 'error']
                flash(msg[0], (msg[1]))
                return redirect(request.referrer)
            if request.method == 'POST' and 'deleteUser' in request.form:
                # Create variables for easy access
                id = request.form['id']
                try:
                    db.session.query(User).filter(User.id == id).delete()
                    db.session.commit()
                    msg =  ['User\'s record deleted successfully!', 'success']
                except:
                    db.session.rollback()
                    msg =  ['Unable to delete User\'s record, please try again later!', 'error']
                flash(msg[0], (msg[1]))
                return redirect(request.referrer)
            return render_template('admin/manage_user.html', pageTitle=pageTitle, users=users, community=community)
        flash('Please login first!', ('warning'))
        return redirect(url_for('login')+'#admin')
    
    def manageIncident():
        if "admin" in session:
            incident = Incident.query.all()
            pageTitle = "Manage Incident"
            return render_template('admin/manage_incident.html', pageTitle=pageTitle, incident=incident)
        flash('Please login first!', ('warning'))
        return redirect(url_for('login')+'#admin')
    
    def signup():
        pageTitle = "Signup Page"
        error, valid = {}, 1
        communities = db.session.query(Setting.data_values).filter_by(data_keys='community').all()
        if request.method == 'POST':
            # Create variables for easy access
            surname = request.form['surname']
            othername = request.form['othername']
            mobile = request.form['contact']
            role = False if request.form['role'] == '0' else True
            community = request.form['comm'] if role  else request.form['community']
            # Check if account exists using MySQL
            checkMobile = User.query.filter_by(mobile=mobile).first()
            checkCommunity = User.query.filter_by(community=community, role=role).first()
            # Validation checks
            if not surname:
                error['surname'] = "Surname is required"; valid = 0
            if not othername:
                error['othername'] = "Othername is required"; valid = 0
            if not mobile or len(mobile) != 11:
                error['mobile'] = "Invalid phone number"; valid = 0
            if checkMobile:
                error['mobile'] = "This phone number has been taken, please try another one"; valid = 0
            if not community:
                error['community'] = "Community is required"; valid = 0
            if checkCommunity and role:
                error['community'] = f"{community} already have coordinator, change your role to member"; valid = 0
            if valid:
                password = generate_password_hash(surname)
                user = User(role=role, surname=surname, othername=othername, mobile=mobile, community=community, password=password)
                checkComm = Setting.query.filter_by(data_keys='community', data_values=community).first()
                try:
                    db.session.add(user)
                    db.session.commit()
                    if role and not checkComm:
                        db.session.add(Setting(data_keys='community', data_values=community))
                        db.session.commit()
                    flash('You\'ve registered successfully,  login now please!', ('success'))
                    return redirect(url_for('login'))
                except Exception as e:
                    print(e)
                    db.session.rollback()
                    flash('Something went wrong, Please try again!', ('error'))
                    return redirect(request.referrer)
            flash('Fill out the form and try again!', ('error'))
        return render_template('signup.html', pageTitle=pageTitle, error=error, community=communities)
    
    def login():
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Validation checks
        admin = Admin.query.filter_by(name=username).first()
        if admin is None or not admin.check_password(password):
            flash('Invalid Credential', ('error'))
            return redirect(request.referrer+'#admin')   
        session['admin'] = admin.to_dict()
        flash('You\'ve successfully logged in!', ('success'))
        return redirect(url_for('admin.dashboard'))
    
    def logout():
        session.pop('user', None)
        flash('You have successfully logged out!', ('warning'))
        return redirect(url_for('login')+'#admin')