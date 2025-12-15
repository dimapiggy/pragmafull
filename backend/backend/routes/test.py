from fastapi import APIRouter
router = APIRouter(prefix="/test")

@router.get("/ping")
def ping():
    return {"status": "ok", "message": "Server is running"}

@router.post("/echo")
def echo(data: dict):
    return {"received": True, "data": data}