from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.core.db import get_db
from backend import crud
from backend.schemas.sphere import SphereCreate, SphereOut, SphereUpdate
from backend.models.user import User
from backend.core.auth import get_current_user

router = APIRouter(prefix="/spheres", tags=["spheres"])

@router.post("/", response_model=SphereOut)
def create_sphere(
    sphere: SphereCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud.sphere.create_sphere(db, sphere, user_id=current_user.id)

@router.get("/", response_model=list[SphereOut])
def read_spheres(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud.sphere.get_spheres_by_user(db, user_id=current_user.id)

@router.get("/{sphere_id}", response_model=SphereOut)
def read_sphere(sphere_id: int, db: Session = Depends(get_db)):
    db_sphere = crud.sphere.get_sphere(db, sphere_id)
    if not db_sphere:
        raise HTTPException(status_code=404, detail="Sphere not found")
    return db_sphere

@router.put("/{sphere_id}", response_model=SphereOut)
def update_sphere(sphere_id: int, sphere: SphereUpdate, db: Session = Depends(get_db)):
    db_sphere = crud.sphere.update_sphere(db, sphere_id, sphere)
    if not db_sphere:
        raise HTTPException(status_code=404, detail="Sphere not found")
    return db_sphere

@router.delete("/{sphere_id}")
def delete_sphere(sphere_id: int, db: Session = Depends(get_db)):
    ok = crud.sphere.delete_sphere(db, sphere_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Sphere not found")
    return {"detail": "Sphere deleted"}
