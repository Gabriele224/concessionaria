# Dockerfile for FastAPI Backend
 
# Use the official Python image from the Docker Hub
FROM python:3.10-slim
 
# Set the working directory in the container
WORKDIR /app
 
# Copy the requirements file into the container
COPY requirements.txt .
 
# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install typing_inspect
 
# Copy the FastAPI app code into the container
COPY . .
 
# Expose the port FastAPI runs on
EXPOSE 8000
 
# Command to run the FastAPI app
CMD ["uvicorn", "main:app","--reload", "--host", "0.0.0.0", "--port", "8000"]