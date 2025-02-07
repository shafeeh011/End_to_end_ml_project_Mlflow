# Use a Python version compatible with the required packages (>=3.9)
FROM python:3.9-slim
WORKDIR /app
COPY . /app
# Upgrade pip to the latest version
RUN pip install --upgrade pip
# Install dependencies with --no-cache-dir to avoid potential caching issues
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python3", "app.py"]