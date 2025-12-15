from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.core.db import get_db
from backend import crud
from backend.schemas.tag import TagCreate, TagOut, TagUpdate
from backend.core.auth import get_current_user
from backend.models import User

router = APIRouter(prefix="/tags", tags=["tags"])

# Создание тега
@router.post("/", response_model=TagOut)
def create_tag(
    tag: TagCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud.tag.create_tag(db, tag, user_id=current_user.id)

# Получение всех тегов текущего пользователя
@router.get("/", response_model=list[TagOut])
def read_tags(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud.tag.get_tags_by_user(db, current_user.id)

# Получение тега по ID (только свой)
@router.get("/{tag_id}", response_model=TagOut)
def read_tag(
    tag_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_tag = crud.tag.get_tag(db, tag_id)
    if not db_tag or db_tag.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Tag not found")
    return db_tag

# Обновление тега (только своего)
@router.put("/{tag_id}", response_model=TagOut)
def update_tag(
    tag_id: int,
    tag: TagUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_tag = crud.tag.get_tag(db, tag_id)
    if not db_tag or db_tag.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Tag not found")
    return crud.tag.update_tag(db, tag_id, tag)

# Удаление тега (только своего)
@router.delete("/{tag_id}")
def delete_tag(
    tag_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_tag = crud.tag.get_tag(db, tag_id)
    if not db_tag or db_tag.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Tag not found")
    ok = crud.tag.delete_tag(db, tag_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Tag not found")
    return {"detail": "Tag deleted"}
