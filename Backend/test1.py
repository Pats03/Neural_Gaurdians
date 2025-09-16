import redis

# connect to local redis
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

# test set/get
r.set("hello", "world", ex=60)  # expire after 60s
print("Stored:", r.get("hello"))