# JWT Authentication & CORS Fix — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add JWT authentication to all Orbiter API endpoints and fix the dangerous CORS configuration.

**Architecture:** Create `backend/core/auth.py` for token logic, `backend/api/deps.py` for FastAPI dependency injection, add login/register endpoints to `main.py`, and add auth dependency to every protected router.

**Tech Stack:** PyJWT, passlib[bcrypt], FastAPI HTTPBearer security scheme, existing SQLAlchemy/SQLite database.

---

## File Map

| Action | File | Purpose |
|--------|------|---------|
| Create | `backend/core/auth.py` | JWT creation/validation, password hashing |
| Create | `backend/api/deps.py` | FastAPI `get_current_user` dependency |
| Modify | `backend/main.py` | Fix CORS, add login/register endpoints, add auth to upload endpoint |
| Modify | `backend/api/jobs.py` | Add auth to all routes |
| Modify | `backend/api/applications.py` | Add auth to all routes |
| Modify | `backend/api/dashboard.py` | Add auth to all routes |
| Modify | `backend/api/profile.py` | Add auth to all routes |
| Modify | `backend/api/settings.py` | Add auth to all routes |
| Modify | `backend/api/crm.py` | Add auth to all routes |
| Modify | `backend/api/mode.py` | Add auth to all routes |
| Modify | `backend/api/promptops.py` | Add auth to all routes |
| Modify | `backend/api/evaluation.py` | Add auth to all routes |
| Modify | `backend/api/chaos.py` | Add auth to all routes |
| Modify | `backend/requirements.txt` | Add pyjwt, passlib[bcrypt] |
| Create | `.gitignore` | Prevent secrets from being committed |
| Create | `tests/test_auth/test_auth.py` | Test token creation, validation, expiry, login/register |

---

### Task 1: Add Dependencies to requirements.txt

**Files:**
- Modify: `backend/requirements.txt`

- [ ] **Step 1: Add pyjwt and passlib[bcrypt]**

Add these two lines after the existing dependencies in `backend/requirements.txt`:

```
pyjwt>=2.8.0
passlib[bcrypt]>=1.7.4
```

- [ ] **Step 2: Install dependencies**

Run: `pip install pyjwt "passlib[bcrypt]"`

Expected: Successfully installed pyjwt and passlib.

- [ ] **Step 3: Commit**

```bash
git add backend/requirements.txt
git commit -m "chore: add pyjwt and passlib[bcrypt] for JWT auth"
```

---

### Task 2: Create `.gitignore` at project root

**Files:**
- Create: `.gitignore`

- [ ] **Step 1: Create `.gitignore`**

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.egg-info/
dist/
build/
.eggs/
*.egg

# Virtual environments
venv/
.venv/
env/

# Environment variables
.env

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Database
*.db
*.db-journal

# Logs
*.log

# Redis
dump.rdb
celerybeat-schedule*

# OAuth tokens
token.json

# Test / coverage
.pytest_cache/
htmlcov/
.coverage
```

- [ ] **Step 2: Commit**

```bash
git add .gitignore
git commit -m "chore: add .gitignore to prevent secrets and build artifacts"
```

---

### Task 3: Create `backend/core/auth.py`

**Files:**
- Create: `backend/core/auth.py`

- [ ] **Step 1: Write the failing test for token creation**

Create `tests/test_auth/__init__.py` (empty file).

Create `tests/test_auth/test_auth.py`:

```python
import pytest
from datetime import timedelta
from backend.core.auth import create_access_token, verify_token


def test_create_access_token_returns_string():
    token = create_access_token({"sub": "user123"})
    assert isinstance(token, str)
    assert len(token) > 0


def test_verify_token_valid():
    token = create_access_token({"sub": "user123"})
    payload = verify_token(token)
    assert payload["sub"] == "user123"
    assert "exp" in payload


def test_verify_token_expired():
    token = create_access_token({"sub": "user123"}, expires_delta=timedelta(seconds=-1))
    with pytest.raises(Exception) as exc_info:
        verify_token(token)
    assert exc_info.value.status_code == 401
    assert "expired" in exc_info.value.detail.lower()


