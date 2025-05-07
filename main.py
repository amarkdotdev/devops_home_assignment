# main.py
from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Literal
from home_assignment import grant_permission, get_items_by_year

app = FastAPI()

class GrantRequest(BaseModel):
    username: str
    repo_or_group: str
    role: Literal["guest", "reporter", "developer", "maintainer", "owner"]

@app.post("/grant_permission")
def grant_access(data: GrantRequest):
    result = grant_permission(data.username, data.repo_or_group, data.role)
    return {"result": result}

@app.get("/get_items_by_year")
def fetch_items(item_type: Literal["issues", "mr"], year: int = Query(..., ge=1000, le=9999)):
    items = get_items_by_year(item_type, year)
    return {"count": len(items), "items": items}
