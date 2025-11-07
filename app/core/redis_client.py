"""
Redis client configuration for caching and session management
"""

from typing import Optional, Any, Union
import json
import logging
from redis import Redis, ConnectionPool
from redis.exceptions import RedisError, ConnectionError as RedisConnectionError

from .config import settings


# Configure logging
logger = logging.getLogger(__name__)


# ============================================
# Redis Connection Pool
# ============================================

redis_pool = ConnectionPool(
    host=settings.redis.host,
    port=settings.redis.port,
    db=settings.redis.db,
    password=settings.redis.password if settings.redis.password else None,
    max_connections=settings.redis.max_connections,
    socket_timeout=settings.redis.socket_timeout,
    socket_connect_timeout=settings.redis.socket_timeout,
    decode_responses=True,  # Automatically decode responses to strings
)


# ============================================
# Redis Client
# ============================================

class RedisClient:
    """
    Redis client wrapper with utility methods
    """
    
    def __init__(self):
        """Initialize Redis client"""
        if settings.redis.enabled:
            try:
                self.client = Redis(connection_pool=redis_pool)
                self._test_connection()
            except Exception as e:
                logger.error(f"Failed to connect to Redis: {str(e)}")
                self.client = None
        else:
            logger.info("Redis is disabled in settings")
            self.client = None
    
    def _test_connection(self) -> bool:
        """Test Redis connection"""
        try:
            self.client.ping()
            logger.info("✅ Redis connection successful")
            return True
        except RedisConnectionError as e:
            logger.error(f"❌ Redis connection failed: {str(e)}")
            return False
    
    def is_available(self) -> bool:
        """Check if Redis is available"""
        if not self.client:
            return False
        try:
            return self.client.ping()
        except:
            return False
    
    # ============================================
    # Basic Operations
    # ============================================
    
    def get(self, key: str) -> Optional[str]:
        """
        Get value by key
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None
        """
        if not self.client:
            return None
        
        try:
            return self.client.get(key)
        except RedisError as e:
            logger.error(f"Redis GET error: {str(e)}")
            return None
    
    def set(
        self,
        key: str,
        value: Union[str, int, float],
        expire: Optional[int] = None
    ) -> bool:
        """
        Set key-value pair
        
        Args:
            key: Cache key
            value: Value to cache
            expire: Expiration time in seconds
            
        Returns:
            True if successful, False otherwise
        """
        if not self.client:
            return False
        
        try:
            if expire is None:
                expire = settings.redis.cache_expire
            
            return self.client.setex(key, expire, value)
        except RedisError as e:
            logger.error(f"Redis SET error: {str(e)}")
            return False
    
    def delete(self, *keys: str) -> int:
        """
        Delete one or more keys
        
        Args:
            keys: Keys to delete
            
        Returns:
            Number of keys deleted
        """
        if not self.client:
            return 0
        
        try:
            return self.client.delete(*keys)
        except RedisError as e:
            logger.error(f"Redis DELETE error: {str(e)}")
            return 0
    
    def exists(self, key: str) -> bool:
        """
        Check if key exists
        
        Args:
            key: Cache key
            
        Returns:
            True if exists, False otherwise
        """
        if not self.client:
            return False
        
        try:
            return bool(self.client.exists(key))
        except RedisError as e:
            logger.error(f"Redis EXISTS error: {str(e)}")
            return False
    
    def expire(self, key: str, seconds: int) -> bool:
        """
        Set expiration time for key
        
        Args:
            key: Cache key
            seconds: Expiration time in seconds
            
        Returns:
            True if successful, False otherwise
        """
        if not self.client:
            return False
        
        try:
            return self.client.expire(key, seconds)
        except RedisError as e:
            logger.error(f"Redis EXPIRE error: {str(e)}")
            return False
    
    def ttl(self, key: str) -> int:
        """
        Get remaining time to live for key
        
        Args:
            key: Cache key
            
        Returns:
            Seconds remaining, -1 if no expiry, -2 if key doesn't exist
        """
        if not self.client:
            return -2
        
        try:
            return self.client.ttl(key)
        except RedisError as e:
            logger.error(f"Redis TTL error: {str(e)}")
            return -2
    
    # ============================================
    # JSON Operations
    # ============================================
    
    def get_json(self, key: str) -> Optional[Any]:
        """
        Get JSON value
        
        Args:
            key: Cache key
            
        Returns:
            Deserialized JSON value or None
        """
        value = self.get(key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error: {str(e)}")
                return None
        return None
    
    def set_json(
        self,
        key: str,
        value: Any,
        expire: Optional[int] = None
    ) -> bool:
        """
        Set JSON value
        
        Args:
            key: Cache key
            value: Value to serialize and cache
            expire: Expiration time in seconds
            
        Returns:
            True if successful, False otherwise
        """
        try:
            json_value = json.dumps(value)
            return self.set(key, json_value, expire)
        except (TypeError, json.JSONEncodeError) as e:
            logger.error(f"JSON encode error: {str(e)}")
            return False
    
    # ============================================
    # Hash Operations
    # ============================================
    
    def hget(self, name: str, key: str) -> Optional[str]:
        """Get hash field value"""
        if not self.client:
            return None
        
        try:
            return self.client.hget(name, key)
        except RedisError as e:
            logger.error(f"Redis HGET error: {str(e)}")
            return None
    
    def hset(self, name: str, key: str, value: str) -> bool:
        """Set hash field value"""
        if not self.client:
            return False
        
        try:
            return bool(self.client.hset(name, key, value))
        except RedisError as e:
            logger.error(f"Redis HSET error: {str(e)}")
            return False
    
    def hgetall(self, name: str) -> dict:
        """Get all hash fields"""
        if not self.client:
            return {}
        
        try:
            return self.client.hgetall(name)
        except RedisError as e:
            logger.error(f"Redis HGETALL error: {str(e)}")
            return {}
    
    def hdel(self, name: str, *keys: str) -> int:
        """Delete hash fields"""
        if not self.client:
            return 0
        
        try:
            return self.client.hdel(name, *keys)
        except RedisError as e:
            logger.error(f"Redis HDEL error: {str(e)}")
            return 0
    
    # ============================================
    # List Operations
    # ============================================
    
    def lpush(self, name: str, *values: str) -> int:
        """Push values to list (left)"""
        if not self.client:
            return 0
        
        try:
            return self.client.lpush(name, *values)
        except RedisError as e:
            logger.error(f"Redis LPUSH error: {str(e)}")
            return 0
    
    def rpush(self, name: str, *values: str) -> int:
        """Push values to list (right)"""
        if not self.client:
            return 0
        
        try:
            return self.client.rpush(name, *values)
        except RedisError as e:
            logger.error(f"Redis RPUSH error: {str(e)}")
            return 0
    
    def lrange(self, name: str, start: int = 0, end: int = -1) -> list:
        """Get list range"""
        if not self.client:
            return []
        
        try:
            return self.client.lrange(name, start, end)
        except RedisError as e:
            logger.error(f"Redis LRANGE error: {str(e)}")
            return []
    
    # ============================================
    # Set Operations
    # ============================================
    
    def sadd(self, name: str, *values: str) -> int:
        """Add members to set"""
        if not self.client:
            return 0
        
        try:
            return self.client.sadd(name, *values)
        except RedisError as e:
            logger.error(f"Redis SADD error: {str(e)}")
            return 0
    
    def smembers(self, name: str) -> set:
        """Get all set members"""
        if not self.client:
            return set()
        
        try:
            return self.client.smembers(name)
        except RedisError as e:
            logger.error(f"Redis SMEMBERS error: {str(e)}")
            return set()
    
    def sismember(self, name: str, value: str) -> bool:
        """Check if value is in set"""
        if not self.client:
            return False
        
        try:
            return bool(self.client.sismember(name, value))
        except RedisError as e:
            logger.error(f"Redis SISMEMBER error: {str(e)}")
            return False
    
    # ============================================
    # Utility Methods
    # ============================================
    
    def incr(self, key: str, amount: int = 1) -> Optional[int]:
        """Increment key by amount"""
        if not self.client:
            return None
        
        try:
            return self.client.incr(key, amount)
        except RedisError as e:
            logger.error(f"Redis INCR error: {str(e)}")
            return None
    
    def decr(self, key: str, amount: int = 1) -> Optional[int]:
        """Decrement key by amount"""
        if not self.client:
            return None
        
        try:
            return self.client.decr(key, amount)
        except RedisError as e:
            logger.error(f"Redis DECR error: {str(e)}")
            return None
    
    def flush_db(self) -> bool:
        """Flush current database (USE WITH CAUTION!)"""
        if not self.client:
            return False
        
        try:
            return self.client.flushdb()
        except RedisError as e:
            logger.error(f"Redis FLUSHDB error: {str(e)}")
            return False
    
    def keys(self, pattern: str = "*") -> list:
        """Get keys matching pattern"""
        if not self.client:
            return []
        
        try:
            return self.client.keys(pattern)
        except RedisError as e:
            logger.error(f"Redis KEYS error: {str(e)}")
            return []
    
    def info(self) -> dict:
        """Get Redis server info"""
        if not self.client:
            return {}
        
        try:
            return self.client.info()
        except RedisError as e:
            logger.error(f"Redis INFO error: {str(e)}")
            return {}


# ============================================
# Create Redis Client Instance
# ============================================

redis_client = RedisClient()


# ============================================
# Cache Decorator
# ============================================

def cache(expire: int = 3600, key_prefix: str = ""):
    """
    Cache decorator for functions
    
    Args:
        expire: Cache expiration time in seconds
        key_prefix: Prefix for cache key
    
    Usage:
        @cache(expire=300, key_prefix="user")
        def get_user(user_id: int):
            return db.query(User).filter(User.id == user_id).first()
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = f"{key_prefix}:{func.__name__}:{str(args)}:{str(kwargs)}"
            
            # Try to get from cache
            cached = redis_client.get_json(cache_key)
            if cached is not None:
                logger.debug(f"Cache hit: {cache_key}")
                return cached
            
            # Execute function
            result = func(*args, **kwargs)
            
            # Store in cache
            redis_client.set_json(cache_key, result, expire)
            logger.debug(f"Cache set: {cache_key}")
            
            return result
        
        return wrapper
    return decorator


# ============================================
# Exports
# ============================================

__all__ = [
    "redis_client",
    "RedisClient",
    "cache",
]