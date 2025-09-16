NeuralGuardians – Agentic AI Smart Incident Responder
🚀 Overview

NeuralGuardians is an Agentic AI-powered cyber incident response system that detects, analyzes, and responds to suspicious activities in real-time.
It autonomously protects logins, file access, and fake account creation while providing clear AI-generated reports to admins.

This project was developed as part of a hackathon to showcase the future of AI-driven cybersecurity.

✨ Novelty

Agentic AI Workflow: Uses LangGraph to chain specialized AI agents (Detector → Analyzer → Action → Reporter).

Autonomous Defense: Detects threats and auto-blocks malicious users or sessions in real time.

Adaptive Detection: Learns from user login patterns, file access history, and bot behaviors.

Smart Reporting: AI-generated human-readable reports help admins take quick actions.

Hybrid Storage: Combines Redis for real-time counters and MongoDB for persistent incident history.

Email Alerts: Sends warning emails to users (via Gmail or RapidAPI) if login attempts exceed threshold.

🖥️ Tech Stack
Frontend

React.js + TailwindCSS

ThunderClient / Postman for API testing

Backend

Python Flask

LangGraph (Agent Orchestration)

Ollama (Local AI models e.g., Mistral, Llama3)

Databases

Redis → Fast counters (failed logins, file downloads)

MongoDB → Persistent storage of users, incidents, and reports

Other Tools

Flask-Mail / Gmail App Passwords (email alerts)

dotenv for environment variables

⚡ Problem-Solution Fit

Problem: Increasing cyberattacks like brute-force logins, unauthorized file access, and fake account creation are difficult to monitor manually.

Solution: NeuralGuardians provides an autonomous AI-powered SOC assistant that:

Detects anomalies in login attempts.

Monitors and blocks sensitive file access.

Flags fake or bot accounts.

Provides real-time dashboards and AI reports for admins.

🛠️ Setup & Installation
1️⃣ Clone the Repo
git clone https://github.com/<your-repo>/NeuralGuardians.git
cd NeuralGuardians/backend

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Setup Environment Variables

Create a .env file in backend/ with:

PORT=8000
MONGO_URI=mongodb://localhost:27017/neural_guardians
REDIS_HOST=localhost
REDIS_PORT=6379

MAIL_USERNAME=yourgmail@gmail.com
MAIL_PASSWORD=your_app_password

4️⃣ Run Redis & MongoDB
# Start Redis
redis-server

# Start MongoDB
mongod --dbpath ./data

5️⃣ Start Flask Server
python app.py

6️⃣ Start Frontend
cd frontend
npm install
npm run dev

🔍 API Routes
Auth

POST /register → Register new user

POST /login → Login user

Incidents

POST /incident → Send login/file access event for analysis

GET /incidents → Get all incidents

GET /incidents/<username> → Get incidents of specific user

GET /failed-logins → Get failed login history

GET /file-access → Get suspicious file access history

Analytics

GET /stats → Get system-wide incident stats

Testing

GET /send-test-email → Test mail sending

📊 Scalability & Impact

Can be scaled into a full SOC assistant for enterprises.

Pluggable with SIEM systems for real-world deployment.

Reduces response time from hours to milliseconds.

Protects against insider threats, brute-force attacks, and malicious file downloads.

🎥 Demo

Frontend dashboard showing:

Failed login attempts with risk levels

File access incidents with severity

AI-generated incident reports

Backend logs for anomaly detection

Email alerts triggered after 3 failed logins

👨‍💻 Team NeuralGuardians

Thatikonda Vigneshwar (Backend + AI Agents)

[Add team names if applicable]

⚡ NeuralGuardians – Building the future of Autonomous AI Security Agentss

## Repository Structure

Neural_Gaurdians/
├── Backend/
│ ├── [Python files …]
│ └── …
├── neural_frontend/
│ ├── [JS / React / CSS etc …]
│ └── …
├── .gitignore
└── README.md ← (this file)


- **Backend/**: contains the server side code (APIs, maybe model, routing etc)  
- **neural_frontend/**: UI client side  
- **.gitignore**: files/folders ignored by Git  

---

## Dependencies

You need to install dependencies for both backend and frontend parts.

### Backend

- Python (version ≥ 3.x)  
- Some Python packages: (examples) Flask / Django / FastAPI / others (depending on which framework used)  
- Possibly ML / deep-learning libraries like PyTorch, TensorFlow, or others.  
- Other utilities (e.g. for data processing, maybe database driver)  

### Frontend

- Node.js (version ≥ 14 or 16, depending)  
- Package manager: npm or yarn  
- Frontend framework (React / Vue / Angular / plain JS)  
- Other JS dependencies (CSS frameworks, build tools, etc.)  

---

## Setup / Installation

> These instructions assume you have `git`, `python`, `node` installed on your machine.

### Backend Setup

1. Clone the repository  
   ```bash
   git clone https://github.com/Pats03/Neural_Gaurdians.git
   cd Neural_Gaurdians/Backend
python3 -m venv venv        # or: python -m venv venv
source venv/bin/activate
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install flask  # and other packages
cd ../neural_frontend
npm install
npm start
Running the Project

With both backend and frontend set up:

Start the backend server:

cd Backend
source venv/bin/activate        # if not already active
# or on Windows activate venv as earlier
python app.py                    # or whatever the entry point is


Alternatively, if using Flask:

export FLASK_APP=app.py         # on macOS/Linux
set FLASK_APP=app.py            # on Windows CMD
flask run


Note: the port (default is often 5000) and host might be configurable.

Start the frontend server:

cd neural_frontend
npm start


Visit the frontend in your browser:

Usually at http://localhost:3000 (or whatever port your frontend dev server uses).
The frontend will make API calls to the backend (e.g. localhost:5000) — might need to configure CORS or proxy.

Environment Variables / Configuration

You may need to set up some environment / config values, such as:

Variable	Purpose / What to set
FLASK_APP or similar	Points to the main backend file (e.g. app.py)
FLASK_ENV	Development vs production mode (e.g. development)
API_BASE_URL or frontend config	URL of backend server for API calls
Database credentials, if used	
Secret keys (if authentication is involved)	

You can create a .env file in the backend root (and possibly in frontend) and load these with dotenv or equivalent.
Troubleshooting / FAQ

If you get a module not found error in backend → ensure you installed all required packages and the virtual environment is activated.

If frontend cannot communicate with backend → check the API base URL / CORS settings.

Port conflicts → change port via command line or config.

If static assets or missing files error → check that the frontend build / public folder is correct.

License & Attribution

Specify the license under which this project is released (e.g. MIT, GPL, etc.).
If any external libraries/models are used, give credit / references.
