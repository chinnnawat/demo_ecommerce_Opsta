# Use the official Python image as a parent image
FROM python:3

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY backend/ /app


# Install dependencies specified in requirements.txt
RUN pip install -r ./mysite/requirements.txt

# Expose port 8000
EXPOSE 8000

# Command to run the Django server
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
