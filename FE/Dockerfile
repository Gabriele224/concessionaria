# Dockerfile for Streamlit Frontend
 
# Use the official Python image from the Docker Hub
FROM python:3.10-slim
 
# Set the working directory in the container
WORKDIR /app
 
# Copy the requirements file into the container
COPY requirements.txt .
 
# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt
 
# Copy the Streamlit app code into the container
COPY . .
 
# Expose the port Streamlit runs on
EXPOSE 8501
 
# Command to run the Streamlit app
CMD ["streamlit", "run", "streamlit_main.py", "--server.port=8501", "--server.address=0.0.0.0"]