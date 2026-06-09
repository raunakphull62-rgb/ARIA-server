# server/routes/stats.py
from fastapi import APIRouter
from server.database import SessionLocal
from server.models import Package

router = APIRouter(tags=["stats"])

@router.get("/stats")
def get_stats():
    db = SessionLocal()
    total = db.query(Package).count()
    total_installs = sum(p.install_count for p in db.query(Package).all())
    popular = db.query(Package).order_by(Package.install_count.desc()).limit(5).all()
    db.close()
    return {
        "total_packages": total,
        "total_installs": total_installs,
        "most_popular": [{"name": p.name, "installs": p.install_count} for p in popular]
    }

@router.get("/featured")
def featured():
    # Hardcoded for now
    return [
        {"name": "aria-git-advanced", "description": "Advanced git operations"},
        {"name": "aria-docker-tool", "description": "Docker management via NL"},
        {"name": "aria-code-writer", "description": "AI writes and saves code"}
    ]
