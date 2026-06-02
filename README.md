# my-web-gis

A web GIS app that collects telemetry from a mobile device
(GPS + accelerometer) and shows it on an interactive map.


## About
 
**MyWebGIS** is a learning and portfolio app. It shows the full cycle of
working with geospatial data on the web: a logged-in user sends GPS
location and accelerometer data from their phone, the server saves it in
PostGIS, and a Leaflet map shows the collected layers.
 
The project demonstrates a typical GIS development stack: FastAPI on the
backend, PostgreSQL + PostGIS to store geometry, and Leaflet for
visualization.
 
---
 
## Features
 
**Implemented:**
- Public pages (home, map, contacts)
- Interactive map with Leaflet
- Telemetry collection page on the phone (GPS + accelerometer)
- Telemetry storage in PostGIS
- JWT authentication and authorization
- Linking telemetry to a user in the database

**Planned:**
- Showing collected tracks on the map
- Post-processing and geo-analysis of the collected data
- Public dashboards with analytics
---
 
## Tech Stack
 
**Backend**
- [FastAPI](https://fastapi.tiangolo.com/) — web framework
- [SQLAlchemy 2.x](https://www.sqlalchemy.org/) — ORM
- [GeoAlchemy2](https://geoalchemy-2.readthedocs.io/) — geometry support in the ORM
- [Alembic](https://alembic.sqlalchemy.org/) — database migrations
- [Pydantic v2](https://docs.pydantic.dev/) — data validation

**Database**
- PostgreSQL + [PostGIS](https://postgis.net/) (hosted on Supabase)

**Frontend**
- Vanilla JavaScript
- [Leaflet 1.9.4](https://leafletjs.com/) — interactive maps
- Static HTML / CSS

**Other**
- Python 3.10
---
 
## Quick Start
 
### Requirements
- Python 3.10+
- PostgreSQL 16 with the PostGIS 3.4 extension (or a [Supabase](https://supabase.com/) account)
- Git
### Setup (Windows / PowerShell)
 
```powershell
# 1. Clone the repository
git clone https://github.com/<your-username>/my-web-gis.git
 
# 2. Create and activate a virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1
 
# 3. Install dependencies
pip install -r requirements.txt
 
# 4. Set up the environment
Copy-Item .env.example .env
 
# 5. Apply migrations
alembic upgrade head
 
# 6. Run the server
python -m uvicorn app.main:app --reload
```
 
### Setup (macOS / Linux)
 
```bash
git clone https://github.com/<your-username>/my-web-gis.git
 
python -m venv venv
source venv/bin/activate
 
pip install -r requirements.txt
 
cp .env.example .env 
 
alembic upgrade head
 
python -m uvicorn app.main:app --reload
```
 
After it starts, the app is available at
**http://127.0.0.1:8000**
 
> **Collecting telemetry from a phone.** Browser sensors (geolocation,
> accelerometer) work only in a secure context (HTTPS) or on
> `localhost`. To test from a real phone on your local network, run the
> server with `--host 0.0.0.0` and use an HTTPS tunnel
> (for example, [ngrok](https://ngrok.com/)).
 
---
 
## Project Structure
 
```
my-web-gis/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI app + endpoints
│   │   ├── database.py      # database connection
│   │   ├── models/          # SQLAlchemy ORM models
│   │   └── schemas/         # Pydantic schemas
│   ├── alembic/             # database migrations
│   └── .env.example         # environment variables template
└── frontend/
    ├── index.html           # home page
    ├── map.html             # Leaflet map
    ├── track.html           # telemetry collection
    ├── login.html / register.html
    ├── css/
    └── js/
```
 
---
 
## License
 
Distributed under the license in the [LICENSE](LICENSE) file.
 
---
 
## Contact
 
Questions and suggestions: **GIS2011I@gmail.com**
