FROM python:3.10.6

# Set the working directory inside the container
WORKDIR /app

# Copy the application files to the container
COPY . /app

# Install Nginx
#RUN apt-get update && apt-get install -y nginx

# Copy the Nginx configuration file
#COPY nginx.conf /etc/nginx/sites-available/default

# Install dependencies
RUN pip install -r requirements.txt

# Expose port 80 as a TCP port
EXPOSE 80/tcp

# Set the startup command
CMD python bot.py
