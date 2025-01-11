from fastapi import APIRouter, Depends

from application.auth.auth_service import AuthService

admin_router = APIRouter()


@admin_router.get("/stats", dependencies=[Depends(AuthService.is_admin)])
async def admin_stats():
    stats = {"users": 100, "products": 50}
    return stats
