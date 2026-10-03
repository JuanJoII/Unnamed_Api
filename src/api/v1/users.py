from fastapi import APIRouter, Depends
from src.core.dependencies import DBSession
from src.services.user_service import UserServices
from src.schemas.user import UserRead

router = APIRouter(prefix="/users", tags=["users"])


def get_user_service(db: DBSession) -> UserServices:
    return UserServices(db)


@router.get("/all", response_model=list[UserRead])
def get_all_users_endpoint(
    user_service: UserServices = Depends(get_user_service),
) -> list[UserRead]:
    return user_service.get_all_users()
