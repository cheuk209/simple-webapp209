# simple-webapp209
## How to access the web app?
You can choose to run locally using `make install` and `make run`, but note you **won't be able to make any real requests** since you would need your own OpenAI API key, which I have stored locally.

To access it on your web browser: http://my-flask-app-alb-297038120.eu-west-1.elb.amazonaws.com/

## The web application
I began writing my web application first. As the instructions noted API calls would be an added bonus, I thought it would be nice to incorporate an OpenAI API service. Essentially it is an AI Chatbot, and I have instructed it to answer all questions related to F1. 

I decided on a F1-themed web app because I've been getting into the sport.

### Tech Stack
I am using HTMX for frontend, to save me from the trouble of javascript and react code. 

Backend is composed of a simple flask app, when you enter a question on the website, it will make calls to the OpenAI API.

## Containerisation
After I was happy with the design and functionality of the web app, I began containerising the application for ease of deployment to AWS. Docker is the obvious choice, and I made sure the container can run locally.

## Infrastructure
All of my AWS resources were deployed with Terraform with the exception of a single S3 bucket, used to store my terraform states. I couldn't be bothered writing out terraform for one single S3 bucket. 

### Networking
I began deploying the networking components needed for the web app. 

I created a VPC, two public and private subnets. Public subnets because I need to have my application Load Balancer to distribute traffic. The private subnets are used to host two different instances of my web app, for increased availability.

Routing tables and a NAT Gateway are used to help navigate API calls made to OpenAI, while allowing the subnets to communicate to each other. 

### ECR
After I built my docker image, I pushed to an ECR registry, so that my ECS cluster can run the Fargate instances in the 2 private subnets as I intended.

### ECS + Fargate
Initially I thought about using EC2, but it is much more costly to run for a simple web app. Fargate reduces the operational burden and it still allows me to hit my objectives. Hence I went with it in the end. Fargate is a serverless compute engine for containers, meaning I don't have to worry about the underlying servers. 

I deployed a ECS cluster, then deployed a ECS service in each of the subnet, with a desired count of 2 for high availability. So that if one instance goes down, my web app would still be active. I also enabled Cloudwatch logs, so I can monitor its logs.

I am opting for a single region architecture choice here, in the case of an actual production level deployment, we might have to worry about multi-region availability.

### Security Groups
Then I added security group to the ECS service, to make sure specific ports are open for traffic from specific sources. This is to restrict traffic to the absolute minimum. 

I have security groups for both my ECS services in the private subnet, as well as my load balancer in the public subnet, for security purposes.

### Load Balancer
I employed an application load balancer to distribute traffic across my various instances, I have a security group deployed to the ALB which would then communicate to the security group of the ECS tasks. ALB also performs health checks on the ECS tasks to ensure they can handle requests.

### Autoscaling groups
I also implemented autoscaling groups that will track the CPU and memory utilisation of the ECS services, so that they may scale up or down depending on activity. This should be a good solution for maintaining uptime and fault-tolerance. 

### Ability to destroy/reuse my solution
Sure, simple run `terraform destroy` and then `terraform apply` :) 


## things to improve
- Using security groups as our primary means of security, no custom NACL created
- really rubbish Terraform structure, I was going through a lot of experimentation/deletion so never bothered to put them in the right categories/modules/subdirectories, so it may be a confusing read
- Similar to last point, I did not make use of Terraform's full potential. A lot of variables could have been defined in another file variables.tf for best practice/readability.
- could have easily used Gunicorn + nginx for a better production backend server
- For real production-grade applications, we could have implemented a forward proxy-server between the app and the load balancer
- As the focus was not on the actual application, there is no concept of different environments or CICD implemented here. Obviously testing and CICD would be tremendously important in an actual life cycle.

## time taken 
Approximately 5-6 hours, I forgot how troublesome it is to write terraform from scratch, as most engineers will be used to reusing existing boilerplaces/templates. IAM permissions were a nightmare, had to do multiple `terraform apply` to get it right sometimes :P 
