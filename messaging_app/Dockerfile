# Use a base Python image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy all files into the container
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port your Django app runs on
EXPOSE 8000

# Run the application
# Note: The "-p" flag is used when running the container to map ports (e.g., docker run -p 8000:8000)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
