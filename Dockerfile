# Use official Python base image
FROM python:3.10

# Set working directory inside the container
WORKDIR /app

# Copy everything into the container
COPY . .

# Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Create output directory inside container if not exists
RUN mkdir -p output

# Run your main code file
CMD ["python", "process_pdfs.py"]
