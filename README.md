# FastAPI REST Tutorial

A hands-on tutorial project demonstrating REST API patterns (CRUD, JWT auth, file uploads, payload size limits).

## 🚀 Features
- CRUD Orders API
- JWT authentication
- JSON payload limit (3MB) → multipart/form-data uploads
- Error handling with correlation IDs
- Ready-to-run tests

## 🔧 Local Development

### 1. Clone & Install
```bash
git clone https://github.com/yourname/fastapi-rest-tutorial.git
cd fastapi-rest-tutorial
pip install -r requirements.txt
```

### 2. Run
```bash
uvicorn app.main:app --reload --port 8000
```
Visit: http://localhost:8000/docs

### 3. Login
```bash
curl -X POST http://localhost:8000/auth/login   -H "Content-Type: application/json"   -d '{"username":"admin","password":"secret"}'
```

Use `access_token` for Bearer Auth.

## 🐳 Run with Docker
```bash
docker build -t fastapi-rest-tutorial .
docker run -p 8000:80 fastapi-rest-tutorial
```

## ✅ Run Tests
```bash
pytest -v
```

## 📂 Example: Upload large JSON
If payload > 3 MB:
```bash
curl -X POST http://localhost:8000/v1/uploads   -F "file=@big_payload.json"
```
Response: `{"job_id":"...","filename":"big_payload.json","status":"processing"}`
