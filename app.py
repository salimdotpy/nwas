from routes import app
from models import db

@app.context_processor
def utility_processor():
    from helper import siteName, getImage
    return dict(siteName=siteName, getImage=getImage)

if __name__ == '__main__':
    # Create the database tables.
    with app.app_context():
        db.create_all()
    # Start the Flask development web server.
    # app.run(debug=True, host='0.0.0.0')
    app.run(debug=True)
