"""
Token Blacklist for JWT Logout
Supports Redis for production and in-memory fallback for development
"""
import os
import logging
from datetime import datetime, timedelta
from typing import Optional

logger = logging.getLogger(__name__)


class TokenBlacklist:
    """
    Token blacklist manager with Redis and in-memory support.
    Tokens are stored with TTL matching their expiration time.
    """

    def __init__(self):
        self._redis_client = None
        self._memory_store = {}  # Fallback: {jti: expiry_timestamp}
        self._use_redis = False
        self._initialized = False

    def init_app(self, app):
        """Initialize with Flask app configuration"""
        redis_url = app.config.get('REDIS_URL') or os.environ.get('REDIS_URL')

        if redis_url:
            try:
                import redis
                self._redis_client = redis.from_url(
                    redis_url,
                    decode_responses=True,
                    socket_connect_timeout=5,
                    socket_timeout=5
                )
                # Test connection
                self._redis_client.ping()
                self._use_redis = True
                logger.info("Token blacklist initialized with Redis")
            except Exception as e:
                logger.warning(f"Redis connection failed, using in-memory blacklist: {e}")
                self._use_redis = False
        else:
            logger.info("No REDIS_URL configured, using in-memory token blacklist")
            self._use_redis = False

        self._initialized = True

    def add(self, jti: str, expires_delta: Optional[timedelta] = None) -> bool:
        """
        Add a token JTI to the blacklist.

        Args:
            jti: The JWT ID (unique identifier)
            expires_delta: How long to keep in blacklist (default: 1 hour)

        Returns:
            True if successfully added
        """
        if expires_delta is None:
            expires_delta = timedelta(hours=1)

        ttl_seconds = int(expires_delta.total_seconds())

        if self._use_redis and self._redis_client:
            try:
                # Store with TTL so Redis auto-cleans expired entries
                self._redis_client.setex(
                    f"token_blacklist:{jti}",
                    ttl_seconds,
                    "revoked"
                )
                logger.debug(f"Token {jti[:8]}... added to Redis blacklist")
                return True
            except Exception as e:
                logger.error(f"Redis blacklist add failed: {e}")
                # Fall through to memory store

        # In-memory fallback
        expiry = datetime.utcnow() + expires_delta
        self._memory_store[jti] = expiry.timestamp()
        self._cleanup_memory_store()
        logger.debug(f"Token {jti[:8]}... added to memory blacklist")
        return True

    def is_blacklisted(self, jti: str) -> bool:
        """
        Check if a token JTI is blacklisted.

        Args:
            jti: The JWT ID to check

        Returns:
            True if token is blacklisted (revoked)
        """
        if self._use_redis and self._redis_client:
            try:
                result = self._redis_client.exists(f"token_blacklist:{jti}")
                return bool(result)
            except Exception as e:
                logger.error(f"Redis blacklist check failed: {e}")
                # Fall through to memory check

        # In-memory check
        if jti in self._memory_store:
            expiry = self._memory_store[jti]
            if datetime.utcnow().timestamp() < expiry:
                return True
            else:
                # Expired entry, clean it up
                del self._memory_store[jti]

        return False

    def _cleanup_memory_store(self):
        """Remove expired entries from memory store"""
        now = datetime.utcnow().timestamp()
        expired = [jti for jti, expiry in self._memory_store.items() if expiry < now]
        for jti in expired:
            del self._memory_store[jti]

    def get_stats(self) -> dict:
        """Get blacklist statistics for monitoring"""
        if self._use_redis and self._redis_client:
            try:
                keys = self._redis_client.keys("token_blacklist:*")
                return {
                    "storage": "redis",
                    "count": len(keys),
                    "connected": True
                }
            except Exception:
                pass

        self._cleanup_memory_store()
        return {
            "storage": "memory",
            "count": len(self._memory_store),
            "connected": False
        }


# Singleton instance
token_blacklist = TokenBlacklist()
