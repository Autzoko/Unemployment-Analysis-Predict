# Web Application for U.S. Unemployment Analysis and Predict

## Backend
use FastAPI + PyMongo
# Run
```bash
PYTHONPATH=src uvicorn src.main:app --host 0.0.0.0 --port 8000
```
under `./backend`.

## Frontend
use Vue + Vite
### Run
```bash
npm run dev
```
under `./frontend'`

## Docker
The frontend, backend, and MongoDB services are encapsulated in different docker containers for easier deploy. Use `docker-compose` command to deploy together.
Run
```bash
docker-compose up -d --build
```
to deploy.

