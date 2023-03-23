import os
from copy import deepcopy

import streamlit as st
from streamlit import runtime
from streamlit.delta_generator import DeltaGenerator
from streamlit.runtime.scriptrunner import get_script_run_ctx

import config


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
        if not st.session_state.get("celebrated", False):
            st.balloons()
            st.session_state["celebrated"] = True
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


def get_ip():
    result = None
    try:
        ctx = get_script_run_ctx()
        if ctx is None:
            return None
        session_info = runtime.get_instance().get_client(ctx.session_id)
        if session_info is None:
            return None
        result = session_info.request.headers.get("X-Real-IP")  # noqa
    except Exception as e:
        print(e)
    return result
