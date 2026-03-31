import streamlit as st
import subprocess
import os

st.set_page_config(page_title="Web Terminal", layout="wide")

# -------------------------------------------------------------------
# Sidebar for dark mode toggle
with st.sidebar:
    dark_mode = st.toggle("🌙 Dark Mode", key="dark_mode")
    if dark_mode:
        st.markdown(
            """
            <style>
            /* Global dark theme overrides */
            .stApp {
                background-color: #0e1117;
                color: #fafafa;
            }
            /* Terminal output area */
            .terminal-container {
                background-color: #1e1e2e;
                border-radius: 8px;
                padding: 1rem;
                font-family: monospace;
                color: #f8f8f2;
            }
            .stCodeBlock {
                background-color: #282a36 !important;
            }
            /* Sidebar background */
            section[data-testid="stSidebar"] {
                background-color: #1e1e2e;
            }
            /* Info box */
            .stAlert {
                background-color: #2d2f3a !important;
                color: #f8f8f2 !important;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

st.title("💻 Web Terminal (Full Access)")
st.write("Run Linux commands (private use only)")

# Session state
if "history" not in st.session_state:
    st.session_state.history = []

if "cwd" not in st.session_state:
    st.session_state.cwd = os.getcwd()

# Show current directory
st.info(f"📂 Current Directory: {st.session_state.cwd}")

# ===== Button to install tmate (unchanged) =====
if st.button("Install tmate"):
    try:
        st.info("Installing tmate... (requires sudo, you may be prompted for password)")
        result = subprocess.run(
            "sudo apt update && sudo apt install -y tmate",
            shell=True,
            capture_output=True,
            text=True
        )
        output = result.stdout if result.stdout else result.stderr
        st.code(output, language="bash")
        st.success("tmate installation finished.")
    except Exception as e:
        st.error(f"Failed to install tmate: {e}")

# -------------------------------------------------------------------
# Terminal-like input and output area
st.markdown("### 📟 Terminal")

# Container for scrollable terminal output (fixed height, border)
terminal_container = st.container(height=400, border=True)

# Display terminal history in order (oldest first)
with terminal_container:
    if st.session_state.history:
        for item in st.session_state.history:
            st.code(f"$ {item['command']}\n{item['output']}", language="bash")
    else:
        st.write("No commands run yet. Type a command below and press Enter.")

# Chat input for commands – behaves like a terminal: press Enter to run
command = st.chat_input("Enter Linux command...")

if command:
    # Process the command
    try:
        # Handle cd separately to update session cwd
        if command.startswith("cd "):
            path = command.replace("cd ", "").strip()
            new_path = os.path.abspath(os.path.join(st.session_state.cwd, path))

            if os.path.isdir(new_path):
                st.session_state.cwd = new_path
                output = f"Changed directory to {new_path}"
            else:
                output = f"No such directory: {path}"

        else:
            result = subprocess.run(
                command,
                shell=True,
                cwd=st.session_state.cwd,
                capture_output=True,
                text=True
            )

            output = ""
            if result.stdout:
                output += result.stdout
            if result.stderr:
                output += result.stderr

            if output.strip() == "":
                output = "[No output]"

        # Save to history
        st.session_state.history.append({
            "command": command,
            "output": output
        })

        # Force a rerun so the new output appears instantly
        st.rerun()

    except Exception as e:
        st.error(str(e))

# -------------------------------------------------------------------
# Clear history button (unchanged)
if st.button("Clear History"):
    st.session_state.history = []
    st.rerun()
