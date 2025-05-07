# 🚀 GitLab Permissions & History – **HTTPS Microservice**

A one‑file **FastAPI** service (served by Uvicorn over **HTTPS**) that lets you:

1. **Grant** a GitLab user a role on a project *or* group  
2. **Query** all issues or merge‑requests created in a given year  

Packaged in a tiny Alpine‑based **Docker** image.  
➡️ **Self‑signed TLS certs are generated automatically during the build!**

---

## Highlights

| Feature | Details |
|---------|---------|
| 🔐 **Zero‑touch HTTPS** | Dockerfile runs `openssl` to create `cert.pem` + `key.pem` inside the image. |
| ⚡ **FastAPI + Uvicorn** | Async‑ready Python 3.11 stack, auto‑docs at `/docs`. |
| 🐳 **Instant Docker** | `docker run -p 8443:8443 …` and you’re live. |
| 🔐 **.env‑driven secrets** | GitLab PAT & URL loaded with `python‑dotenv`. |
| 📝 **Swagger UI** | Perfect for demos & manual testing. |

---

## 📂 Project Structure (annotated)

```text
devops_home_assignment/
├── Dockerfile          # Builds the image & auto‑generates self‑signed certs
├── requirements.txt    # Python deps
├── main.py             # FastAPI app (<250 LOC): API + GitLab logic + TLS launch
├── .env.example        # Template for secrets (PAT, GITLAB_URL)
└── README.md           # You’re reading it 🙂
```

> **Note:** `certs/` is created *inside the image*; no keys are stored in git.

---

## 🚀 Quick Start

```bash
# 1 · Clone
git clone https://github.com/amarkdotdev/devops_home_assignment.git
cd devops_home_assignment

# 2 · Secrets
cp .env.example .env   # then edit with your PAT
#   PAT=glpat-xxxxxxxxxxxxxxxx
#   GITLAB_URL=https://gitlab.com/api/v4

# 3 · Build (auto‑generates TLS certs)
docker build -t gitlab-tool-https .

# 4 · Run (HTTPS → 8443)
docker run -p 8443:8443 --env-file .env gitlab-tool-https
```

Open **https://localhost:8443/docs** → interactive Swagger.  
*(Browser will warn about the self‑signed cert – that’s expected.)*

---

## 🔍 API Cheat‑Sheet

### 🔧 `POST /grant_permission`

Assign a role to a GitLab user.

| Field | Type | Example |
|-------|------|---------|
| `username` | `string` | `"aaronofjm"` |
| `repo_or_group` | `string` | `"mobileye_group_VPs"` |
| `role` | `"guest" \| reporter \| developer \| maintainer \| owner"` | `"developer"` |

### 📆 `GET /get_items_by_year`

`GET /get_items_by_year?item_type=issues&year=2025`

Returns count + array of items created that year.

---


Made with 🛠 by **Aaron Mark** – Pro DevOps Engineer :)
