FROM --platform=linux/amd64 python:3.8-slim

WORKDIR /usr/src/

COPY . .

RUN dir -s

RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME dev

CMD ["python", "app/app.py"]