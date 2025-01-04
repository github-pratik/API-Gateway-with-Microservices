FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy source code
COPY src/ .

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "main.py"] 