def test_verify_token_invalid():
    with pytest.raises(Exception) as exc_info:
        verify_token("not.a.valid.token")
    assert exc_info.value.status_code == 401


def test_hash_and_verify_password():
    from backend.core.auth import hash_password, verify_password
    hashed = hash_password("testpass123")
    assert verify_password("testpass123", hashed) is True
    assert verify_password("wrongpass", hashed) is False
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_auth/test_auth.py -v`

Expected: FAIL — `ModuleNotFoundError: No module named 'backend.core.auth'`

- [ ] **Step 3: Write the implementation**

```python
from datetime import datetime, timedelta
from typing import Optional
import jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status

SECRET_KEY = "orbiter-secret-key-change-in-production"  # Read from env in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_auth/test_auth.py -v`

Expected: 5 passed.

- [ ] **Step 5: Commit**

```bash
git add backend/core/auth.py tests/test_auth/__init__.py tests/test_auth/test_auth.py
git commit -m "feat: add JWT auth core module with token creation, validation, and password hashing"
```

---

### Task 4: Create `backend/api/deps.py`

**Files:**
- Create: `backend/api/deps.py`

- [ ] **Step 1: Write the implementation**

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from backend.core.auth import verify_token

security = HTTPBearer()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_token(token)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    return {"user_id": user_id}


async def get_current_user_optional(authorization: str = None):
    if not authorization:
        return None
    try:
        token = authorization.replace("Bearer ", "")
        payload = verify_token(token)
        return {"user_id": payload.get("sub")}
    except Exception:
        return None
```

- [ ] **Step 2: Commit**

```bash
git add backend/api/deps.py
git commit -m "feat: add FastAPI auth dependency for JWT Bearer tokens"
```

---

### Task 5: Fix CORS and Add Login/Register in `backend/main.py`

**Files:**
- Modify: `backend/main.py`

- [ ] **Step 1: Fix CORS middleware**

Replace the existing CORS block (lines 87–93):

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

With:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

- [ ] **Step 2: Add imports for auth**

Add these imports at the top of `main.py`, after the existing imports:

```python
from pydantic import BaseModel
from typing import Optional
from backend.core.auth import create_access_token, hash_password, verify_password
```

- [ ] **Step 3: Add auth request/response models and login/register endpoints**

Add the following AFTER the `health_check` endpoint and BEFORE the `upload_resume` endpoint (after line 108):

```python
class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    email: str
    password: str
    name: Optional[str] = None


# In-memory user store for Phase 1 (will be replaced with DB in Phase 2)
_users_db: dict = {}


@app.post("/api/auth/register")
def register(payload: RegisterRequest):
    if payload.email in _users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    _users_db[payload.email] = {
        "email": payload.email,
        "hashed_password": hash_password(payload.password),
        "name": payload.name or payload.email.split("@")[0],
    }
    token = create_access_token({"sub": payload.email})
    return {"access_token": token, "token_type": "bearer", "user": {"email": payload.email, "name": _users_db[payload.email]["name"]}}


