import hashlib

import redis
from decouple import config


__all__ = ('RedisManager',)


def _hash(val):
    return hashlib.md5(val.encode()).hexdigest()


class _RedisManager:

    def __init__(self):
        self._r = None

    def connect(self):
        try:
            self._r = redis.StrictRedis(
                host=config('REDIS_HOST'),
                port=config('REDIS_PORT'),
                password=config('REDIS_PASSWORD'),
            )
        except redis.exceptions.ConnectionError:
            pass

    def is_connected(self):
        return self._r is not None

    def get(self, key):
        if self._r is None:
            return

        url_hash = _hash(key)[:12]
        if not self._r.exists(url_hash):
            return

        item = self._r.get(url_hash).decode()
        return item

    def save(self, key, val):
        if self._r is None:
            return

        url_hash = _hash(key)[:12]
        self._r.set(url_hash, val)


RedisManager = _RedisManager()
if not RedisManager.is_connected():
    RedisManager.connect()
