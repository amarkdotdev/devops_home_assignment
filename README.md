
# 🔧 GitLab Permissions & History CLI Tool (Dockerized)

A lightweight CLI utility (in Docker) for:
1. **Granting a GitLab user a specific role on a project or group**
2. **Fetching all issues or merge requests created in a given year**

Built in Python, using the GitLab API v15.11, and packaged in a minimal Alpine-based Docker container.

---

## 📦 Features

- 🛡️ Grant or update permissions (`guest`, `reporter`, `developer`, `maintainer`, `owner`) to a user on a GitLab project or group
- 🕒 Fetch all issues or merge requests created in a specific year
- 🐳 Dockerized CLI for consistent, secure usage
- 🔐 Uses `.env` file for secure token access

---

## 🧱 Project Structure

```
devops_home_assignment/
├── home_assignment.py      # Core logic functions
├── entrypoint.py           # CLI parser and dispatcher
├── Dockerfile              # Alpine-based Docker image
├── requirements.txt        # Python deps (requests, dotenv)
└── .env                    # Private token (ignored by git)
```

---

## 🧪 The Functions

### 1. `grant_permission(username, repo_or_group, role)`
Grants or updates the user's access role (e.g., `developer`) on the specified GitLab **project** or **group**.

- If the user is already a member, updates their role (unless they're Owner).
- If not, adds them directly.

Example:
```bash
grant_permission("aaronofjm", "mobileye_group_VPs", "developer")
```

---

### 2. `get_items_by_year(item_type, year)`
Fetches **issues** or **merge requests** created in the specified year.

- `item_type`: `"issues"` or `"mr"`
- `year`: 4-digit year like `2024`

Example:
```bash
get_items_by_year("issues", 2025)
```

---

## 🚀 Run it with Docker

### 1. Clone this repo

```bash
git clone https://github.com/amarkdotdev/devops_home_assignment.git
cd devops_home_assignment
```

### 2. Add your GitLab token to `.env`

Create a `.env` file:
```
PAT=your_gitlab_token_here
```

> Your token must have `api` scope.

---

### 3. Build the Docker image

```bash
docker build -t gitlab-tool .
```

---

### 4. Run it!

#### ✅ Grant permission to a user:
```bash
docker run --env-file .env gitlab-tool grant_permission aaronofjm mobileye_group_VPs reporter
```

#### ✅ Fetch issues or MRs from a year:
```bash
docker run --env-file .env gitlab-tool get_items_by_year issues 2025
docker run --env-file .env gitlab-tool get_items_by_year mr 2023
```

---

📝 *I hope I get the job!*  
— Aaron Mark