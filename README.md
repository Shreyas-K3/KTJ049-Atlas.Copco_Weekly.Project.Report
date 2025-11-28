Weekly Project Update App (Streamlit & SQLite)

A minimal, visually impactful project update dashboard built with Streamlit, SQLAlchemy/SQLite, and GitHub for deployment.

🚀 Quick Start

Install Dependencies:

pip install -r requirements.txt


Add Initialization File: Ensure the file app/__init__.py (it can be empty) exists to make the app directory a Python package.

Run the App:

streamlit run streamlit_app.py


🔐 Access Credentials

Client View: Requires a project code (set by the Admin) and client name.

Admin Panel: Requires the hardcoded Admin Access Code.

Default Admin Code: SECRET_ADMIN_123

(It is highly recommended to change this in a production environment.)

🎨 Visual Enhancements

Meters: Circular HTML/CSS meters are used for visually tracking progress and days spent.

Branding: Strong Dark Mode theme using Red/Black/White colors.

Font: Requires AvantGarde.woff2 in app/assets/fonts/ for the custom font, with a fallback to system sans-serif.

📂 Folder Structure

app/: Core logic (Client, Admin, DB, Styling, Utilities).

data/: Stores app.db (SQLite). Note: Exclude data/app.db from git, but ensure data/.gitkeep exists.

streamlit_app.py: Main entry point and authentication router.

☁️ Deployment (Streamlit Cloud)

Push this repo to GitHub.

Go to Streamlit Cloud, select your repo.

Set Main file path to streamlit_app.py.

Deploy!

🚧 TODO: Real-time Upgrade Path

For true real-time push notifications (avoiding the 10-second polling refresh on the Admin comments page), consider:

WebSocket Microservice: Build a small, separate FastAPI service to handle WebSocket connections and database write triggers.

Streamlit Component: Use a community component like streamlit-webrtc or streamlit-socketio to manage the WebSocket connection directly from the client side. The current DB polling is sufficient for moderate internal use but should be replaced for high concurrency.
