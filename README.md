# Host-AI-App-ECS-Bedrock
AI-Powered Web Application using Amazon Bedrock & ECS Fargate

## Introduction:
This project focuses on Building the description for the user's uploaded Image using Amazon Bedrock and Anthropic’s Claude 3 Haiku Foundation Model. The frontend is running in the Elastic container service cluster and the task is running using fargate serverless mode and it can scale horizontally depends upon the traffic loads. The backend is running in Lambda and can scale easily depends upon the traffic which inturns invoke the Amazon bedrock Anthropic's claude 3 haiku model and store the response in the dynamo DB.

## Architecture:
![ecs-bedrock](https://github.com/user-attachments/assets/7f7fe69d-5c83-41a7-85ad-52e0d763ce82)

## Project Highlights and Learnings:
1. Version Control:
   Used Git, Github and Dockerhub to store the frontend, backend codebase and the docker images.

2. Containerization :
    Worked and Learned how to containerize the frontend files such as html,css and js.
   
4. Docker :
    Used Docker platform for Containerizing and build the image for the frontend code and ran using docker desktop locally.

4. ECS Cluster:
    Configured the Elastic Container Service Cluster for running the Containerized Image and ensuring scalability and resilience.

5. ECS Task Definition :
     Created the task definition for running the Elastic Container service by pulling the image from  Elastic Container repository.

6. Elastic Container Repository:
   Used to store Docker images with the version control support for streamline deployment of images.

7. Fargate:
   It is serverless mode of running the task in ECS cluster where AWS will provide the compute, storage capacity for running the tasks on demand.

8. IAM:
  Configured IAM roles and policies for secure access control for the lambda and ECS tasks.

9. Load Balancer:
  Deployed a Applocation Load Balancer (NLB) in public subnets to distribute traffic efficiently across the cluster in multiple AZs.

10. VPC Setup:
  Designed a custom VPC from the scratch with public, private, and database subnets across multiple Availability Zones.
