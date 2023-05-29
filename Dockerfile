# Pull base image
FROM python:3.9

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Copy the project files to the working directory
COPY . /app

# Install system-level dependencies for GDAL
RUN apt-get update && \
    apt-get install -y gdal-bin libgdal-dev

# Install dependencies
RUN pip install --upgrade pip

RUN pip install pillow

RUN pip install -r requirements.txt

# Copy project
EXPOSE 8000

CMD ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]






