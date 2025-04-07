IMAGE_NAME = raga_seeker
CONTAINER_NAME = raga_seeker
CONTAINER_EXPOSED_PORT = 8082

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME) .

# Run the container (detached mode)
run: stop
	docker run -d -p $(CONTAINER_EXPOSED_PORT):8000 --name $(CONTAINER_NAME) $(IMAGE_NAME)

# Stop and remove the container if it's running
stop:
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true

# Remove the Docker image
clean: stop
	docker rmi $(IMAGE_NAME) || true

# Run a shell inside the running container
shell:
	docker exec -it $(CONTAINER_NAME) sh

# Rebuild and restart the server
rebuild: clean build run
