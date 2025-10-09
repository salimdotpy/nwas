# 🛡️ Neighbourhood Watch Assistance System

A Flask-based web application that empowers communities to report, monitor, and respond to safety incidents within their neighborhood.  
This system integrates **Google Maps** for real-time location tracking and employs the **Vincenty inverse formula** for accurate geodesic distance calculations between coordinates.

---

## 🚀 Features

- 📍 **Accurate Location Tracking:** Uses Vincenty formula (inverse method) to compute precise distances between two GPS coordinates.
- 🗺️ **Google Maps Integration:** Visual representation of incident reports and responder locations.
- 🔔 **Real-time Alerts:** Built with Flask-SocketIO for instant communication and event updates.
- 👥 **Community Reporting:** Users can report suspicious activity or emergencies in their area.
- 🧭 **Proximity-Based Response:** Identifies nearby watch members or authorities based on computed distances.
- 💾 **Database-Driven:** Persistent storage powered by SQLAlchemy with MySQL connector.
- 🔒 **Secure Forms & API:** Utilizes Flask-WTF for validation and Flask-RESTful for modular API design.

---

## 🧩 Tech Stack

- **Backend:** Flask, Flask-RESTful, Flask-SocketIO
- **Frontend:** Google Maps JavaScript API, HTML/CSS/JS
- **Database:** MySQL (via Flask-SQLAlchemy)
- **Distance Calculation:** Vincenty Formula (Inverse Method)
- **Real-time Communication:** WebSocket (Flask-SocketIO)

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/<your-username>/nwas.git
cd nwas
```

2. **Create and activate a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   Create a .env file in the root directory and add your configuration:
   ```ini
   SECRET_KEY=your_secret_key
   SQLALCHEMY_DATABASE_URI=mysql+mysqlconnector://user:password@localhost/db_name
   GOOGLE_MAPS_API_KEY=your_google_maps_api_key
   ```
5. **Run the application**
   ```bash
   flask run
   ```
   The app will be available at: http://127.0.0.1:5000

---

## 📦 Dependencies

```ini
aniso8601==9.0.1
blinker==1.7.0
certifi==2024.6.2
charset-normalizer==3.3.2
click==8.1.7
colorama==0.4.6
Flask==3.0.0
Flask-Cors==4.0.1
Flask-RESTful==0.3.10
Flask-SQLAlchemy==3.1.1
Flask-WTF==1.2.1
Flask-SocketIO==5.3.6
greenlet==3.0.1
idna==3.7
importlib-metadata==6.8.0
itsdangerous==2.1.2
Jinja2==3.1.2
MarkupSafe==2.1.3
mysql-connector==2.2.9
Pillow==9.2.0
pytz==2023.3.post1
requests==2.32.3
six==1.16.0
SQLAlchemy==2.0.23
typing_extensions==4.8.0
urllib3==2.2.2
Werkzeug==3.0.1
WTForms==3.1.2
zipp==3.17.0
```

---

## 🗺️ Google Maps Integration

The system uses the Google Maps API to:
- Display user-reported incidents.
- Show responder and watcher locations.
- Provide navigation and proximity-based alerts.

---

**🤝 Contributing**
Contributions, suggestions, and improvements are welcome!
Feel free to open an issue or submit a pull request.

**👨‍💻 Author**

Selim Adekola
📧 salimdotpy@gmail.com
📞 +2348076738293
