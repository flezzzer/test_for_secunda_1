from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.activity import Activity, ActivityCreate
from app.services.activities import create_activity, get_activity_descendants
from app.core.deps import get_db, require_api_key
from app.core.config import settings
from typing import List

router = APIRouter(dependencies=[Depends(require_api_key)])

@router.post("/", response_model=Activity)
def create_activity_api(a: ActivityCreate, db: Session = Depends(get_db)):
    """
    Создаёт новую активность.

    Этот эндпоинт позволяет добавить новый вид деятельности в справочник.
    Можно указать родительскую активность, чтобы построить дерево деятельности.
    Максимальная глубина вложенности ограничена настройкой `MAX_ACTIVITY_DEPTH`.

    **Params**:
    - **x-api-key (str)**: API-ключ, передаваемый в заголовке запроса. Должен совпадать с ключом из `.env`.

   **Returns**:
    - **Activity**: Созданная активность с её ID и родителем

     **Body**:
    - **name (str)**: Название активности
    - **parent_id (int)**: ID родителя (любое значение из имеющихся id, чтобы построить дерево, либо же null)

    **Raises**:
        HTTPException: Если превышена максимальная глубина вложенности или переданы некорректные данные.
    """
    try:
        return create_activity(db, a.name, a.parent_id, settings.MAX_ACTIVITY_DEPTH)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{activity_id}/descendants", response_model=List[int])
def get_descendants(activity_id: int, db: Session = Depends(get_db)):
    """
    Возвращает список всех потомков указанной активности.

    Позволяет получить все подвиды деятельности, которые вложены в указанную активность.
    Используется, например, для поиска организаций по деятельности с учётом подвидов.

    **Params**:
    - **x-api-key (str)**: API-ключ, передаваемый в заголовке запроса. Должен совпадать с ключом из `.env`.
    - **activity_id (int)**: ID родительской активности.

   **Returns**:
    - **List[int]**: Список ID всех потомков активности.
    """
    return list(get_activity_descendants(db, activity_id, settings.MAX_ACTIVITY_DEPTH))

