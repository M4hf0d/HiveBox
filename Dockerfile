# Use an official Python runtime with pinned version as the base image
FROM python:3.9.18-slim-bullseye


# Create a non-root user
RUN groupadd -r hivebox && useradd -r -g hivebox hivebox

# Set the working directory in the container
WORKDIR /app

# Expose the port the app runs on
EXPOSE 5000

# Copy requirements first to leverage Docker Layers cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code into the container
COPY app.py .

# Change ownership of the app directory
RUN chown -R hivebox:hivebox /app

# Switch to non-root user
USER hivebox

# Use ENTRYPOINT with CMD
ENTRYPOINT ["python"]
CMD ["-m", "flask", "run", "--host=0.0.0.0"]
