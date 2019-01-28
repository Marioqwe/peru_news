import hashlib

import redis

from scrappy import settings


__all__ = ('RedisManager',)


REDIS = getattr(settings, 'REDIS', None)
if REDIS is None:
    raise ValueError('\'REDIS\' settings not set.')


def _hash(val):
    return hashlib.md5(val.encode()).hexdigest()


class _RedisManager:

    def __init__(self):
        self._r = None

    def connect(self):
        try:
            self._r = redis.StrictRedis(
                host=REDIS.HOST,
                port=REDIS.PORT,
                password=REDIS.PASSWORD,
            )
        except redis.exceptions.ConnectionError:
            pass

    def is_connected(self):
        return self._r is not None

    def get(self, key, hashed=False):
        if self._r is None:
            return

        if not hashed:
            url_hash = _hash(key)
        else:
            url_hash = key

        if not self._r.exists(url_hash):
            return

        item = self._r.get(url_hash).decode()
        return item

    def save(self, key, val):
        if self._r is None:
            return

        url_hash = _hash(key)
        self._r.set(url_hash, val)


RedisManager = _RedisManager()
if not RedisManager.is_connected():
    RedisManager.connect()
