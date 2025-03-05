## **Chapter 3: Redis**

In this chapter, we delve into **Redis**, a lightning-fast, in-memory data store that pairs well with containerized environments. You’ll learn about key Redis concepts (data structures, persistence, commands) and how to integrate Redis with other services (e.g., Flask) via **Docker Compose**. By the end, you should be able to spin up a Redis container, connect to it from a Python app, and use it for tasks such as caching or counting page hits.

---

### **1. Theories**

1. **What is Redis?**  
   - **In-Memory Data Store**: Data lives in RAM, giving near-instant read/writes.  
   - **Use Cases**: Caching, session storage, real-time analytics, pub/sub messaging.  
   - **Data Structures**: Strings, Lists, Hashes, Sets, Sorted Sets. Each structure has specialized commands for maximum efficiency.

2. **Redis Architecture**  
   - **Single-Threaded** but extremely performant.  
   - **Persistence**: Optional (RDB snapshots, Append-Only File). Many users treat Redis as ephemeral, but you can configure it to save data to disk.  
   - **Connections**: Typically on port 6379.

3. **Dockerizing Redis**  
   - **Official Image**: `redis:alpine` is a common lightweight choice.  
   - **docker-compose.yml**: Usually, you define a service named `redis` with `image: redis:alpine`.  
   - **Named Volume**: If you require data persistence across container restarts, map a volume to `/data`.

4. **Basic Redis Commands**  
   - **CLI**: `redis-cli` for testing (e.g., `SET key value`, `GET key`, `INCR counter`).  
   - **Libraries**: Python’s `redis` library for app-level interactions, e.g.,  
     ```python
     import redis
     r = redis.Redis(host='redis', port=6379)
     r.incr('hits')
     ```

5. **Redis in a Multi-Service Application**  
   - **Flask Example**: Use Redis to store session data or track page views.  
   - **Django Example**: Often used for caching or Celery task queue backends.  
   - **Networking**: Docker Compose automatically provides a hostname (`redis` if your service is named `redis`) for your other containers to connect via `host='redis'`.

---

### **2. Step-by-Step Workshop**

#### **Step 1: Minimal Redis Setup in Docker Compose**

1. **docker-compose.yml Example**  
   ```yaml
   version: '3.8'
   services:
     redis:
       image: redis:alpine
       container_name: my_redis
       ports:
         - "6379:6379"
       volumes:
         - redis_data:/data

   volumes:
     redis_data:
   ```
   - This defines a `redis` service with the **`redis:alpine`** image, mapping port 6379 locally, and storing data in a named volume for persistence.

2. **Startup**  
   - Run:
     ```bash
     docker compose up -d
     ```
   - Check logs:
     ```bash
     docker compose logs -f redis
     ```
   - You should see output indicating Redis is ready to accept connections.

#### **Step 2: Interact with Redis (CLI)**

1. **Exec into the Container**  
   ```bash
   docker compose exec redis sh
   ```
2. **Install redis-tools (optional)**  
   - If `redis-cli` is not present, you can install or use another container that has `redis-cli`. On many Alpine-based images, you might run:
     ```bash
     apk add --no-cache redis
     ```
3. **Test Commands**  
   ```bash
   redis-cli
   > PING
   PONG
   > SET greeting "Hello from Redis"
   OK
   > GET greeting
   "Hello from Redis"
   ```

#### **Step 3: Connect from a Python App**

1. **requirements.txt** (for your Python code)
   ```plaintext
   redis==4.5.1
   ```
2. **app.py** (Flask or any Python script)
   ```python
   import redis

   r = redis.Redis(host='redis', port=6379, decode_responses=True)
   r.set('framework', 'Flask')
   print("Redis saved framework as:", r.get('framework'))
   ```
3. **Docker Compose Integration**  
   - If you have another service named `web`, it can link to `redis` via `host='redis'`. 
   - For example:
     ```yaml
     services:
       web:
         build: .
         depends_on:
           - redis
       redis:
         image: redis:alpine
         ...
     ```
   - This ensures `web` starts after `redis`, and the container hostname `redis` is resolvable within the `web` container.

#### **Step 4: Using Redis for a Simple Counter (Optional)**

- **Flask** integration example in `app.py`:
  ```python
  from flask import Flask
  import redis

  app = Flask(__name__)
  r = redis.Redis(host='redis', port=6379, decode_responses=True)

  @app.route('/')
  def index():
      hits = r.incr('page_hits')
      return f"This page has been visited {hits} times."
  ```
- Rebuild and run via Docker Compose, then check `http://localhost:5000`.

---

### **3. Assignment**

1. **Objective**  
   - Learn how to start a Redis service, connect to it from a local or containerized Python script, and store ephemeral data.

2. **Tasks**  
   1. **Docker Compose**  
      - Create a `redis` service using the `redis:alpine` image, exposing port `6379`.  
      - Persist data via a named volume.
   2. **Redis CLI**  
      - Exec into the Redis container, run `redis-cli`, and set a key (`"student_name"`) with your name.  
      - Retrieve it to confirm the data is stored.
   3. **Optional**: **Flask Integration**  
      - Modify a Flask route to use Redis for a hit counter.  
      - Submit a screenshot showing the incremented counts.

3. **Deliverables**  
   - Docker Compose file snippet.  
   - Screenshot of Redis CLI or logs showing your key.  
   - (Optional) Screenshot of the Flask route counting visits.

---

### **4. Conclusion**

**Redis** is a powerful in-memory store that fits seamlessly into containerized environments for high-performance caching, counters, and ephemeral data. Through Docker Compose, you can link a `redis` service to your web containers, referencing **`host='redis'`** for direct connections. Mastering these fundamentals sets the stage for building more complex applications—like caching layers in Django or session management in Flask—that benefit from Redis’s lightning-fast operations.