# Stage 1: Build the Java application
FROM openjdk:11 AS java-builder

# Set the working directory in the container
WORKDIR /app

# Copy the Java application source code into the container
COPY phenomiser-cli-0.1.1.jar /app
COPY hp.obo /app
COPY phenotype.hpoa /app

# Stage 2: Build the Flask API
FROM python:3.8.10

# Set the working directory in the container
WORKDIR /app

# Copy the Flask application source code into the container
COPY . /app

# Copy the Java application from the previous stage into the container
COPY --from=java-builder /app/phenomiser-cli-0.1.1.jar /app/phenomiser-cli-0.1.1.jar

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Expose the port
EXPOSE 5000

# Command to run the Flask application
CMD ["python", "phenomizer.py"]

