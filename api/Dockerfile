FROM --platform=linux/amd64 python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the app code
COPY app ./app
# Copy specific config files if needed
COPY .env.example .
# Do NOT copy the whole folder structure blindly

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
