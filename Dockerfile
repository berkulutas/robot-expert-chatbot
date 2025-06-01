# Dockerfile
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the full app code
COPY . .

# Expose the internal Flask port
EXPOSE 5000

# Default Flask command
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
