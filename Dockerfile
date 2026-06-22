# Use a stable Python environment
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first to cache dependencies
COPY backend/requirements.txt .

# Install the heavy ML packages and backend dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend files into the container
COPY backend/ .

# Expose port 7860 (Mandatory for Hugging Face Spaces)
EXPOSE 7860

# Start the FastAPI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]