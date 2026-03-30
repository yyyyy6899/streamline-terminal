import streamlit as st
import subprocess
import os

st.set_page_config(page_title="Web Terminal", layout="wide")

st.title("💻 Web Terminal (Full Access)")
st.write("Run Linux commands (private use only)")

# Session state
if "history" not in st.session_state:
    st.session_state.history = []

if "cwd" not in st.session_state:
    st.session_state.cwd = os.getcwd()

# Show current directory
st.info(f"📂 Current Directory: {st.session_state.cwd}")

# Input
command = st.text_input("Enter Linux command:")

# Run command
if st.button("Run Command"):
    if command.strip() == "":
        st.warning("Please enter a command")
    else:
        try:
            # Handle cd separately
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

            # Save history
            st.session_state.history.append({
                "command": command,
                "output": output
            })

        except Exception as e:
            st.error(str(e))

# Output display
st.subheader("📄 Terminal Output")

if st.session_state.history:
    for item in reversed(st.session_state.history):
        st.code(f"$ {item['command']}\n{item['output']}", language="bash")
else:
    st.write("No commands run yet.")

# Clear history
if st.button("Clear History"):
    st.session_state.history = []
