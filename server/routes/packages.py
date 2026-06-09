# server/routes/packages.py
from fastapi import APIRouter, HTTPException, Query
from server.database import SessionLocal
from server.models import Package
from pydantic import BaseModel
from typing import Optional, List

router = APIRouter(prefix="/packages", tags=["packages"])

class PackagePublish(BaseModel):
    name: str
    version: str
    description: Optional[str] = None
    author: Optional[str] = None
    github_url: Optional[str] = None
    download_url: Optional[str] = None
    manifest_json: Optional[str] = None

@router.get("")
def list_packages(search: Optional[str] = Query(None)):
    db = SessionLocal()
    if search:
        packages = db.query(Package).filter(Package.name.contains(search)).all()
    else:
        packages = db.query(Package).all()
    db.close()
    return [{"name": p.name, "version": p.version, "description": p.description,
             "author": p.author, "install_count": p.install_count} for p in packages]

@router.get("/{name}")
def get_package(name: str):
    db = SessionLocal()
    pkg = db.query(Package).filter(Package.name == name).first()
    db.close()
    if not pkg:
        raise HTTPException(status_code=404, detail="Package not found")
    return {"name": pkg.name, "version": pkg.version, "description": pkg.description,
            "author": pkg.author, "github_url": pkg.github_url, "download_url": pkg.download_url,
            "install_count": pkg.install_count, "manifest": pkg.manifest_json}

@router.post("/publish")
def publish_package(pkg: PackagePublish):
    db = SessionLocal()
    existing = db.query(Package).filter(Package.name == pkg.name).first()
    if existing:
        existing.version = pkg.version
        existing.description = pkg.description
        existing.author = pkg.author
        existing.github_url = pkg.github_url
        existing.download_url = pkg.download_url
        existing.manifest_json = pkg.manifest_json
        db.commit()
        db.refresh(existing)
        db.close()
        return {"message": "Package updated", "name": existing.name}
    new_pkg = Package(name=pkg.name, version=pkg.version, description=pkg.description,
                      author=pkg.author, github_url=pkg.github_url, download_url=pkg.download_url,
                      manifest_json=pkg.manifest_json)
    db.add(new_pkg)
    db.commit()
    db.refresh(new_pkg)
    db.close()
    return {"message": "Package published", "name": new_pkg.name}

@router.post("/{name}/install")
def install_package(name: str):
    db = SessionLocal()
    pkg = db.query(Package).filter(Package.name == name).first()
    if not pkg:
        db.close()
        raise HTTPException(status_code=404, detail="Package not found")
    pkg.install_count += 1
    db.commit()
    db.close()
    return {"name": pkg.name, "install_count": pkg.install_count}
