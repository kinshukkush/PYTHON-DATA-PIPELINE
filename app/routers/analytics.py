from fastapi import APIRouter
from ..models import AnalyticsSummary
from ..services.analytics_service import get_analytics_summary

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/summary", response_model=AnalyticsSummary)
def analytics_summary():
    return get_analytics_summary()
