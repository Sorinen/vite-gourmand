from fastapi import APIRouter, Depends
from app.services.stats_service import get_stats_par_menu
from app.utils.dependencies import require_role

router = APIRouter(prefix="/admin/stats", tags=["stats"])

@router.get("/commandes-par-menu")
async def stats_commandes_par_menu(
    current_user=Depends(require_role("Administrateur"))
):
    return await get_stats_par_menu()