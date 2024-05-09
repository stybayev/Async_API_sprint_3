import os
import time
import redis

redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = os.getenv('REDIS_PORT', '6379')

if __name__ == '__main__':
    r = redis.Redis(host=redis_host, port=redis_port)
    while True:
        try:
            r.get("none")
            break
        except redis.exceptions.ConnectionError:
            time.sleep(1)
