FROM python:3.13.2

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy all code
COPY . .

# Create required dirs
RUN mkdir -p uploads chroma_db

# Make startup script executable
RUN chmod +x start.sh

EXPOSE 7860

CMD ["bash","./start.sh"]