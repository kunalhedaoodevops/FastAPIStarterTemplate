from calendar import c
import typer
from pathlib import Path
from rich import print
from rich.prompt import Prompt, Confirm

app = typer.Typer(help="FastAPI generator CLI")
component_app = typer.Typer(help="Generate FastAPI components")
app.add_typer(component_app, name="component")

BASE_DIR = Path("app")

# ======================================================
# FIELD HELPERS (NO PRICE)
# ======================================================

FIELD_TYPES = {
    "string": "String(255)",
    "text": "Text",
    "int": "Integer",
    "bool": "Boolean",
}

def ask_fields():
    fields = [
        ("title", "String(255)", False),
        ("description", "Text", True),
    ]

    print("[cyan]Default fields:[/cyan] title, description")

    if Confirm.ask("Add custom fields?", default=False):
        while True:
            name = Prompt.ask("Field name")
            ftype = Prompt.ask("Field type", choices=list(FIELD_TYPES.keys()))
            nullable = Confirm.ask("Nullable?", default=True)
            fields.append((name, FIELD_TYPES[ftype], nullable))

            if not Confirm.ask("Add another field?", default=False):
                break

    return fields

# ======================================================
# MODEL TEMPLATE
# ======================================================
def to_class_name(raw: str) -> str:
    return "".join(word.capitalize() for word in raw.replace("-", "_").split("_"))

def model_template(name, fields):
    lname = name.lower()
    imports = {t.split("(")[0] for _, t, _ in fields}

    columns = "\n".join(
        f"    {f} = Column({t}, nullable={n})"
        for f, t, n in fields
    )
    class_name = to_class_name(name)
    return f'''from sqlalchemy import Column, Integer, ForeignKey, {", ".join(imports)}
from sqlalchemy.orm import relationship
from .base import Base

class {class_name}(Base):
    __tablename__ = "{lname}s"

    id = Column(Integer, primary_key=True, index=True)
{columns}
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="{lname}s")
'''

# ======================================================
# SCHEMA TEMPLATE (NO IMPORTS INSIDE)
# ======================================================

def schema_template(name, fields):
    def map_type(t):
        if "String" in t or "Text" in t:
            return "Optional[str]"
        if "Integer" in t:
            return "Optional[int]"
        if "Boolean" in t:
            return "Optional[bool]"
        return "Optional[str]"

    props = "\n".join(
        f"    {f}: {map_type(t)} = None"
        for f, t, _ in fields
    )

    return f'''
class {name}Base(BaseModel):
{props}

class {name}Create({name}Base):
    pass

class {name}Update({name}Base):
    pass

class {name}Out({name}Base):
    id: int
    owner_id: int

    class Config:
        from_attributes = True
'''.strip()

# ======================================================
# SCHEMA WRITER (IMPORT SAFE)
# ======================================================

def write_schema(name, fields):
    schemas_path = BASE_DIR / "databases" / "schemas.py"
    schemas_path.parent.mkdir(exist_ok=True)

    base_imports = """from pydantic import BaseModel
from typing import Optional
"""

    schema_block = schema_template(name, fields)

    if not schemas_path.exists() or not schemas_path.read_text().strip():
        schemas_path.write_text(base_imports + "\n\n" + schema_block + "\n")
        return

    existing = schemas_path.read_text()

    if f"class {name}Base" in existing:
        print(f"[yellow]⚠ Schema {name} already exists, skipping[/yellow]")
        return

    updated = existing.rstrip()

    if "from pydantic import BaseModel" not in existing:
        updated = base_imports + "\n\n" + updated

    updated += "\n\n\n" + schema_block + "\n"
    schemas_path.write_text(updated)

# ======================================================
# SERVICE TEMPLATE (NO PRICE)
# ======================================================

def service_template(name):
    lname = name.lower()
    class_name = to_class_name(lname)
    return f'''from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from app.databases import schemas
from app.models.{lname}s import {class_name} as {name}

def create_{lname}(db: Session, owner_id: int, item: schemas.{name}Create):
    obj = {name}(**item.dict(), owner_id=owner_id)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_{lname}(db: Session, item_id: int):
    return db.query({name}).filter({name}.id == item_id).first()

def update_{lname}(db: Session, obj: {name}, changes: schemas.{name}Update):
    for k, v in changes.dict(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

def delete_{lname}(db: Session, obj: {name}):
    db.delete(obj)
    db.commit()

def list_{lname}s(db, skip=0, limit=10, search=None, owner_id=None):
    q = db.query({name})

    if search:
        q = q.filter({name}.title.ilike(f"%{{search}}%"))

    if owner_id:
        q = q.filter({name}.owner_id == owner_id)

    return q.offset(skip).limit(limit).all(), q.count()

def portable_search(db, q=None, owner_id=None, cursor=None, limit=20):
    query = db.query({name})

    if q:
        q = q.lower().strip()
        query = query.filter(
            or_(
                func.lower({name}.title).startswith(q),
                func.lower({name}.description).startswith(q),
            )
        )

    if owner_id:
        query = query.filter({name}.owner_id == owner_id)

    if cursor:
        query = query.filter({name}.id > cursor)

    return query.order_by({name}.id).limit(min(limit, 100)).all()
'''

# ======================================================
# ROUTER TEMPLATE (ITEMS STYLE, NO PRICE)
# ======================================================

