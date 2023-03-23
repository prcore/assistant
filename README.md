# Docs Assistant

[![](https://img.shields.io/github/actions/workflow/status/prcore/assistant/main.yml?label=Docker%20compose%20service)](https://github.com/prcore/assistant/actions/workflows/main.yml)
[![](https://img.shields.io/website?label=Demo%20service&url=https%3A%2F%2Fprcore-assistant.chaos.run)](https://prcore-assistant.chaos.run)

This is a simple tool to help you to create an AI-powered chatbot for your documentation.

What it used:

- LangChain: for embedding and similarity calculation
- OpenAI GPT-3.5 turbo: for conversation summary and response generation
- Streamlit: for web interface

## Diagram

First, use all documents + LangChain + OpenAI Embedding to create a Vector Store.

When receiving a user's question, generate the vector of the question and obtain K most similar document paragraphs as part of prompt for background information.

At the same time, retrieve the latest K messages in the conversation history and summary as part of prompt for historical messages.

Then use the user's original message as the final prompt question and ask OpenAI's model for an answer.

Finally, record this question-answer pair as part of Memory storage.

![](https://i.imgur.com/AtUkJnC.png)

## Demo

You can try the demo at [https://prcore-assistant.chaos.run](https://prcore-assistant.chaos.run).

This is a screenshot of the demo:

![](https://i.imgur.com/yTXOoVJ.png)

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
the assistant will allow user to ask any question. 

Note: In this mode, the assistant won't use the knowledge base.
