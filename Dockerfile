FROM python:3.10.6

# Set the working directory inside the container
WORKDIR /app

# Copy the application files to the container
COPY . /app

# Install Java
RUN apt-get update && apt-get install -y default-jre

# Install dependencies
RUN pip install -r requirements.txt

# Expose port 80 as a TCP port
EXPOSE 80/tcp

# Set the startup command
CMD sh -c "java -jar lavalink/Lavalink.jar & python bot.py"
