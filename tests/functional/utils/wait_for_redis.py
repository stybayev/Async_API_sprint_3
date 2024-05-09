import os
import time
import redis

redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = os.getenv('REDIS_PORT', '6379')

if __name__ == '__main__':
    r = redis.Redis(host=redis_host, port=redis_port)
    while True:
        try:
            # Trying to get a non-existing key, just to ping the server
            r.get("none")
            break
        except redis.exceptions.ConnectionError:
            print("Waiting for Redis to be ready...")
            time.sleep(1)
    print("Redis is ready!")
