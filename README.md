# FixMyCar AI 🔧🚗

**FixMyCar AI** is a functional, responsive web application that empowers ordinary car owners to perform basic maintenance and repairs at home with confidence. It delivers clear, safety-first, step-by-step guides, digital garage management, and persistent repair progress tracking.

Built with Python Flask, PostgreSQL, SQLAlchemy, Jinja2, modern dark-mode automotive CSS, and vanilla JavaScript. Ready for instant deployment to Render.com and GitHub.

---

## 🌟 Key Features

- **Automotive Repair Library**: 8 core home repair guides:
  1. *Engine Oil Change* (Comprehensive 9-step guide with torque cautions)
  2. *Replace Engine Air Filter*
  3. *Replace Cabin Air Filter*
  4. *Replace Car Battery* (12V handling and terminal sequence rules)
  5. *Replace Brake Pads* (Intermediate safety-first guide)
  6. *Replace Brake Discs* (Precision rotor replacement)
  7. *Replace Windshield Wipers* (Windshield protection tips)
  8. *Change a Headlight Bulb* (Halogen bulb quartz handling)
- **Digital Garage**: Add, view, edit, and manage multiple vehicles (Brand, Model, Year, Engine, optional VIN and Mileage).
- **Interactive Step-by-Step Workshop Mode**:
  - High-contrast, mobile-optimized cards readable in dim garage lighting or standing under the hood.
  - Previous / Next buttons and keyboard arrow key navigation (`←` and `→`).
  - Screen WakeLock API integration so your phone screen doesn't time out while turning wrenches.
  - Progress bar dynamically updating and saving state to PostgreSQL.
- **Persistent Repair Logging**:
  - Resumes exactly where you left off if you close the browser.
  - Completion timestamps and custom maintenance notes (e.g. oil viscosity, part numbers).
- **Safety First Architecture**:
  - Persistent reminders never to work under a car supported solely by a jack.
  - Clear hazard warnings for hot fluids, hazardous battery acid, and safety-critical brake hydraulics.
- **Enterprise Security**:
  - Werkzeug password hashing (passwords are never stored in plain text).
  - Strict ownership checks on every vehicle and repair session.
  - CSRF protection across all forms via Flask-WTF.
  - Secure session cookies with automatic HTTPS detection.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.11+, Flask 3.x
- **Database**: PostgreSQL (with SQLite automatic fallback for local zero-config dev)
- **ORM & Migrations**: Flask-SQLAlchemy 3.x, Flask-Migrate 4.x (Alembic)
- **Authentication & Security**: Flask-Login, Werkzeug, Flask-WTF CSRF protection
- **Frontend**: Responsive HTML5, Jinja2 templates, Custom Dark Automotive CSS3, Vanilla ES6 JavaScript
- **Production Server**: Gunicorn WSGI server

---

## 📁 Project Structure

```
fixmycar-ai/
├── app.py                  # Application factory, routes, and error handlers
├── config.py               # Environment configuration and database URL normalization
├── forms.py                # WTForms form validations and CSRF protection
├── models.py               # SQLAlchemy database models and relations
├── seed.py                 # Idempotent database seed script for the 8 core repair guides
├── Procfile                # Gunicorn process definition for Render/Heroku
├── render.yaml             # Render Blueprint for automated web + PostgreSQL deployment
├── requirements.txt        # Production Python dependencies
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules for virtual environments, .env, and caches
├── README.md               # Complete setup, testing, and deployment guide
├── migrations/             # Alembic database migration scripts
├── static/
│   ├── css/
│   │   └── style.css       # Responsive dark automotive styling
│   └── js/
│       └── main.js         # Mobile navigation, keyboard shortcuts, wake lock
├── templates/
│   ├── base.html           # Master layout with navbar, alerts, footer
│   ├── index.html          # Public landing page
│   ├── register.html       # User registration
│   ├── login.html          # User login
│   ├── dashboard.html      # User dashboard and activity summary
│   ├── garage.html         # Garage vehicle management
│   ├── add_vehicle.html    # Add / edit vehicle form
│   ├── repairs.html        # Searchable and filterable repair library
│   ├── repair_detail.html  # Repair guide details, tools, and safety warnings
│   ├── repair_session.html # Interactive workshop step-by-step progress
│   ├── my_repairs.html     # Active and completed repair history
│   ├── profile.html        # User profile and stats
│   └── 404.html            # Error page (404, 403, 500)
└── tests/
    └── test_app.py         # Automated test suite
```

---

## 🚀 Local Setup & Development

### 1. Clone or Open the Repository
```bash
git clone <your-repo-url>
cd fixmycar-ai
```

### 2. Create and Activate a Virtual Environment
- **Windows (PowerShell)**:
  ```powershell
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  ```
- **macOS / Linux**:
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env`:
- **Windows**: `copy .env.example .env`
- **macOS / Linux**: `cp .env.example .env`

*(Note: If `DATABASE_URL` is omitted locally, the app automatically defaults to a local `sqlite:///fixmycar.db` database for fast, zero-configuration local development!)*

