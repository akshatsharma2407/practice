#!/bin/bash
# Login to AWS ECR
aws ecr get-login-password --region ap-southeast-2 | docker login --username AWS --password-stdin 851725541946.dkr.ecr.ap-southeast-2.amazonaws.com

# Pull the latest image
docker pull 851725541946.dkr.ecr.ap-southeast-2.amazonaws.com/emotion1:v3

docker stop campusx-app || true
docker rm campusx-app || true

# Run a new container
docker run -d -p 80:5000 -e AKSHAT=8a0f419a615e6eae881208edae20992709002635 --name campusx-app 851725541946.dkr.ecr.ap-southeast-2.amazonaws.com/emotion1:v3