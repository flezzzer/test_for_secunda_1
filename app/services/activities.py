from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.activity import Activity

def get_activity_descendants(db: Session, activity_id: int, max_depth: int = 3):
    ids = set()
    frontier = [(activity_id, 1)]
    while frontier:
        current_id, depth = frontier.pop()
        if current_id in ids:
            continue
        ids.add(current_id)
        if depth >= max_depth:
            continue
        children = db.execute(select(Activity.id).where(Activity.parent_id == current_id)).scalars().all()
        for c in children:
            frontier.append((c, depth + 1))
    return ids

def create_activity(db: Session, name: str, parent_id: int | None, max_depth: int):
    depth = 1
    current_parent = parent_id
    while current_parent:
        parent = db.get(Activity, current_parent)
        if not parent:
            raise ValueError("parent not found")
        depth += 1
        current_parent = parent.parent_id
        if depth > max_depth:
            raise ValueError(f"max depth {max_depth} exceeded")
    a = Activity(name=name, parent_id=parent_id)
    db.add(a)
    db.commit()
    db.refresh(a)
    return a
