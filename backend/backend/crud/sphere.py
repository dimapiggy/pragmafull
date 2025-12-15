from sqlalchemy.orm import Session
from backend.models.sphere import Sphere
from backend.schemas.sphere import SphereCreate, SphereUpdate

def create_sphere(db: Session, sphere: SphereCreate, user_id: int) -> Sphere:
    db_sphere = Sphere(**sphere.dict(), user_id=user_id)
    db.add(db_sphere)
    db.commit()
    db.refresh(db_sphere)
    return db_sphere

def get_spheres(db: Session) -> list[Sphere]:
    return db.query(Sphere).all()

def get_spheres_by_user(db: Session, user_id: int) -> list[Sphere]:
    return db.query(Sphere).filter(Sphere.user_id == user_id).all()

def get_sphere(db: Session, sphere_id: int) -> Sphere | None:
    return db.query(Sphere).filter(Sphere.id == sphere_id).first()

def update_sphere(db: Session, sphere_id: int, sphere: SphereUpdate) -> Sphere | None:
    db_sphere = db.query(Sphere).filter(Sphere.id == sphere_id).first()
    if not db_sphere:
        return None
    for field, value in sphere.dict(exclude_unset=True).items():
        setattr(db_sphere, field, value)
    db.commit()
    db.refresh(db_sphere)
    return db_sphere

def delete_sphere(db: Session, sphere_id: int) -> bool:
    db_sphere = db.query(Sphere).filter(Sphere.id == sphere_id).first()
    if not db_sphere:
        return False
    db.delete(db_sphere)
    db.commit()
    return True