### 5. Initialize Database & Seed Repair Guides
```bash
flask db upgrade
python seed.py
```

### 6. Run the Application
```bash
python app.py
```
Open your browser at: **`http://localhost:5000`**

### 7. Run Automated Tests
```bash
python -m unittest tests/test_app.py
```

---

## 🚢 Deployment to GitHub & Render.com

Deploying FixMyCar AI to production with Render and a managed PostgreSQL database takes just a few minutes.

### Step 1: Create a GitHub Repository & Push Code
1. Initialize git (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit: FixMyCar AI functional web application"
   ```
2. Create a new repository on [GitHub](https://github.com/new).
3. Connect and push your code:
   ```bash
   git remote add origin https://github.com/<your-username>/<your-repo-name>.git
   git branch -M main
   git push -u origin main
   ```

---

### Step 2: Deploy to Render.com

You can deploy using either **Option A (Blueprint - 1 Click)** or **Option B (Manual Dashboard)**:

#### Option A: Deploy with Blueprint (`render.yaml`) — Recommended
1. Log in to [Render.com](https://render.com).
2. Click **New +** and select **Blueprint**.
3. Connect your GitHub repository.
4. Render will detect `render.yaml` and automatically configure:
   - A free **PostgreSQL Database** (`fixmycar-db`).
   - A **Web Service** (`fixmycar-ai`) with `buildCommand` and `startCommand`.
   - Automatic generation of a secure `SECRET_KEY`.
   - Direct connection of `DATABASE_URL` between database and web service.
5. Click **Apply**. Render will build, migrate, seed, and launch the service!

---

#### Option B: Manual Setup on Render

If configuring services manually in Render's dashboard:

##### 1. Create the PostgreSQL Database:
1. In Render Dashboard, click **New +** &rarr; **PostgreSQL**.
2. Name: `fixmycar-db`
3. Database Name: `fixmycar`
4. User: `fixmycar_user`
5. Plan: **Free**
6. Click **Create Database**.
7. Once provisioned, copy the **Internal Database URL** (e.g., `postgres://fixmycar_user:...@dpg-...-a/fixmycar`).

##### 2. Create the Web Service:
1. Click **New +** &rarr; **Web Service**.
2. Connect your GitHub repository.
3. Runtime: **Python 3**
4. Build Command:
   ```bash
   pip install -r requirements.txt && flask db upgrade && python seed.py
   ```
5. Start Command:
   ```bash
   gunicorn app:app
   ```
6. Instance Type: **Free**

##### 3. Add Environment Variables:
Under the **Environment** tab of your Web Service, add:
- `SECRET_KEY`: *A strong random string (e.g. generated via `openssl rand -hex 32`)*
- `DATABASE_URL`: *Paste the Internal Database URL from your Render PostgreSQL database*
- `PYTHON_VERSION`: `3.11.9`
- `FLASK_ENV`: `production`

> **Note on `DATABASE_URL`**: Render provides connection strings starting with `postgres://`. FixMyCar AI's `config.py` automatically detects and normalizes this to `postgresql://` as required by SQLAlchemy 2.x.

##### 4. Deploy:
Click **Save Changes** and deploy. Render will run migrations, seed the 8 repair guides, and launch Gunicorn.

---

## 🔒 Verification & Smoke Testing in Production

Once deployed, verify the complete workflow on your live Render URL:
1. **Public Landing**: Navigate to `/` and confirm hero section, "Get Started", and "Explore Repairs".
2. **Registration & Login**: Create an account; confirm secure session and flash message.
3. **Garage Management**: Add your vehicle (Make, Model, Year, Engine); test editing and deleting.
4. **Repair Catalog**: Visit `/repairs`, test category filters (Maintenance, Brakes, Electrical, etc.) and search.
5. **Start Repair Session**: Select your vehicle and start a repair guide (e.g. *Engine Oil Change*).
6. **Progress Tracking**: Step through the instructions; refresh the browser to verify your progress persists.
7. **Complete Repair**: Add notes (e.g. oil brand used) and submit; confirm it appears under `/my-repairs`.
8. **Authorization Security**: Confirm you cannot access another user's garage or repair sessions.

---

## ⚠️ Safety Disclaimer

Working on automobiles involves inherent physical, chemical, and electrical hazards. Always observe proper workshop safety rules:
- **NEVER** crawl or work underneath a car supported only by a hydraulic or scissor jack.
- **ALWAYS** use certified jack stands on level concrete and apply wheel chocks.
- Disconnect battery terminals properly (negative first, negative last).
- Complex brake hydraulics and electrical work should only be attempted if you have adequate experience; when in doubt, consult an ASE-certified technician.

---

## 📄 License
This project is open-source under the MIT License.
