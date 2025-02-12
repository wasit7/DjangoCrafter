from flask import Flask
import redis

app = Flask(__name__)

# Connect to Redis using the service name defined in docker-compose.yml
r = redis.Redis(host='redis', port=6379, decode_responses=True)

@app.route('/')
def index():
    # Increment the "hits" key in Redis
    r.incr('hits')
    hits = r.get('hits')
    return f"Hello, World! This page has been viewed {hits} times."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
