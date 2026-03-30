import streamlit as st
import subprocess
import os

st.set_page_config(page_title="Code Server Launcher", layout="wide")

st.title("💻 Code-Server Web IDE")
st.write("Install and run code-server on port 7000")

# Store logs
if "logs" not in st.session_state:
    st.session_state.logs = ""

# Install code-server
if st.button("Install code-server"):
    try:
        install_cmd = "curl -fsSL https://code-server.dev/install.sh | sh"
        result = subprocess.run(install_cmd, shell=True, capture_output=True, text=True)
        st.session_state.logs += result.stdout + result.stderr
        st.success("code-server installed successfully")
    except Exception as e:
        st.error(str(e))

# Run code-server
if st.button("Start code-server (port 7000)"):
    try:
        run_cmd = "code-server --bind-addr 0.0.0.0:7000 > code-server.log 2>&1 &"
        subprocess.run(run_cmd, shell=True)

        st.success("code-server started on port 7000")

        # Read password file
        password_cmd = "cat ~/.config/code-server/config.yaml"
        result = subprocess.run(password_cmd, shell=True, capture_output=True, text=True)

        st.session_state.logs += result.stdout

    except Exception as e:
        st.error(str(e))

# Show logs / password
st.subheader("📄 Logs & Password Info")
if st.session_state.logs:
    st.code(st.session_state.logs, language="bash")
else:
    st.write("No logs yet")

# Show access info
st.subheader("🌐 Access Info")
st.info("Open in browser: http://YOUR_SERVER_IP:7000")
