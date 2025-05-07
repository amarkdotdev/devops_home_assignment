import os
from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Literal
from dotenv import load_dotenv
import requests
from urllib.parse import quote
import uvicorn

load_dotenv()

app = FastAPI()

# Load secrets from .env
private_token = os.getenv("PAT")
gitlab_url = os.getenv("GITLAB_URL")

HEADERS = {
    "PRIVATE-TOKEN": private_token,
}

GITLAB_ROLES = {
    "guest": 10,
    "reporter": 20,
    "developer": 30,
    "maintainer": 40,
    "owner": 50,
}

class GrantRequest(BaseModel):
    username: str
    repo_or_group: str
    role: Literal["guest", "reporter", "developer", "maintainer", "owner"]

@app.post("/grant_permission")
def grant_access(data: GrantRequest):
    username = data.username
    repo_or_group_name = data.repo_or_group
    role = data.role.lower()

    user_resp = requests.get(f"{gitlab_url}/users?username={username}", headers=HEADERS)
    user_resp.raise_for_status()
    users = user_resp.json()
    if not users:
        return {"error": f"User '{username}' not found"}
    user_id = users[0]["id"]

    access_level = GITLAB_ROLES.get(role)
    if not access_level:
        return {"error": f"Invalid role '{role}'"}

    encoded_name = quote(repo_or_group_name, safe="")
    is_project = requests.get(f"{gitlab_url}/projects/{encoded_name}", headers=HEADERS).status_code == 200
    scope = "project" if is_project else "group"
    base_url = f"{gitlab_url}/{scope}s/{encoded_name}/members"

    add_resp = requests.post(
        base_url,
        headers=HEADERS,
        data={"user_id": user_id, "access_level": access_level},
    )

    if add_resp.status_code in (200, 201):
        return {"result": f"Added '{username}' to {scope} '{repo_or_group_name}' as '{role}'"}

    if add_resp.status_code in (400, 409):
        check_resp = requests.get(f"{base_url}/{user_id}", headers=HEADERS)
        if check_resp.status_code != 200:
            return {"error": f"Failed to check current role for '{username}'"}

        current_access = check_resp.json().get("access_level")
        current_role = next((r for r, lvl in GITLAB_ROLES.items() if lvl == current_access), "unknown")

        if current_role == role:
            return {"result": f"No update needed — current role of '{username}' is already '{role}'"}
        if current_role == "owner":
            return {"error": f"'{username}' is an Owner — cannot override with lower role"}

        update = requests.put(
            f"{base_url}/{user_id}",
            headers=HEADERS,
            data={"access_level": access_level},
        )
        if update.status_code in (200, 201):
            return {"result": f"Updated role in {scope} '{repo_or_group_name}' to '{role}'"}
        return {"error": f"Failed to update role: {update.text}"}

    return {"error": f"Failed to add/update user: {add_resp.text}"}


@app.get("/get_items_by_year")
def fetch_items(item_type: Literal["issues", "mr"], year: int = Query(..., ge=1000, le=9999)):
    endpoint = "merge_requests" if item_type == "mr" else "issues"
    response = requests.get(f"{gitlab_url}/{endpoint}", headers=HEADERS, params={"per_page": 100})
    if response.status_code != 200:
        return {"error": f"GitLab API error: {response.status_code}"}

    data = response.json()
    relevant_items = [item for item in data if int(item["created_at"][:4]) == year]
    return {"count": len(relevant_items), "items": relevant_items}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8443,
                ssl_keyfile="certs/key.pem", ssl_certfile="certs/cert.pem")