def router_template(name):
    lname = name.lower()
    class_name = to_class_name(lname)

    return f'''from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.databases import schemas
from app.services import {class_name}s_Service as {name}s_Service
from app.databases.db import get_db
from app.utils.deps import get_current_user
from fastapi_cache.decorator import cache

router = APIRouter(prefix='/{lname}s', tags=['{class_name}s'])

@router.post('/', response_model=schemas.{name}Out)
@cache(expire=30)
def create_{lname}(
    item_in: schemas.{name}Create,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return {name}s_Service.create_{lname}(db, current_user.id, item_in)

@router.get('/search', response_model=List[schemas.{name}Out])
@cache(expire=10)
def search_{lname}s(
    q: Optional[str] = None,
    owner_id: Optional[int] = None,
    cursor: Optional[int] = None,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    return {name}s_Service.portable_search(db, q, owner_id, cursor, limit)

@router.get('/{{item_id}}', response_model=schemas.{name}Out)
def read_{lname}(item_id: int, db: Session = Depends(get_db)):
    obj = {name}s_Service.get_{lname}(db, item_id)
    if not obj:
        raise HTTPException(status_code=404, detail='{name} not found')
    return obj

@router.get('/', response_model=List[schemas.{name}Out])
def list_{lname}s(
    page: int = 1,
    size: int = 10,
    search: Optional[str] = None,
    owner_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    skip = (page - 1) * size
    items, _ = {name}s_Service.list_{lname}s(db, skip, size, search, owner_id)
    return items

# ======================================================
# UPDATE
# ======================================================

@router.patch('/{{item_id}}', response_model=schemas.{name}Out)
def update_{lname}(
    item_id: int,
    changes: schemas.{name}Update,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    obj = {name}s_Service.get_{lname}(db, item_id)

    if not obj:
        raise HTTPException(status_code=404, detail='{name} not found')

    if obj.owner_id != current_user.id and current_user.role != 'admin':
        raise HTTPException(status_code=403, detail='Not permitted')

    return {name}s_Service.update_{lname}(db, obj, changes)

# ======================================================
# DELETE
# ======================================================

@router.delete('/{{item_id}}', status_code=204)
def delete_{lname}(
    item_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    obj = {name}s_Service.get_{lname}(db, item_id)

    if not obj:
        raise HTTPException(status_code=404, detail='{name} not found')

    if obj.owner_id != current_user.id and current_user.role != 'admin':
        raise HTTPException(status_code=403, detail='Not permitted')

    {name}s_Service.delete_{lname}(db, obj)
    return None
'''

# ======================================================
# USER RELATIONSHIP APPENDER
# ======================================================

def append_user_relationship(component_name: str):
    user_model_path = BASE_DIR / "models" / "users.py"

    if not user_model_path.exists():
        print("[yellow]⚠ users.py not found, skipping User relationship[/yellow]")
        return

    lname = component_name.lower()
    rel_name = f"{lname}s"  # e.g. tests, products
    class_name = to_class_name(component_name)
    content = user_model_path.read_text()

    # ✅ Skip if relationship already exists
    if f"{rel_name} = relationship(" in content:
        print(f"[yellow]⚠ User.{rel_name} already exists, skipping[/yellow]")
        return

    # ✅ Ensure relationship import exists
    if "from sqlalchemy.orm import relationship" not in content:
        content = content.replace(
            "from sqlalchemy import",
            "from sqlalchemy import\nfrom sqlalchemy.orm import relationship",
        )

    lines = content.splitlines()
    output = []
    inside_user = False
    inserted = False

    for line in lines:
        output.append(line)

        # Detect User class
        if line.startswith("class User"):
            inside_user = True
            continue

        # Insert relationship after existing relationships
        if inside_user and line.strip().startswith("items = relationship"):
            output.append(
                f"    {rel_name} = relationship('{class_name}', back_populates='owner')"
            )
            inserted = True
            inside_user = False  # insert only once

    # Fallback: if User has no relationships block
    if not inserted:
        output = []
        inside_user = False
        for line in lines:
            output.append(line)
            if line.startswith("class User"):
                inside_user = True
            elif inside_user and line.strip() == "":
                output.append(
                    f"    {rel_name} = relationship('{class_name}', back_populates='owner')"
                )
                break

    user_model_path.write_text("\n".join(output))
    print(f"[green]✔ Added User.{rel_name} relationship[/green]")


# ======================================================
# CLI COMMAND
# ======================================================

@component_app.command("create")
def create(name: str):
    print(f"[green]Generating {name} component[/green]")
    class_name = to_class_name(name.lower())
    fields = ask_fields()

    (BASE_DIR / "models").mkdir(exist_ok=True)
    (BASE_DIR / "services").mkdir(exist_ok=True)
    (BASE_DIR / "routes").mkdir(exist_ok=True)
    (BASE_DIR / "databases").mkdir(exist_ok=True)

    (BASE_DIR / "models" / f"{name.lower()}s.py").write_text(
        model_template(name, fields)
    )
    append_user_relationship(name)
    (BASE_DIR / "services" / f"{class_name}s_Service.py").write_text(
        service_template(name)
    )
    (BASE_DIR / "routes" / f"{name.lower()}s.py").write_text(
        router_template(name)
    )
    write_schema(name, fields)

    print("[bold green]✔ Component created successfully[/bold green]")

if __name__ == "__main__":
    app()
