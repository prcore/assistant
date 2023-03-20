import os
from random import choice
from string import ascii_letters, digits

import streamlit as st
from streamlit.delta_generator import DeltaGenerator

import chat
import index
import web


def init_session_state() -> None:
    if "human" not in st.session_state:
        st.session_state["human"] = []
    if "ai" not in st.session_state:
        st.session_state["ai"] = []
    if "input" not in st.session_state:
        st.session_state["input"] = ""
    if "input_disabled" not in st.session_state:
        st.session_state["input_disabled"] = False
    if "magic_mode" not in st.session_state:
        st.session_state["magic_mode"] = False


def check_input(container: DeltaGenerator, query: str) -> None:
    print(f"Query: {query}")

    if not query:
        return

    if query == os.getenv("MAGIC_WORD", "".join(choice(ascii_letters + digits) for _ in range(16))):
        st.session_state["magic_mode"] = True
        st.session_state["memory"] = chat.new_magic_memory()
        st.session_state["chain"] = chat.get_magic_chain()
        st.session_state["human"] = []
        st.session_state["ai"] = []
        st.session_state["input_disabled"] = False
        st.session_state["input"] = ""
        st.experimental_rerun()
        return

    st.session_state["input"] = ""
    st.session_state.human.append(query)
    web.display_conversation(container)

    output = chat.get_response(query)
    st.session_state["input_disabled"] = False
    st.session_state.ai.append(output)
    web.display_conversation(container)
    st.experimental_rerun()


if __name__ == '__main__':
    web.set_web()
    init_session_state()
    index.load_vector_store()
    conversation_container = st.empty()
    web.display_conversation(conversation_container)
    user_input = chat.get_input()
    check_input(conversation_container, user_input)
