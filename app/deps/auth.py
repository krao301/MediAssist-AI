from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import requests
from functools import lru_cache
import os

security = HTTPBearer()

@lru_cache()
def get_jwks():
    """Fetch and cache Auth0 JWKS"""
    jwks_url = os.getenv("AUTH0_JWKS", "https://your-tenant.auth0.com/.well-known/jwks.json")
    response = requests.get(jwks_url)
    return response.json()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify Auth0 JWT token"""
    token = credentials.credentials
    
    try:
        # For demo/development, you can skip verification
        # In production, uncomment the full verification below
        
        # Quick decode without verification for hackathon speed
        unverified = jwt.get_unverified_claims(token)
        return unverified
        
        # Production version:
        # jwks = get_jwks()
        # unverified_header = jwt.get_unverified_header(token)
        # rsa_key = {}
        # for key in jwks["keys"]:
        #     if key["kid"] == unverified_header["kid"]:
        #         rsa_key = {
        #             "kty": key["kty"],
        #             "kid": key["kid"],
        #             "use": key["use"],
        #             "n": key["n"],
        #             "e": key["e"]
        #         }
        # if rsa_key:
        #     payload = jwt.decode(
        #         token,
        #         rsa_key,
        #         algorithms=["RS256"],
        #         audience=os.getenv("AUTH0_AUDIENCE"),
        #         issuer=f"https://{os.getenv('AUTH0_DOMAIN')}/"
        #     )
        #     return payload
        
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}"
        )
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unable to verify token"
    )

def require_auth(token_data: dict = Depends(verify_token)):
    """Dependency that requires authentication"""
    return token_data

# Optional: For hackathon demo without Auth0 setup
def demo_auth():
    """Simple demo auth that returns a mock user"""
    return {"sub": "demo-user-123", "name": "Demo User"}
