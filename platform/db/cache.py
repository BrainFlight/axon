import logging
from typing import List

import valkey

from config import GlobalConfig

logger = logging.getLogger(__name__)

config = GlobalConfig()


class CacheClient:
    def __init__(
        self, 
        host: str = config.cache_host, 
        port: int = config.cache_port, 
        db: int = 0
    ):
        self.client = valkey.Valkey(host=host, port=port, db=db)

    def set(self, key: str, value: str) -> bool:
        """
        Set value in cache.

        Args:
            key: Key to set value for.
            value: Value to set.
        """
        if self.client.set(key, value):
            return True
        return False

    def get(self, key) -> str:
        """
        Get value from cache.

        Args:
            key: Key to get value for.

        Returns:
            str: Value for key.
        """
        return self.client.get(key)
    
    def delete(self, key) -> bool:
        """
        Delete key from cache.

        Args:
            key: Key to delete.
        """
        if self.client.delete(key):
            return True
        return False
    
    def exists(self, key) -> bool:
        """
        Check if key exists in cache.

        Args:
            key: Key to check.
        """
        if self.client.exists(key):
            return True
        return False
    
    def keys(self, pattern: str) -> List[str]:
        """
        Get all keys matching pattern.

        Args:
            pattern: Pattern to match keys.

        Returns:
            List[str]: List of keys matching pattern.
        """
        return self.client.keys(pattern)
    
    def hash_set(self, key: str, field: str, value: str) -> bool:
        """
        Set value in hash.

        Args:
            key: Key of hash.
            field: Field to set value for.
            value: Value to set.
        """
        if self.client.hset(key, field, value):
            return True
        return False

    def hash_get(self, key: str, field: str) -> str:
        """
        Get value from hash.

        Args:
            key: Key of hash.
            field: Field to get value for.

        Returns:
            str: Value for field.
        """
        return self.client.hget(key, field)
    
    def hash_delete(self, key: str, field: str):
        """
        Delete field from hash.

        Args:
            key: Key of hash.
            field: Field to delete.
        """
        if self.client.hdel(key, field):
            return True
        return False
