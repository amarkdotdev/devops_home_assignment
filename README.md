# 🔐 GitLab Permissions & History — HTTPS API Service (FastAPI + Uvicorn via Docker)

A secure **FastAPI**-based microservice to:

1. 🚀 Grant GitLab user permissions on projects or groups
2. 🗓️ Fetch issues or merge requests by year

Now served over **HTTPS** via **Uvicorn** inside a **Docker** container!

---

## 💪 Features

* 🔒 HTTPS secured API (self-signed or real certs)
* 🎓 Grant GitLab access levels: `guest`, `reporter`, `developer`, `maintainer`, `owner`
* 🕒 Query GitLab for issues or merge requests by year
* 💪 FastAPI backend with automatic `/docs`
* 🐿 Lightweight, production-ready Docker image
* 🔐 Uses `.env` file for secrets

---

## 📁 Project Structure

```
devops_home_assignment/
├── main.py             # FastAPI app with 2 routes
├── run_https.py        # HTTPS server entrypoint using Uvicorn
├── home_assignment.py  # Core GitLab logic (API requests)
├── entrypoint.py       # Optional CLI fallback
├── Dockerfile          # Alpine-based Docker setup
├── requirements.txt    # Python deps
├── certs/              # SSL cert + key
│   ├── cert.pem
│   └── key.pem
├── .env                # GitLab PAT + URL (not committed)
└── README.md
```

---

## 🔐 SSL Certificate Setup

Use your own cert, or generate a self-signed one (for localhost testing):

```bash
mkdir -p certs
openssl req -x509 -newkey rsa:4096 -nodes \
  -keyout certs/key.pem -out certs/cert.pem \
  -days 365 -subj "/CN=localhost"
```

---

## 🚀 Run with Docker

### 1. Clone the repo

```bash
git clone https://github.com/amarkdotdev/devops_home_assignment.git
cd devops_home_assignment
```

### 2. Add a `.env` file

```env
PAT=your_gitlab_token_here
GITLAB_URL=https://gitlab.com/api/v4
```

### 3. Build the Docker image

```bash
docker build -t gitlab-tool-https .
```

### 4. Run it (HTTPS on port 8443)

```bash
docker run -p 8443:8443 --env-file .env gitlab-tool-https
```

Then visit:

* 🔗 [https://localhost:8443/docs](https://localhost:8443/docs)

> Accept browser warning if using self-signed certs.

---

## 🔎 API Endpoints

### POST `/grant_permission`

Grants a GitLab user a role in a group/project.

**Request Body:**

```json
{
  "username": "aaronofjm",
  "repo_or_group": "mobileye_group_VPs",
  "role": "developer"
}
```

**Response:**

```json
{
  "result": "Added 'aaronofjm' to group 'mobileye_group_VPs' as 'developer'"
}
```

---

### GET `/get_items_by_year`

Returns all issues/MRs from a given year.

**Query Parameters:**

* `item_type`: `issues` or `mr`
* `year`: e.g. `2025`

**Example:**

```
GET https://localhost:8443/get_items_by_year?item_type=issues&year=2025
```

**Response:**

```json
{
  "count": 5,
  "items": [
    { "id": 123, "title": "Fix X", "created_at": "2025-01-12T..." },
  ]
}
```

---

## 🔄 CLI Mode (Optional)

Still supported:

```bash
docker run --env-file .env gitlab-tool-https grant_permission aaronofjm mobileye_group_VPs developer
docker run --env-file .env gitlab-tool-https get_items_by_year issues 2025
```

---

## 🔒 Security Notes

* Do NOT commit your `.env` or real certs
* Use valid TLS certs for production (Let's Encrypt or org-issued)
* Use authentication or IP restrictions in production environments

---

📝 *Built with heart by Aaron Mark — wish me luck!* 🚀
