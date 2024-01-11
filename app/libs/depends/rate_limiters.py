"""
Rate limiters dependencies for API endpoints.
"""
from fastapi import Depends
from fastapi_limiter.depends import RateLimiter

DEFAULT_RATE_LIMITERS = [
    Depends(RateLimiter(times=6, seconds=1)),
    Depends(RateLimiter(times=7, seconds=2)),
    Depends(RateLimiter(times=45, seconds=30)),
    Depends(RateLimiter(times=1200, seconds=3600)),
]
