# Docs Assistant

This is a simple tool to help you to create an AI-powered chatbot for your documentation.

What it used:

- LangChain: for embedding and similarity calculation
- OpenAI GPT-3.5 turbo: for conversation summary and response generation
- Streamlit: for web interface

## Demo

You can try the demo at [https://prcore-assistant.chaos.run](https://prcore-assistant.chaos.run).

## Deployment

Follow the steps below to deploy the service.

1. Make sure you installed `docker` and `docker-compose` on your machine.
2. Clone this repository.
3. Run `cd scripts && bash prepare.sh` to prepare the environment. 
4. You will be asked to edit the `.env` file. Please fill in each field with the correct information. You will also need to edit other files accordingly, including the prompt template.
5. Then place your documentation files (text files only) in `data/docs` folder.
6. Run `cd scripts && bash install.sh` to install the service.

The service will be deployed on `localhost:<WEB_PORT>`.

## Magic mode

If you defined `MAGIC_WORD` in `.env` file, when user input the magic word,
the assistant will allow user to ask any question, even not related to the documentation.
