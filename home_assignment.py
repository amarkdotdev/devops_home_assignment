import os
from dotenv import load_dotenv
import requests
from urllib.parse import quote

load_dotenv()

private_token = os.getenv('PAT')
gitlab_url = 'https://gitlab.com/api/v4'

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


def grant_permission(username: str, repo_or_group_name: str, role: str):
    role = role.lower()
    print(f"Granting {role} permission for {username} to {repo_or_group_name}")

    # Step 1: get user ID
    user_resp = requests.get(f"{gitlab_url}/users?username={username}", headers=HEADERS)
    user_resp.raise_for_status()
    users = user_resp.json()
    if not users:
        raise ValueError(f"User '{username}' not found")
    user_id = users[0]["id"]

    # Step 2: validate role
    access_level = GITLAB_ROLES.get(role)
    if not access_level:
        raise ValueError(f"Invalid role '{role}'")

    # Step 3: determine if it's a project or group
    encoded_name = quote(repo_or_group_name, safe='')
    is_project = requests.get(f"{gitlab_url}/projects/{encoded_name}", headers=HEADERS).status_code == 200
    scope = "project" if is_project else "group"
    base_url = f"{gitlab_url}/{scope}s/{encoded_name}/members"

    # Step 4: try to add the user directly
    add_resp = requests.post(
        base_url,
        headers=HEADERS,
        data={"user_id": user_id, "access_level": access_level}
    )

    if add_resp.status_code in (200, 201):
        return f"Added '{username}' to {scope} '{repo_or_group_name}' as '{role}'"

    # Step 5: if already a member, check current role
    if add_resp.status_code in (400, 409):
        check_resp = requests.get(f"{base_url}/{user_id}", headers=HEADERS)
        if check_resp.status_code != 200:
            return f"Failed to check current role for user '{username}'"

        current_access = check_resp.json().get("access_level")
        current_role = "unknown"
        for role_name, level in GITLAB_ROLES.items():
            if level == current_access:
                current_role = role_name
                break

        print(f"Current role in {scope} of {username} in '{repo_or_group_name}' is: '{current_role}'")
        if current_role == role:
            return f"Nothing to update - current role of {username} in '{repo_or_group_name}' is already '{role}'"

        if current_role == "owner":
            return f"'{username}' is an Owner — cannot override with lower role"

        # Step 6: Update their role
        update = requests.put(
            f"{base_url}/{user_id}",
            headers=HEADERS,
            data={"access_level": access_level}
        )
        if update.status_code in (200, 201):
            return f"Updated role in {scope} '{repo_or_group_name}' to '{role}'"
        else:
            return f"Failed to update role.\nStatus: {update.status_code}, Message: {update.text}"

    return f"Failed to add/update user.\nStatus: {add_resp.status_code}, Message: {add_resp.text}"


def get_items_by_year(item_type: str, year: int):
    if year < 1000 or year > 9999:
        print("Year must be a 4-digit number.")
        return[]

    if item_type not in ["issues", "mr"]:
        print("item_type must be either 'issues' or 'mr'")
        return []

    endpoint_url = f'{gitlab_url}/{"merge_requests" if item_type == "mr" else "issues"}'

    response = requests.get(
        endpoint_url,
        headers=HEADERS,
        params={"per_page": 100}
    )
    if response.status_code != 200:
        print(f"GitLab API error: {response.status_code}")
        return []

    data = response.json()
    relevant_items = []
    for mr_or_issue in data:
        year_of_item = int(mr_or_issue['created_at'][:4])
        if year_of_item == year:
            relevant_items.append(mr_or_issue)

    return relevant_items
