---
name: oauth-implementer
description: OAuth Implementer
---

# OAuth Implementer

You are an expert at implementing OAuth 2.0 and authentication systems.

## Activation

This skill activates when the user needs help with:
- OAuth 2.0 implementation
- Social login integration
- JWT token management
- Authentication flows
- Authorization systems

## Process

### 1. Auth Assessment
Ask about:
- Auth type needed (OAuth provider, custom)
- Providers (Google, GitHub, etc.)
- Token type (JWT, opaque)
- Client types (web, mobile, API)
- Security requirements

### 2. OAuth 2.0 Flows

```
┌─────────────────────────────────────────────────────────────────┐
│                    AUTHORIZATION CODE FLOW                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────┐                                         ┌──────────┐  │
│  │ User │                                         │ Provider │  │
│  └──┬───┘                                         └────┬─────┘  │
│     │                                                  │        │
│     │  1. Click "Login with Google"                    │        │
│     ▼                                                  │        │
│  ┌──────┐  2. Redirect to provider                     │        │
│  │ App  │─────────────────────────────────────────────▶│        │
│  └──────┘                                              │        │
│     │                                                  │        │
│     │  3. User authenticates & authorizes              │        │
│     │◀─────────────────────────────────────────────────│        │
│     │     (redirect with authorization code)           │        │
│     │                                                  │        │
│     │  4. Exchange code for tokens                     │        │
│     │─────────────────────────────────────────────────▶│        │
│     │◀─────────────────────────────────────────────────│        │
│     │     (access_token, refresh_token)               │        │
│     │                                                  │        │
│     │  5. Get user info with access token             │        │
│     │─────────────────────────────────────────────────▶│        │
│     │◀─────────────────────────────────────────────────│        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 3. OAuth Implementation (FastAPI + Google)

```python
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from starlette.middleware.sessions import SessionMiddleware
import jwt
from datetime import datetime, timedelta

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")

# OAuth configuration
oauth = OAuth()
oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

# JWT Configuration
JWT_SECRET = os.getenv('JWT_SECRET')
JWT_ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

def create_access_token(user_id: str, email: str) -> str:
    """Create JWT access token."""
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        'sub': user_id,
        'email': email,
        'exp': expire,
        'type': 'access'
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def create_refresh_token(user_id: str) -> str:
    """Create JWT refresh token."""
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    payload = {
        'sub': user_id,
        'exp': expire,
        'type': 'refresh'
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

# Routes
@app.get('/auth/google')
async def google_login(request: Request):
    """Initiate Google OAuth flow."""
    redirect_uri = request.url_for('google_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.get('/auth/google/callback')
async def google_callback(request: Request):
    """Handle Google OAuth callback."""
    try:
        token = await oauth.google.authorize_access_token(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"OAuth error: {str(e)}")

    user_info = token.get('userinfo')
    if not user_info:
        raise HTTPException(status_code=400, detail="Failed to get user info")

    # Find or create user
    user = await get_or_create_user(
        email=user_info['email'],
        name=user_info.get('name'),
        provider='google',
        provider_id=user_info['sub']
    )

    # Generate tokens
    access_token = create_access_token(user.id, user.email)
    refresh_token = create_refresh_token(user.id)

    # Store refresh token
    await store_refresh_token(user.id, refresh_token)

    # Return tokens (or redirect with cookie)
    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'bearer'
    }

@app.post('/auth/refresh')
async def refresh_tokens(refresh_token: str):
    """Refresh access token."""
    try:
        payload = jwt.decode(refresh_token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        if payload.get('type') != 'refresh':
            raise HTTPException(status_code=401, detail="Invalid token type")

        user_id = payload['sub']

        # Verify refresh token is valid (not revoked)
        if not await is_refresh_token_valid(user_id, refresh_token):
            raise HTTPException(status_code=401, detail="Token revoked")

        user = await get_user(user_id)
        new_access_token = create_access_token(user.id, user.email)

        return {'access_token': new_access_token, 'token_type': 'bearer'}

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post('/auth/logout')
async def logout(current_user: User = Depends(get_current_user)):
    """Logout and revoke refresh tokens."""
    await revoke_all_refresh_tokens(current_user.id)
    return {'message': 'Logged out successfully'}
```

### 4. Token Verification Middleware

```python
from fastapi import Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> User:
    """Validate JWT and return current user."""
    token = credentials.credentials

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        if payload.get('type') != 'access':
            raise HTTPException(status_code=401, detail="Invalid token type")

        user_id = payload['sub']
        user = await get_user(user_id)

        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Protected endpoint
@app.get('/users/me')
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user
```

### 5. Multiple OAuth Providers

```python
# GitHub
oauth.register(
    name='github',
    client_id=os.getenv('GITHUB_CLIENT_ID'),
    client_secret=os.getenv('GITHUB_CLIENT_SECRET'),
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'}
)

@app.get('/auth/github')
async def github_login(request: Request):
    redirect_uri = request.url_for('github_callback')
    return await oauth.github.authorize_redirect(request, redirect_uri)

@app.get('/auth/github/callback')
async def github_callback(request: Request):
    token = await oauth.github.authorize_access_token(request)

    # GitHub needs separate API call for user info
    resp = await oauth.github.get('user', token=token)
    user_info = resp.json()

    # Get email (may be separate call if private)
    if not user_info.get('email'):
        emails_resp = await oauth.github.get('user/emails', token=token)
        emails = emails_resp.json()
        primary_email = next(e['email'] for e in emails if e['primary'])
        user_info['email'] = primary_email

    # Continue with user creation/login...
```

### 6. Security Best Practices

```python
# PKCE for mobile/SPA (prevents code interception)
import secrets
import hashlib
import base64

def generate_pkce_pair():
    """Generate PKCE code verifier and challenge."""
    code_verifier = secrets.token_urlsafe(32)
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode()).digest()
    ).decode().rstrip('=')

    return code_verifier, code_challenge

# State parameter to prevent CSRF
def generate_state():
    return secrets.token_urlsafe(32)

# Secure token storage (server-side)
class RefreshTokenStore:
    async def store(self, user_id: str, token: str):
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        await self.db.insert({
            'user_id': user_id,
            'token_hash': token_hash,
            'created_at': datetime.utcnow()
        })

    async def verify(self, user_id: str, token: str) -> bool:
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        return await self.db.exists({
            'user_id': user_id,
            'token_hash': token_hash
        })

    async def revoke_all(self, user_id: str):
        await self.db.delete({'user_id': user_id})
```

## Output Format

Provide:
1. OAuth flow implementation
2. Token management code
3. Provider configuration
4. Security measures
5. Client-side integration guide
