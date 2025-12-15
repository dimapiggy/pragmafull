from sqlalchemy.orm import Session
from backend.models.tag import Tag
from backend.schemas.tag import TagCreate, TagUpdate

def create_tag(db: Session, tag: TagCreate, user_id: int) -> Tag:
    db_tag = Tag(**tag.dict(), user_id=user_id)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

def get_tags_by_user(db: Session, user_id: int) -> list[Tag]:
    return db.query(Tag).filter(Tag.user_id == user_id).all()

def get_tag(db: Session, tag_id: int) -> Tag | None:
    return db.query(Tag).filter(Tag.id == tag_id).first()
 
def update_tag(db: Session, tag_id: int, tag: TagUpdate) -> Tag | None:
    db_tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not db_tag:
        return None
    for field, value in tag.dict(exclude_unset=True).items():
        setattr(db_tag, field, value)
    db.commit()
    db.refresh(db_tag)
    return db_tag

def delete_tag(db: Session, tag_id: int) -> bool:
    db_tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not db_tag:
        return False
    db.delete(db_tag)
    db.commit()
    return True
