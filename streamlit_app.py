import streamlit as st
import subprocess
import os

st.set_page_config(page_title="Web Terminal", layout="wide")

# Session state
if "history" not in st.session_state:
    st.session_state.history = []

if "cwd" not in st.session_state:
    st.session_state.cwd = os.getcwd()

# Dark mode toggle (moved from sidebar to main area)
dark_mode = st.checkbox("🌙 Dark Mode", value=False)
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
            border: 1px solid #3a3a4a;
            overflow-y: auto;
            height: 400px;
        }
        .stCodeBlock {
            background-color: #282a36 !important;
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

# Show current directory
st.info(f"📂 Current Directory: {st.session_state.cwd}")

# -------------------------------------------------------------------
# Terminal display area (with auto‑scroll)
# Build the terminal content as a single block of text
terminal_content = ""
for item in st.session_state.history:
    terminal_content += f"$ {item['command']}\n{item['output']}\n"

# Wrap in a scrollable div with a fixed height and monospace font
st.markdown(
    f"""
    <div id="terminal-output" class="terminal-container" style="
        background-color: {'#1e1e2e' if dark_mode else '#f0f2f6'};
        color: {'#f8f8f2' if dark_mode else '#000000'};
        border: 1px solid {'#3a3a4a' if dark_mode else '#dddddd'};
        font-family: monospace;
        font-size: 14px;
        padding: 10px;
        border-radius: 8px;
        overflow-y: auto;
        height: 400px;
        white-space: pre-wrap;
        word-wrap: break-word;
    ">
    {terminal_content if terminal_content else "No commands run yet. Type a command below and press Enter."}
    </div>
    """,
    unsafe_allow_html=True,
)

# JavaScript to auto‑scroll to bottom (runs after each rerun)
st.markdown(
    """
    <script>
    (function() {
        var terminalDiv = document.getElementById('terminal-output');
        if (terminalDiv) {
            terminalDiv.scrollTop = terminalDiv.scrollHeight;
        }
    })();
    </script>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------------------------
# Terminal input – behaves like a real terminal: press Enter to run
command = st.chat_input("Enter Linux command...")

if command:
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

        # Force rerun to display new output and trigger auto‑scroll
        st.rerun()

    except Exception as e:
        st.error(str(e))

# -------------------------------------------------------------------
# Clear history button (unchanged)
if st.button("Clear History"):
    st.session_state.history = []
    st.rerun()
