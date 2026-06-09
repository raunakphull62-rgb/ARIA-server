# server/main.py
from fastapi import FastAPI
from server.database import engine, Base
from server.routes import health, packages, stats

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ARIA Registry", version="1.0")

app.include_router(health.router)
app.include_router(packages.router)
app.include_router(stats.router)

@app.get("/")
def root():
    from server.database import SessionLocal
    from server.models import Package
    db = SessionLocal()
    count = db.query(Package).count()
    db.close()
    return {"name": "ARIA Registry", "version": "1.0", "total_packages": count}
