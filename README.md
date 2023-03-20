# PrCore Docs Assistant

This is a simple tool to help you to create an AI-powered chatbot for your documentation.

Follow the steps below to deploy the service.

1. Make sure you installed `docker` and `docker-compose` on your machine.
2. Clone this repository.
3. Run `cd scripts && bash prepare.sh` to prepare the environment. 
4. Then place your documentation files (text files only) in `data/docs` folder.
5. Run `cd scripts && bash install.sh` to install the service.

The service will be deployed on `localhost:<WEB_PORT>`.
