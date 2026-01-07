from redis import Redis
import json


class RedisClient:
    def __init__(self, host='localhost', port=6379, db=0, decode_responses=True):
        self.client = Redis(host=host, port=port, db=db, decode_responses=decode_responses)

    def get(self, key: str) -> str | None:
        return self.client.get(key)

    def set(self, key: str, value: str) -> None:
        self.client.set(key, value)

    def get_dict(self, key: str) -> dict | None:
        value = self.get(key)
        return value if value is None else json.loads(value)
    
    def set_dict(self, key: str, value: dict) -> None:
        values = json.dumps(value)
        self.set(key, values)

    def exists(self, key: str) -> bool:
        return self.client.exists(key) == 1
    
    def expire(self, key: str, seconds: int) -> None:
        self.client.expire(key, seconds)

    def close(self):
        self.client.close()
