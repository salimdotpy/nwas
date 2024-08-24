from flask import render_template, request, flash, redirect, url_for, session
from flask_socketio import SocketIO, emit
from models import User, Setting, Incident, Notification, db
from werkzeug.security import generate_password_hash
import time

class UserController():
    def dashboard():
        pageTitle = "User Dashboard"
        if 'user' in session:
            user = User.query.get(session['user']['id'])
            notify = Notification.query.filter_by(community=user.community).first()
            pageTitle = "Member Dashboard" if user.role == 0 else "Coordinator Dashboard"
            if request.method == 'POST' and 'riaseAlarm' in request.form:
                incident = request.form['incident']
                location = request.form['location']
                # Validation checks
                if not incident:
                    msg = ['Please fill out the form!', 'error']
                elif not location:
                    msg = ['Unable to get your location, try again please!', 'error']
                else:
                    location = {'raiser': {user.id: location}}
                    incident = Incident(uid=user.id, incident=incident, community=user.community, location=str(location))
                    try:
                        db.session.add(incident)
                        db.session.commit()
                        notify = Notification(iid=incident.id, text=f'New alarm raised by {user.surname} {user.othername}')
                        db.session.add(notify)
                        db.session.commit()
                        # emit('alarm_raised', {'id': incident.id, 'msg': f'New alarm raised by {user.surname} {user.othername}'}, broadcast=True)
                        flash('Alarm riased successfully!', 'success')
                        return redirect(url_for('user.track', id=incident.id, loc=location))
                    except: 
                        db.session.rollback() 
                        msg = ['Unable to riased alarm, please try again later!', 'error']
                flash(msg[0], (msg[1]))
                return redirect(request.referrer)
            return render_template('dashboard.html', pageTitle=pageTitle, user=user, notify=notify)
        flash('Please login first!', ('warning'))
        return redirect(url_for('login'))
    
    def track(id, loc):
        pageTitle = "Track Page" 
        if 'user' in session:
            user = User.query.get(session['user']['id'])
            incident = Incident.query.get(id)
            alarm = incident.to_dict()
            if incident.raiser.id != user.id:
                try:
                    alarm['location']['member'][user.id] = loc
                except:
                    alarm['location']['member'] = {user.id: loc}
                try:
                    incident.location = str(alarm['location'])
                    db.session.commit()
                except:
                    db.session.rollback()
            # emit('member_join', {'id': user.id, 'name': f'{user.surname} {user.othername}', 'location': loc}, broadcast=True)
            return render_template('track.html', pageTitle=pageTitle, user=user, incident=alarm)
        flash('Please login first!', ('warning'))
        return redirect(url_for('login'))
    
    def monitor():
        if 'user' in session:
            user = User.query.get(session['user']['id'])
            incident = Incident.query.filter_by(community=user.community).all()
            if request.method == 'POST' and 'alarm_raised' in request.form:
                return Notification.query.filter_by(community=user.community).all()
            if request.method == 'POST' and 'location_update' in request.form:
                incident = [{'location': list(eval(e.location).values())} for e in incident]
                location = None
                try:
                    location = []
                    for i, j in incident[0]['location'][0].items():
                        get = User.query.get(i)
                        location.append({'id': i, 'name': f'{get.surname} {get.othername}', 'location': j})
                    for i, j in incident[0]['location'][1].items():
                        get = User.query.get(i)
                        location.append({'id': i, 'name': f'{get.surname} {get.othername}', 'location': j})
                except:
                    location = []
                    for i, j in incident[0]['location'][0].items():
                        get = User.query.get(i)
                        location.append({'id': i, 'name': f'{get.surname} {get.othername}', 'location': j})
                return location
            return None
        return None

    def profileUpdate():
        if 'user' in session:
            user = User.query.get(session['user']['id'])
            # Create variables for easy access
            surname = request.form['surname']
            othername = request.form['othername']
            mobile = request.form['contact']
            img_file = oldImage = request.form['oldImage']
            image = request.files['image']
            # Check if account exists using MySQL
            checkMobile = db.session.query(User).filter(User.mobile==mobile, User.id != user.id).first()
            # Validation checks
            if not surname or not othername or not mobile:
                msg = ['Please fill out the form!', 'error']
            elif not int(mobile) or len(mobile) != 11:
                msg = ['Invalid phone number!', 'error']
            elif checkMobile:
                msg = ['This phone number has been taken, please try another one', 'error']
            else:
                user.surname = surname
                user.othername = othername
                user.mobile = mobile
                if image:
                    pre = 'Coordinator_' if user.role else 'Member_'
                    img_file = pre+str(time.time())+'.jpg' if oldImage=="None" else oldImage
                    image.save('static/images/users/'+img_file)
                try:
                    if img_file !="None": user.image = img_file
                    db.session.commit()
                    msg = ['Profile updated successfully!', 'success']
                except:
                    db.session.rollback()
                    msg = ['Unable to update profile, please try again later!', 'error']
            session['user'] = user.to_dict()
            flash(msg[0], (msg[1]))
            return redirect(url_for('user.dashboard'))
        flash('Please login first!', ('warning'))
        return redirect(url_for('login'))
    
    def passwordUpdate():
        if "user" in session:
            user = User.query.get(session['user']['id'])
            # Create variables for easy access
            opass = request.form['opass']
            npass = request.form['npass']
            cpass = request.form['cpass']
            if not opass or not npass or not cpass:
                msg = ['Please fill out the form!', 'error']
            elif npass != cpass:
                msg = ['Two password does not match!', 'error']
            elif not user.check_password(opass):
                msg = ['Old password does not match!', 'error']
            else:
                password = generate_password_hash(npass)
                user.password = password
                try: 
                    db.session.commit()
                    msg = ['Password updated successfully!', 'success']
                except:
                    db.session.rollback() 
                    msg = ['Unable to update password, please try again later!', 'error']
                session['user'] = user.to_dict()
            flash(msg[0], (msg[1]))
            return redirect(url_for('user.dashboard'))
        flash('Please login first!', ('warning'))
        return redirect(url_for('login'))

    def member():
        if "user" in session:
            user = User.query.get(session['user']['id'])
            pageTitle = f"{user.community} Community Member"
            member = User.query.filter_by(community=user.community).all()
            if request.method == 'POST':
                # Create variables for easy access
                surname = request.form['surname']
                othername = request.form['othername']
                mobile = request.form['contact']
                # Check if account exists using MySQL
                checkMobile = User.query.filter_by(mobile=mobile).first()
                if not surname or not othername or not mobile:
                    msg = ['Please fill out the form!', 'error']
                elif not mobile or len(mobile) != 11:
                    msg = ['Invalid phone number', 'error']
                elif checkMobile:
                    msg = ['This phone number has been taken, please try another one', 'error']
                else:
                    password = generate_password_hash(surname)
                    user = User(surname=surname, othername=othername, mobile=mobile, community=user.community, password=password)
                    try: 
                        db.session.add(user)
                        db.session.commit()
                        msg = ['New member registered successfully!', 'success']
                    except:
                        db.session.rollback() 
                        msg = ['Unable to register member, please try again later!', 'error']
                flash(msg[0], (msg[1]))
                return redirect(request.referrer)
            return render_template('member.html', pageTitle=pageTitle, user=user, member=member)
        flash('Please login first!', ('warning'))
        return redirect(url_for('login'))
    
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
                    db.session.rollback()
                    print(e)
                    flash('Something went wrong, Please try again!', ('error'))
                    return redirect(request.referrer)
            flash('Fill out the form and try again!', ('error'))
        return render_template('signup.html', pageTitle=pageTitle, error=error, community=communities)
    
    def login():
        pageTitle = "Login Page"
        if request.method == 'POST':
            # Create variables for easy access
            mobile = request.form['contact']
            password = request.form['password']
            # Validation checks
            user = User.query.filter_by(mobile=mobile).first()
            if user is None or not user.check_password(password):
                flash('Invalid Credential', ('error'))
                return redirect(request.referrer)
            session['user'] = user.to_dict()
            flash('You\'ve successfully logged in!', ('success'))
            return redirect(url_for('user.dashboard'))
        return render_template('login.html', pageTitle=pageTitle)
    
    def forgetRestPass():
        msg = ''
        if request.method == 'POST' and 'forgotP' in request.form:
            # Create variables for easy access
            contact = request.form['contact']
            surname = request.form['surname']
            # Check if account exists
            user = User.query.filter_by(mobile=contact, surname=surname).first()
            if user: return [contact, True]
            else: return ['Invalid Credential!', False]
        if request.method == 'POST'and 'resetP' in request.form:
            # Create variables for easy access
            msg = ''
            npass = request.form['npass']
            cpass = request.form['cpass']
            contact = request.form['contact']
            # validation checks
            if not npass or not cpass or not contact:
                msg = ['Please fill out the form!', 'error']
            elif npass != cpass:
                msg = ['Two password does not match!', 'error']
            else:
                update = User.query.filter_by(mobile=contact).first()
                password = generate_password_hash(npass)
                update.password = password
                try:
                    db.session.commit()
                    return ['Password reset successfully!', 'success']
                except:
                    db.session.rollback()
                    return ['Unable to reset Password, Please try again!', 'error']
        return msg

    def logout():
        session.pop('user', None)
        flash('You have successfully logged out!', ('warning'))
        return redirect(url_for('login'))