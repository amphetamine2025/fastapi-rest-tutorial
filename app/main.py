from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, status
from uuid import uuid4
from datetime import datetime
from typing import List

from .models import OrderIn, Order
from .auth import create_access_token, get_current_user
from .middleware import MaxJSONMiddleware, all_exceptions_handler

app = FastAPI(title="FastAPI REST Tutorial")

# middleware
app.add_middleware(MaxJSONMiddleware)
app.add_exception_handler(Exception, all_exceptions_handler)

# In-memory DB
DB = {}

def compute_total(items):
    return sum(i.qty * i.price for i in items)

@app.post("/auth/login")
def login(creds: dict):
    if creds.get("username") != "admin" or creds.get("password") != "secret":
        raise HTTPException(status_code=401, detail="Bad credentials")
    access = create_access_token("admin", expires_minutes=15)
    return {"access_token": access, "token_type": "bearer"}

@app.post("/v1/orders", status_code=status.HTTP_201_CREATED)
def create_order(payload: OrderIn, current_user: str = Depends(get_current_user)):
    oid = str(uuid4())
    total = compute_total(payload.items)
    order = Order(id=oid, total=total, status="created", created_at=datetime.utcnow(), **payload.dict())
    DB[oid] = order
    return {"id": oid, "location": f"/v1/orders/{oid}"}

@app.get("/v1/orders", response_model=List[Order])
def list_orders(limit: int = 20, offset: int = 0, current_user: str = Depends(get_current_user)):
    return list(DB.values())[offset:offset+limit]

@app.get("/v1/orders/{order_id}", response_model=Order)
def get_order(order_id: str, current_user: str = Depends(get_current_user)):
    if order_id not in DB:
        raise HTTPException(status_code=404, detail="Not found")
    return DB[order_id]

@app.post("/v1/uploads", status_code=202)
async def upload_file(file: UploadFile = File(...)):
    job_id = str(uuid4())
    filepath = f"/tmp/{file.filename}"
    with open(filepath, "wb") as f:
        f.write(await file.read())
    return {"job_id": job_id, "filename": file.filename, "status": "processing"}
