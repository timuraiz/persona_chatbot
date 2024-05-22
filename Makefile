IMAGE_NAME=bot
CONTAINER_NAME=bot-container

all: build run

build:
	docker build -t $(IMAGE_NAME) .

run:
	docker run -d --name $(CONTAINER_NAME) -p 4000:80 $(IMAGE_NAME)

stop:
	docker stop $(CONTAINER_NAME)
	docker rm $(CONTAINER_NAME)

help:
	@echo "Makefile commands:"
	@echo "make build - Build the Docker image"
	@echo "make run - Run the Docker container"
	@echo "make stop - Stop and remove the Docker container"
	@echo "make all - Build the image and run the container"
