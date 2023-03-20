import logging
import os
from copy import deepcopy

import streamlit as st
from streamlit.delta_generator import DeltaGenerator

import config

# Enable logging
logger = logging.getLogger(__name__)


def set_web():
    st.set_page_config(page_title=os.getenv("WEB_TITLE", "Docs Assistant"), layout="wide")
    st.title(os.getenv("WEB_TITLE", "Docs Assistant"))

    with open(config.INTRO_PATH, "r") as f:
        intro_text = f.read()
    st.markdown(intro_text, unsafe_allow_html=True)

    with open(config.SIDEBAR_PATH, "r") as f:
        sidebar_text = f.read()
    with st.sidebar:
        st.title(os.getenv("SIDEBAR_TITLE", "Links"))
        st.markdown(sidebar_text, unsafe_allow_html=True)

    if st.session_state.get("magic_mode", False):
        with open(config.MAGIC_PATH, "r") as f:
            magic_text = f.read()
        st.markdown(magic_text, unsafe_allow_html=True)

    hide_menu_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_menu_style, unsafe_allow_html=True)


def display_conversation(container: DeltaGenerator):
    with container.container():
        message_containers = [st.empty() for _ in range(len(st.session_state["human"]) * 2)]
        human_list = deepcopy(st.session_state["human"])
        ai_list = deepcopy(st.session_state["ai"])

        if len(human_list) > len(ai_list):
            ai_list.append("...")

        for i, (human_msg, ai_msg) in enumerate(zip(human_list, ai_list)):
            message_containers[i * 2].info(human_msg, icon="💡")
            message_containers[i * 2 + 1].success(ai_msg, icon="🤖")
