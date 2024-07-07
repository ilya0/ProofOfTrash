
# Use Python 3.9 slim image from Docker Hub
FROM --platform=linux/amd64 python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the backend application
COPY . .

# Install Python dependencies from requirements.txt
WORKDIR /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV PORT 8000
ENV CURRENT_HOST 0.0.0.0

EXPOSE $PORT
RUN chmod +x /usr/src/app/start.sh
CMD ["/usr/src/app/start.sh"]