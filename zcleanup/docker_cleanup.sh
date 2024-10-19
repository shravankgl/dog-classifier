#!/bin/bash

echo "Starting Docker cleanup..."

# Stop all running containers
echo "Stopping all running containers..."
docker stop $(docker ps -aq)

# Remove all containers
echo "Removing all containers..."
docker rm $(docker ps -aq)

# Remove all images forcefully
echo "Removing all images forcefully..."
docker images -q | xargs -r docker rmi -f

# Remove all volumes
echo "Removing all volumes..."
docker volume rm $(docker volume ls -q)

# Remove all networks
echo "Removing all networks..."
docker network rm $(docker network ls -q)

# Remove any dangling images, containers, volumes, and networks
echo "Removing any dangling resources..."
docker system prune -a --volumes -f

echo "Docker cleanup complete!"

# List remaining images (if any)
echo "Remaining images:"
docker images

# List remaining containers (if any)
echo "Remaining containers:"
docker ps -a

# List remaining volumes (if any)
echo "Remaining volumes:"
docker volume ls

# List remain