If you want to execute commands inside a running container (often called "exec into" the container), you can use the `docker exec` command. Here are the steps:

1. **Run Your Container (if it's not running yet):**  
   If your container isn’t running, you can start it using:

   ```bash
   docker run -d --name my_container my_image
   ```

   Replace `my_container` with your desired container name and `my_image` with your image name. The `-d` flag runs the container in detached mode.

2. **Execute a Command Inside the Container:**  
   To start an interactive shell session in the container, use:

   ```bash
   docker exec -it my_container /bin/bash
   ```

   **Note:**  
   - The `-it` options combine to allocate a pseudo-TTY and keep STDIN open.  
   - Some slim images might not have bash installed. If you get an error saying bash is not found, you can try `/bin/sh` instead:

     ```bash
     docker exec -it my_container /bin/sh
     ```

3. **Example Workflow:**

   - **Building the image:**

     Assuming your Dockerfile is in the current directory:

     ```bash
     docker build -t my_image .
     ```

   - **Starting the container:**

     ```bash
     docker run -d --name my_container my_image
     ```

   - **Accessing the container's shell:**

     ```bash
     docker exec -it my_container /bin/bash
     ```

   Once you're inside the container, you can run any commands you need.

4. **Stopping and Removing Containers:**  
   When you're done, you might want to stop and remove your container:

   ```bash
   docker stop my_container
   docker rm my_container
   ```

Using these steps, you can execute and interact with your running container. If you need further assistance with specific commands or have any additional questions, feel free to ask!