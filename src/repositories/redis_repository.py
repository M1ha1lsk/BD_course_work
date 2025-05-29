import redis
from settings import REDIS_CONFIG
from datetime import timedelta

class RedisRepository:
    def __init__(self):
        self.redis = redis.Redis(**REDIS_CONFIG)
        self.token_ttl = timedelta(hours=1).seconds
        self.cache_ttl = timedelta(minutes=5).seconds

    # Методы для работы с токенами
    def store_token(self, school_name, token):
        self.redis.setex(f"token:{token}", self.token_ttl, school_name)
        self.redis.sadd(f"user:{school_name}:tokens", token)

    def validate_token(self, token):
        return self.redis.get(f"token:{token}")

    def invalidate_token(self, token):
        school_name = self.redis.get(f"token:{token}")
        if school_name:
            self.redis.srem(f"user:{school_name}:tokens", token)
        self.redis.delete(f"token:{token}")

    # Методы для кэширования
    def cache_boats_data(self, key, data):
        self.redis.setex(key, self.cache_ttl, data)

    def get_cached_boats_data(self, key):
        return self.redis.get(key)

    # Методы для уведомлений
    def publish_notification(self, channel, message):
        self.redis.publish(channel, message)

    def subscribe_to_channel(self, channel):
        pubsub = self.redis.pubsub()
        pubsub.subscribe(channel)
        return pubsub