FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies (example: if you need build tools)
RUN apt-get update && apt-get install -y \
    build-essential libpq-dev --no-install-recommends \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entrypoint script into the container
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose port 8000 for Django’s dev server
EXPOSE 8000

# Use the custom entrypoint (it will run the dev server at the end)
ENTRYPOINT ["/entrypoint.sh"]
