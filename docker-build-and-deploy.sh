# Take latest pull from git, build docker image and run on docker-compose
git pull

# Build docker image
docker build -t cloud-lab-app:latest .

# Run docker-compose
docker-compose up -d