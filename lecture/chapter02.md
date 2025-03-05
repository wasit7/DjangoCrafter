## **Chapter 2: Flask**

This chapter explores **Flask**, a popular Python micro-framework known for its simplicity and flexibility. Students will learn about Flask’s routing system, how to serve dynamic web pages, and best practices for running Flask inside a Docker container. By the end of this chapter, students should be able to create and deploy a basic Flask application, understanding how environment variables and container ports work to make the app accessible locally.

---

### **1. Theories**

1. **Flask’s Micro-Framework Philosophy**  
   - **Minimal Core**: Flask provides essentials like routing and request handling, leaving other functionalities (e.g., database integration, authentication) to extensions.  
   - **Flexibility**: Developers can choose their own libraries for templating, database access, etc., making Flask highly customizable.  
   - **Simplicity**: A basic Flask app can start with just a few lines of Python code.

2. **Routing and Views**  
   - **Decorator-Based Routing**: `@app.route('/')` associates a URL path with a Python function that handles the request.  
   - **HTTP Methods**: By default, Flask routes handle GET requests. You can specify `methods=['GET', 'POST']` for handling forms or data submissions.  
   - **Return Values**: A view function returns a string (simple) or rendered templates (with data).

3. **Development Server**  
   - **Flask’s Built-in Server**: For local development, run `flask run` or `app.run()`.  
   - **Default Port**: Flask usually runs on port 5000. In Docker, you’ll map `5000:5000` so the app is reachable at `http://localhost:5000`.  
   - **Production**: In real deployments, you might use a production server like **gunicorn** or **uwsgi** behind **Nginx**.

4. **Using Flask with Docker**  
   - **Dockerfile**: Typically a Python image (`FROM python:3.9-slim`), installing `Flask` in `requirements.txt`.  
   - **Expose and Run**: `EXPOSE 5000` in the Dockerfile; run your app with `CMD ["python", "app.py"]` or `CMD ["flask", "run", "--host=0.0.0.0"]`.  
   - **docker-compose.yml**: If your service is called `web`, you can define: 
     ```yaml
     services:
       web:
         build: .
         ports:
           - "5000:5000"
     ```
   - **Environment Variables**: In Compose, you might set a variable like `FLASK_ENV=development` or `DEBUG=1` for auto-reloads.

5. **Key Flask Extensions** (Optional Reference)  
   - **Jinja2**: Flask’s templating engine, integrated by default.  
   - **Flask SQLAlchemy**: For database connections (not built-in).  
   - **Flask Migrate**: Handling migrations (similar to Django but more manual).  
   - **Flask-Login**: User authentication.  

---

### **2. Step-by-Step Workshop**

Follow these steps to create and run a simple Flask application inside a Docker container:

#### **Step 1: Minimal Flask App**

1. **Project Structure**  
   - Create a folder named `flask-docker-test`.  
   - Inside, have `app.py` and `requirements.txt`.

2. **app.py**  
   ```python
   from flask import Flask

   app = Flask(__name__)

   @app.route('/')
   def index():
       return "Hello from Flask in Docker!"

   if __name__ == '__main__':
       app.run(host='0.0.0.0', port=5000)
   ```

3. **requirements.txt**  
   ```plaintext
   Flask==2.2.3
   ```

#### **Step 2: Dockerfile**

1. **Dockerfile** in the same folder:
   ```dockerfile
   FROM python:3.9-slim

   WORKDIR /app
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   COPY . .
   EXPOSE 5000
   CMD ["python", "app.py"]
   ```

2. **Build**  
   ```bash
   docker build -t flask_docker_test .
   ```
   - This builds an image named `flask_docker_test`.

3. **Run**  
   ```bash
   docker run --rm -p 5000:5000 flask_docker_test
   ```
   - Access `http://localhost:5000` to see **“Hello from Flask in Docker!”**.

#### **Step 3: Docker Compose Setup**

1. **docker-compose.yml**  
   ```yaml
   version: '3.8'
   services:
     web:
       build: .
       container_name: flask_web
       ports:
         - "5000:5000"
   ```
2. **Compose Commands**  
   - `docker compose build`: Builds the image.  
   - `docker compose up`: Runs the container.  
   - Open your browser to `http://localhost:5000`.

3. **Logs & Cleanup**  
   - `docker compose logs -f` to watch the Flask logs.  
   - `docker compose down` stops and removes containers, networks (and volumes, if any).

#### **Step 4: Adding a Route with URL Parameters (Optional)**

- Modify `app.py`:
  ```python
  @app.route('/user/<name>')
  def user_page(name):
      return f"Hello, {name}!"
  ```
- Rebuild or let Flask’s debug mode auto-reload. Go to `http://localhost:5000/user/Alice`.  

---

### **3. Assignment**

1. **Objective**  
   - Demonstrate you can run a minimal Flask application in Docker and extend it with a new route.

2. **Tasks**  
   1. **Create a “hello user” route**  
      - Modify `app.py` to include `@app.route('/hello/<username>')`.  
      - Return a greeting with the user’s name.  
   2. **Docker Compose**  
      - Ensure your `docker-compose.yml` maps port 5000 to your host.  
      - Confirm you can open `http://localhost:5000/hello/Bob` in your browser.  
   3. **Submit Evidence**  
      - A screenshot of your “Hello, Bob!” page.  
      - A short explanation of how you mapped the container port to the host port in `ports:`.

3. **Due Date**  
   - End of **Week 2**. Submit the Dockerfile, `docker-compose.yml`, and screenshots to the LMS.

---

### **4. Conclusion**

**Flask** is a lightweight framework that gives you control over each component of your application stack. Pairing Flask with **Docker** enables you to keep your environment consistent across development and production, solving dependency conflicts and deployment headaches. By mastering basic routes, environment variables, and port mappings, you’re on your way to creating scalable microservices or integrating further with other containers (e.g., Redis, PostgreSQL) in future lessons.