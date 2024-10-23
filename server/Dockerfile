# Use an official Python runtime as the base image
FROM python:3.12.0-slim-bookworm

# Set environment variables for better Python output and bytecode generation
ENV PYTHONBUFFERED=1
ENV PYTHONWRITEBYTECODE=1

# Define the application directory variable
ENV APP=/app

# Set the working directory inside the container
WORKDIR $APP

# Copy the requirements.txt file into the container
COPY requirements.txt $APP

# Install the dependencies listed in requirements.txt
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

# Copy the rest of the application code into the container
COPY . $APP

# Expose the port on which the app will run
EXPOSE 8000

# Make the entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Set the entrypoint for the container
ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]

# Command to start the application using Gunicorn
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "djangoproj.wsgi"]
