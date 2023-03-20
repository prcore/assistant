import os
from copy import deepcopy

import streamlit as st

from langchain.chains import ConversationChain
from langchain.chains.question_answering import load_qa_chain
from langchain.docstore.document import Document
from langchain.llms import OpenAI
from langchain.memory import ConversationSummaryBufferMemory
from langchain.prompts import PromptTemplate
from langchain.vectorstores import Chroma

import config
from index import load_vector_store


def clear_input() -> None:
    st.session_state["input"] = deepcopy(st.session_state["temp"])
    st.session_state["input_disabled"] = True
    st.session_state["temp"] = ""


def get_input() -> str:
    st.text_input(
        label="You: ",
        value="",
        placeholder=("Your AI assistant here! Ask me anything about PrCore"
                     if not st.session_state.input_disabled else "Getting response..."),
        label_visibility="hidden",
        key="temp",
        on_change=clear_input,
        disabled=st.session_state.input_disabled,
    )
    return st.session_state["input"]


def get_response(query: str) -> str:
    try:
        chain = get_chain()
        if st.session_state.magic_mode:
            response = chain.predict(input=query)
            return response.strip()
        else:
            response = chain({"input_documents": get_documents(query), "human_input": query}, return_only_outputs=True)
            return response.get("output_text").strip()
    except Exception as e:
        print(f"Get response error: {e}")
        return "Connection error. Please try again later."


def get_chain():
    if "chain" not in st.session_state:
        st.session_state["chain"] = load_qa_chain(
            llm=OpenAI(
                temperature=0,
                model_name=config.MODEL_NAME,
                request_timeout=int(os.getenv("OPENAI_TIMEOUT", 15))
            ),
            chain_type="stuff",
            memory=get_memory(),
            prompt=get_prompt()
        )
    return st.session_state["chain"]


def get_magic_chain():
    return ConversationChain(
        llm=OpenAI(
            temperature=0,
            model_name=config.MODEL_NAME,
            request_timeout=int(os.getenv("OPENAI_TIMEOUT", 15))
        ),
        memory=get_memory()
    )


def get_memory() -> ConversationSummaryBufferMemory:
    if "memory" not in st.session_state:
        st.session_state["memory"] = new_memory()
    return st.session_state["memory"]


def new_memory() -> ConversationSummaryBufferMemory:
    llm = OpenAI(model_name=config.MODEL_NAME, request_timeout=int(os.getenv("OPENAI_TIMEOUT", 15)))
    memory = ConversationSummaryBufferMemory(
        llm=llm,
        memory_key="chat_history",
        input_key="human_input"
    )
    return memory


def new_magic_memory() -> ConversationSummaryBufferMemory:
    llm = OpenAI(model_name=config.MODEL_NAME, request_timeout=int(os.getenv("OPENAI_TIMEOUT", 15)))
    memory = ConversationSummaryBufferMemory(llm=llm)
    return memory


def get_prompt() -> PromptTemplate:
    if not st.session_state["magic_mode"]:
        with open(config.PROMPT_PATH, "r") as f:
            template = f.read()
        prompt = PromptTemplate(
            input_variables=["chat_history", "human_input", "context"],
            template=template
        )
    else:
        template = ("The AI is talkative and provides lots of specific details from its context. "
                    "If the AI does not know the answer to a question, it truthfully says it does not know.\n\n"
                    "{chat_history}\n"
                    "Human: {human_input}\n"
                    "AI:")
        prompt = PromptTemplate(
            input_variables=["chat_history", "human_input"],
            template=template
        )
    return prompt


def get_documents(query: str) -> list[Document]:
    docsearch = get_docsearch()
    return docsearch.similarity_search(query)


def get_docsearch() -> Chroma:
    if "docsearch" not in st.session_state:
        st.session_state["docsearch"] = load_vector_store()
    return st.session_state["docsearch"]
