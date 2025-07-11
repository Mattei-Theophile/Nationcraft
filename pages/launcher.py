import os

import streamlit as st
from sympy.strategies.core import switch

from nationsglory.bots.launcher.launch_ng import NationsGloryLauncher

linux_dir = None
# Main page content
st.markdown("# Launcher 💻")
st.sidebar.markdown("# Launcher 💻")

operatingSystem= st.radio("Select an option", ["Window","Mac", "Linux"])
if operatingSystem :
    if operatingSystem == "Linux":
        linux_dir = st.text_input("entre le chemin vers le l'éxécutable", placeholder="/home/user/.../nationsglory")

link_launcher = st.button("Lier le launcher")

if link_launcher:
        match operatingSystem:
            case "Window":
                st.session_state.ng_dir = operatingSystem
            case "Mac":
                st.session_state.ng_dir = operatingSystem
            case "Linux":
                st.session_state.ng_dir = linux_dir


if st.button("Launch NationsGlory"):
    import nationsglory.bots.launcher.launch_ng
    NationsGloryLauncher()
    if NationsGloryLauncher.launch_nationsglory:
        st.success("NationsGlory launched successfully")
    else:
        st.error("Error launching NationsGlory")

st.write("Select an option for parameter the launcher")


