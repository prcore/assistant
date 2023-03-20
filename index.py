import os

import streamlit as st
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.indexes.vectorstore import VectorstoreIndexCreator

import config


@st.cache_data
def create_index():
    if os.getenv("TEXT", None) is not None:
        print("Testing mode, skipping the creation of the index")
        return
    if os.path.exists(config.INDEX_PATH) and os.path.isdir(config.INDEX_PATH):
        print("Index already exists, skipping the creation")
        return
    if not os.path.exists(config.DOCS_PATH) or not os.path.isdir(config.DOCS_PATH):
        raise SystemExit("Docs path does not exist or is not a non-empty directory")
    try:
        loader = DirectoryLoader(config.DOCS_PATH, loader_cls=TextLoader)
        index_creator = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory": config.INDEX_PATH})
        docsearch = index_creator.from_loaders([loader])
        docsearch.vectorstore.persist()  # noqa
    except Exception as e:
        raise SystemExit(e)


@st.cache_resource
def load_vector_store() -> Chroma:
    print("Loading vector store...")
    docsearch = Chroma(persist_directory=config.INDEX_PATH, embedding_function=OpenAIEmbeddings())
    print("Loaded vector store")
    return docsearch
