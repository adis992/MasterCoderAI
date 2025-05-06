FROM python:3.9-slim
WORKDIR /app

# Copy and install root-level requirements
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy backend code into container
COPY backend/ /app/

# Default command for API (can be overridden)
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]