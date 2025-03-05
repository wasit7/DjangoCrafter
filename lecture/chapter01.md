## **Chapter 1: Docker**

This chapter provides a comprehensive overview of **Docker**, the containerization platform that underpins our multi-service development environment for modern web applications. By the end of this chapter, students will be able to explain how containers differ from traditional virtual machines, build Docker images, and orchestrate multiple containers with Docker Compose.

---

### **1. Theories**

1. **Containerization vs. Virtual Machines**  
   - **Core Idea**: Containers package an application and its dependencies within a single unit, sharing the host OS kernel rather than virtualizing an entire operating system.  
   - **Benefits**:  
     - **Lightweight**: Less overhead than a VM, as containers don’t each run a separate OS.  
     - **Isolation**: Each container runs in its own environment, reducing conflicts.  
     - **Portability**: Containers can run on any system with Docker installed, making deployments consistent.  
   - **Examples**: Docker, Podman, LXC.

2. **Docker Images and Containers**  
   - **Images**: Immutable blueprints describing how to set up the container (OS libraries, Python packages, etc.).  
   - **Containers**: Running instances of images. You can spin up multiple containers from the same image.  
   - **Layered File System**: Docker images are built in layers, speeding up rebuilds if previous layers haven’t changed.

3. **Dockerfile Basics**  
   - **Purpose**: Defines instructions (layers) to create a custom Docker image.  
   - **Common Instructions**:  
     - `FROM python:3.9-slim` – Base image.  
     - `WORKDIR /app` – Sets the working directory.  
     - `COPY requirements.txt .` – Copies files for installation.  
     - `RUN pip install --no-cache-dir -r requirements.txt` – Installs dependencies.  
     - `COPY . .` – Copies all code into the container.  
     - `CMD ["python", "app.py"]` – Default command upon container startup.

4. **Docker Compose**  
   - **Definition**: A tool for defining and running multi-container Docker applications (e.g., a web container, database container, caching container).  
   - **Features**:  
     - **Services**: Each container is described as a service.  
     - **Networks**: Allows containers to communicate by service name.  
     - **Volumes**: Data persistence across container restarts.  
   - **docker-compose.yml**: The configuration file that declares how each service is built, what ports are exposed, and any environment variables.

5. **Typical Workflow**  
   - **Build**: `docker compose build` reads the Dockerfile(s) and constructs images.  
   - **Run**: `docker compose up -d` launches the containers in the background.  
   - **Logs**: `docker compose logs -f <service>` streams logs for debugging.  
   - **Stop/Remove**: `docker compose down` stops and removes containers and networks (while named volumes persist unless specified).

6. **Why Docker?**  
   - **Reproducible Environments**: Eliminates “it works on my machine” scenarios.  
   - **Isolation**: Each service (web, db, cache) can run in its own container, preventing library conflicts.  
   - **Scalability**: Containers can be scaled horizontally (e.g., multiple web containers).  
   - **Easy Collaboration**: All you need is the project folder and a `docker-compose.yml` to replicate the environment.

---

### **2. Step-by-Step Workshop**

Follow these steps to get a hands-on understanding of Docker and Docker Compose:

#### **Step 1: Install Docker**

1. **Docker Engine**  
   - **Windows/macOS**: Install Docker Desktop from [https://www.docker.com/get-started](https://www.docker.com/get-started).  
   - **Linux**: Install Docker Engine using your distro’s package manager.  
2. **Verification**  
   - Run:
     ```bash
     docker --version
     docker compose version
     ```
   - Confirm Docker and Docker Compose are installed successfully.

#### **Step 2: Create a Simple Dockerfile**

1. **Project Folder**  
   - Make a folder named `my-docker-test`.
2. **Dockerfile**  
   - Inside `my-docker-test`, create a file called `Dockerfile`:
     ```dockerfile
     FROM python:3.9-slim
     WORKDIR /app
     COPY requirements.txt .
     RUN pip install --no-cache-dir -r requirements.txt
     COPY . .
     CMD ["python", "app.py"]
     ```
3. **requirements.txt**  
   - If your Python code depends on certain libraries, list them here. For example:
     ```plaintext
     Flask==2.2.3
     ```
4. **app.py**  
   - A minimal Python script:
     ```python
     print("Hello from Docker!")
     ```

#### **Step 3: Build and Run the Container**

1. **Build the Image**  
   ```bash
   cd my-docker-test
   docker build -t my-docker-test .
   ```
   - `-t my-docker-test` names the image “my-docker-test”.
2. **Run the Container**  
   ```bash
   docker run --rm my-docker-test
   ```
   - You should see “Hello from Docker!” in your terminal.
   - `--rm` removes the container after it exits.

#### **Step 4: Introduce Docker Compose**

1. **docker-compose.yml**  
   - Create `docker-compose.yml` in the `my-docker-test` folder:
     ```yaml
     version: '3.8'
     services:
       web:
         build: .
         container_name: hello_docker
         command: python app.py
     ```
2. **Start Services**  
   ```bash
   docker compose up --build
   ```
   - You’ll see the same “Hello from Docker!” output, but now orchestrated by Compose.

3. **Logs and Cleanup**  
   - **Logs**: `docker compose logs -f`
   - **Stop**: `docker compose down`

#### **Step 5: Expanding to Multiple Services (Optional)**

- If time allows, modify `docker-compose.yml` to include another service (e.g., Redis or PostgreSQL).  
- **Example**:
  ```yaml
  version: '3.8'
  services:
    web:
      build: .
      container_name: simple_web
      command: python app.py
    redis:
      image: redis:alpine
      container_name: simple_redis
  ```
- Now you can run `docker compose up` to start both.

---

### **3. Assignment**

1. **Objective**  
   - Demonstrate understanding of Docker’s basics: building images, running containers, and using Docker Compose.

2. **Tasks**  
   1. **Create a Minimal Project**  
      - Make a `Dockerfile` and a simple Python script (`app.py`) that prints “Your Name’s Docker Test”.  
      - Add a `docker-compose.yml` with one service called `web`.
   2. **Build & Run**  
      - Use `docker compose build` and `docker compose up` to verify the container is working.  
      - Capture output logs.
   3. **Submit Evidence**  
      - Screenshot or copy-paste your Docker output “Your Name’s Docker Test”.  
      - Briefly explain each line in your `Dockerfile`.

3. **Due Date**  
   - End of **Week 1**. Submit to the LMS with a short reflection on how Docker simplifies environment setup.

---

### **4. Conclusion**

**Docker** is a cornerstone technology for modern development, providing **lightweight** and **reproducible** environments. By learning Docker fundamentals, you can effortlessly **build**, **distribute**, and **run** applications across varied systems. As projects grow in complexity—requiring databases, caches, or AI tools—**Docker Compose** orchestrates multiple containers in a single file for consistent multi-service architecture. Mastering Docker in this first chapter sets you up for efficient and scalable workflows throughout the rest of this course and beyond.