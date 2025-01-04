# Use Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first for caching
COPY api/requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application
COPY api/ .

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "index.py"] 