@app.post("/api/auth/login")
def login(payload: LoginRequest):
    user = _users_db.get(payload.email)
    if not user or not verify_password(payload.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_access_token({"sub": payload.email})
    return {"access_token": token, "token_type": "bearer", "user": {"email": payload.email, "name": user["name"]}}
```

- [ ] **Step 4: Add auth dependency to upload_resume endpoint**

Modify the `upload_resume` function signature to include auth:

```python
from backend.api.deps import get_current_user

@app.post("/api/upload-resume")
async def upload_resume(background_tasks: BackgroundTasks, file: UploadFile = File(...), current_user: dict = Depends(get_current_user)):
```

And change the hardcoded `user_id="default_user"` to `user_id=current_user["user_id"]`.

- [ ] **Step 5: Verify the app starts**

Run: `cd K:\JOB\orbiter && python -c "from backend.main import app; print('App imports OK')"`

Expected: `App imports OK`

- [ ] **Step 6: Commit**

```bash
git add backend/main.py
git commit -m "feat: fix CORS origins, add login/register endpoints, protect upload endpoint"
```

---

### Task 6: Add Auth to All API Routers

For each router file, follow the same pattern:
1. Add import: `from backend.api.deps import get_current_user`
2. Add parameter: `current_user: dict = Depends(get_current_user)` to every route function

#### 6a. `backend/api/jobs.py`

- [ ] **Step 1: Add import**

Add after line 9 (`from backend.core.database import get_db`):

```python
from backend.api.deps import get_current_user
```

- [ ] **Step 2: Add auth to `list_jobs`**

Change signature (line 20–27) to:

```python
def list_jobs(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    company: Optional[str] = None,
    location: Optional[str] = None,
    source_type: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
```

- [ ] **Step 3: Add auth to `get_job`**

Change signature (line 63) to:

```python
def get_job(job_id: str, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
```

- [ ] **Step 4: Add auth to `trigger_job_discovery`**

Change signature (line 88) to:

```python
def trigger_job_discovery(current_user: dict = Depends(get_current_user)):
```

- [ ] **Step 5: Add auth to `apply_to_job`**

Change signature (line 97) to:

```python
def apply_to_job(job_id: str, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
```

- [ ] **Step 6: Commit**

```bash
git add backend/api/jobs.py
git commit -m "feat: add JWT auth to jobs router"
```

#### 6b. `backend/api/applications.py`

- [ ] **Step 1: Add import**

Add after line 7 (`from backend.core.database import get_db`):

```python
from backend.api.deps import get_current_user
```

- [ ] **Step 2: Add auth to `list_applications`**

Change signature to:

```python
def list_applications(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
```

- [ ] **Step 3: Add auth to `get_application`**

Change signature to:

```python
def get_application(app_id: str, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
```

- [ ] **Step 4: Add auth to `approve_application`**

Change signature to:

```python
def approve_application(app_id: str, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
```

- [ ] **Step 5: Add auth to `reject_application`**

Change signature to:

```python
def reject_application(app_id: str, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
```

- [ ] **Step 6: Add auth to `export_document`**

Change signature to:

```python
def export_document(
    app_id: str,
    type: str = Query("resume", enum=["resume", "cover_letter"]),
    format: str = Query("pdf", enum=["pdf", "docx", "txt", "md"]),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
```

- [ ] **Step 7: Commit**

```bash
git add backend/api/applications.py
git commit -m "feat: add JWT auth to applications router"
```

#### 6c. `backend/api/dashboard.py`

- [ ] **Step 1: Add import**

Add after line 5 (`from backend.core.database import get_db`):

```python
from backend.api.deps import get_current_user
```

- [ ] **Step 2: Add auth to `get_dashboard_metrics`**

Change signature to:

```python
def get_dashboard_metrics(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
```

- [ ] **Step 3: Add auth to `get_activity`**

Change signature to:

```python
def get_activity(skip: int = 0, limit: int = 20, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
```

- [ ] **Step 4: Commit**

```bash
git add backend/api/dashboard.py
git commit -m "feat: add JWT auth to dashboard router"
```

#### 6d. `backend/api/profile.py`

- [ ] **Step 1: Add import**

Add after line 8 (`from backend.core.action_logger import action_logger`):

```python
from backend.api.deps import get_current_user
```

- [ ] **Step 2: Add auth to `get_profile`**

Change signature to:

```python
def get_profile(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
```

- [ ] **Step 3: Add auth to `create_or_update_profile`**

Change signature to:

```python
def create_or_update_profile(payload: ProfileCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
```

- [ ] **Step 4: Add auth to `upload_resume`**

Change signature to:

```python
async def upload_resume(background_tasks: BackgroundTasks, file: UploadFile = File(...), db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
```

- [ ] **Step 5: Commit**

```bash
git add backend/api/profile.py
git commit -m "feat: add JWT auth to profile router"
```

#### 6e. `backend/api/settings.py`

- [ ] **Step 1: Add import**

Add after line 5 (`from backend.core.action_logger import action_logger`):

```python
from backend.api.deps import get_current_user
```

- [ ] **Step 2: Add auth to `get_settings`**

Change signature to:

```python
def get_settings(current_user: dict = Depends(get_current_user)):
```

Also add the `Depends` import at the top:

```python
from fastapi import APIRouter, Depends
```

- [ ] **Step 3: Add auth to `update_settings`**

Change signature to:

```python
def update_settings(payload: SettingsUpdate, current_user: dict = Depends(get_current_user)):
```

- [ ] **Step 4: Add auth to `check_email_now`**

Change signature to:

```python
def check_email_now(current_user: dict = Depends(get_current_user)):
```

- [ ] **Step 5: Add auth to `email_status`**

Change signature to:

```python
def email_status(current_user: dict = Depends(get_current_user)):
```

- [ ] **Step 6: Commit**

```bash
git add backend/api/settings.py
git commit -m "feat: add JWT auth to settings router"
```

#### 6f. `backend/api/crm.py`

- [ ] **Step 1: Add import**

Add after line 9 (`from backend.crm.service import crm_service`):

```python
from backend.api.deps import get_current_user
```

- [ ] **Step 2: Add auth to all 5 CRM routes**

Add `current_user: dict = Depends(get_current_user)` to: `list_contacts`, `add_contact`, `get_contact`, `get_conversations`, `log_conversation_message`.

- [ ] **Step 3: Commit**

```bash
git add backend/api/crm.py
git commit -m "feat: add JWT auth to CRM router"
```

#### 6g. `backend/api/mode.py`

- [ ] **Step 1: Add import**

Add after line 3 (`from backend.core.config import settings`):

```python
from fastapi import Depends
from backend.api.deps import get_current_user
```

Replace existing import line 1:

```python
from fastapi import APIRouter, HTTPException, Depends
```

- [ ] **Step 2: Add auth to `get_mode` and `update_mode`**

Add `current_user: dict = Depends(get_current_user)` to both.

- [ ] **Step 3: Commit**

```bash
git add backend/api/mode.py
git commit -m "feat: add JWT auth to mode router"
```

#### 6h. `backend/api/promptops.py`

- [ ] **Step 1: Add import**

Add after line 7 (`from backend.promptops.manager import prompt_manager`):

```python
from backend.api.deps import get_current_user
```

- [ ] **Step 2: Add auth to all 4 promptops routes**

Add `current_user: dict = Depends(get_current_user)` to: `list_prompts`, `create_prompt_version`, `activate_version`, `rollback_prompt`.

- [ ] **Step 3: Commit**

```bash
git add backend/api/promptops.py
git commit -m "feat: add JWT auth to promptops router"
```

#### 6i. `backend/api/evaluation.py`

- [ ] **Step 1: Add import**

Add after line 7 (`from backend.evaluation.reporter import evaluation_reporter`):

```python
from backend.api.deps import get_current_user
```

- [ ] **Step 2: Add auth to `list_metrics` and `get_weekly_report`**

Add `current_user: dict = Depends(get_current_user)` to both.

- [ ] **Step 3: Commit**

```bash
git add backend/api/evaluation.py
git commit -m "feat: add JWT auth to evaluation router"
```

#### 6j. `backend/api/chaos.py`

- [ ] **Step 1: Add import**

Add after line 5 (`from backend.chaos.scenarios import CHAOS_SCENARIOS`):

```python
from fastapi import Depends
from backend.api.deps import get_current_user
```

Replace existing import line 1:

```python
from fastapi import APIRouter, HTTPException, Depends
```

- [ ] **Step 2: Add auth to all 4 chaos routes**

Add `current_user: dict = Depends(get_current_user)` to: `list_scenarios`, `enable_scenario`, `disable_scenario`, `run_resilience_suite`.

- [ ] **Step 3: Commit**

```bash
git add backend/api/chaos.py
git commit -m "feat: add JWT auth to chaos router"
```

---

### Task 7: Update Existing Tests to Include Auth Headers

**Files:**
- Modify: `tests/test_api/test_api.py`

- [ ] **Step 1: Add a fixture that creates a token and registers/logs in**

```python
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def _get_auth_header():
    """Register a test user and return Authorization header."""
    client.post("/api/auth/register", json={"email": "test@test.com", "password": "testpass123"})
    resp = client.post("/api/auth/login", json={"email": "test@test.com", "password": "testpass123"})
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


AUTH_HEADER = _get_auth_header()


def test_api_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "online"}


def test_api_register():
    resp = client.post("/api/auth/register", json={"email": "new@test.com", "password": "pass123"})
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert data["user"]["email"] == "new@test.com"


def test_api_login():
    client.post("/api/auth/register", json={"email": "login@test.com", "password": "pass123"})
    resp = client.post("/api/auth/login", json={"email": "login@test.com", "password": "pass123"})
    assert resp.status_code == 200
    assert "access_token" in resp.json()


def test_api_login_wrong_password():
    client.post("/api/auth/register", json={"email": "wrong@test.com", "password": "pass123"})
    resp = client.post("/api/auth/login", json={"email": "wrong@test.com", "password": "wrong"})
    assert resp.status_code == 401


def test_api_dashboard_metrics_unauthorized():
    response = client.get("/api/dashboard/metrics")
    assert response.status_code == 403  # No auth header


def test_api_dashboard_metrics_authorized():
    response = client.get("/api/dashboard/metrics", headers=AUTH_HEADER)
    assert response.status_code == 200
    data = response.json()
    assert "new_matches" in data
    assert "auto_applied" in data
    assert "agent_status" in data
    assert data["agent_status"]["master"] == "online"


def test_api_upload_resume_unauthorized():
    import io
    files = {"file": ("resume.txt", io.BytesIO(b"test content"), "text/plain")}
    response = client.post("/api/upload-resume", files=files)
    assert response.status_code == 403
```

- [ ] **Step 2: Run the full test suite**

Run: `cd K:\JOB\orbiter && pytest tests/test_api/test_api.py -v`

Expected: All tests pass (8 tests).

- [ ] **Step 3: Commit**

```bash
git add tests/test_api/test_api.py
git commit -m "test: add auth headers to API tests, test login/register flow"
```

---

### Task 8: Verify Full Test Suite

- [ ] **Step 1: Run all tests**

Run: `cd K:\JOB\orbiter && pytest tests/ -v --tb=short`

Expected: All tests pass (auth tests + existing tests). Some existing tests may need auth headers — fix them.

- [ ] **Step 2: Fix any broken tests**

If existing tests like `test_chaos`, `test_crm`, `test_promptops`, `test_evaluation` fail with 403, they need the auth header fixture added.

Pattern for each:

```python
def _get_auth_header():
    from fastapi.testclient import TestClient
    from backend.main import app
    c = TestClient(app)
    c.post("/api/auth/register", json={"email": "test@test.com", "password": "testpass123"})
    resp = c.post("/api/auth/login", json={"email": "test@test.com", "password": "testpass123"})
    return {"Authorization": f"Bearer {resp.json()['access_token']}"}

AUTH = _get_auth_header()
```

Then pass `headers=AUTH` to each client call.

- [ ] **Step 3: Final commit**

```bash
git add -A
git commit -m "fix: update remaining test files with auth headers"
```

---

## Self-Review Checklist

1. **Spec coverage:** JWT auth on all endpoints? Yes. Login/register? Yes. CORS fixed? Yes. .gitignore? Yes. Tests? Yes.
2. **Placeholder scan:** No TBD/TODO. All code blocks complete.
3. **Type consistency:** `get_current_user` returns `{"user_id": str}` everywhere. `current_user: dict` parameter name consistent.
4. **Excluded routes:** `/api/health`, `/api/auth/login`, `/api/auth/register` — none have auth dependency. Correct.
5. **Default user fallback:** The `user_id` from JWT replaces `"default_user"` in `upload_resume`. Other routes don't use user_id yet (kept for Phase 2).
