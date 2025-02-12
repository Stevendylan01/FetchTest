# Health Check Script

This project allows you to send HTTP requests and track domain status based on the responses. You can run the script either directly on your local machine or through Docker.

## Two Ways to Run the Project

### 1. **Run Locally (Python)**

- Install the required dependencies:

  ```bash
  pip install -r requirements.txt
  
- Run the script with a file argument (e.g., entry.yaml):
  ```bash
  python health-check.py /path/to/file.yaml

### 2. **Run with Docker**

- Build the docker container

  ```bash
  docker build . -t health-check:v1
  
- Run the docker container:
  ```bash 
    docker run -it -v $(pwd)/file.yaml:/app/file.yaml health-check:v1

- Run the script inside the container:
  ```bash 
    python health-check.py /app/file.yaml
