import streamlit as st
import subprocess
import os

st.set_page_config(page_title="Web Terminal", layout="wide")

# ---------------- STATE ----------------
if "history" not in st.session_state:
    st.session_state.history = []

if "cwd" not in st.session_state:
    st.session_state.cwd = os.getcwd()

# ---------------- STYLE ----------------
st.markdown("""
<style>
.main-container {
    height: 90vh;
    display: flex;
    flex-direction: column;
}

/* Terminal box */
.terminal-box {
    flex-grow: 1;
    background-color: #0d1117;
    color: #c9d1d9;
    font-family: monospace;
    padding: 20px;
    border-radius: 10px;
    overflow-y: auto;
    border: 1px solid #30363d;
}

/* Prompt */
.prompt {
    color: #58a6ff;
}

/* Command text */
.cmd {
    color: #ffffff;
}

/* Output */
.output {
    color: #8b949e;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- BUILT-IN COMMANDS ----------------
def run_command(command):
    if command == "clear":
        st.session_state.history = []
        return None

    if command == "help":
        return """Available commands:
- help
- clear
- ls, pwd, cd (real commands supported)
"""

    try:
        if command.startswith("cd "):
            path = command[3:].strip()
            new_path = os.path.abspath(os.path.join(st.session_state.cwd, path))

            if os.path.isdir(new_path):
                st.session_state.cwd = new_path
                return f"Changed directory to {new_path}"
            else:
                return f"No such directory: {path}"

        result = subprocess.run(
            command,
            shell=True,
            cwd=st.session_state.cwd,
            capture_output=True,
            text=True
        )

        output = result.stdout + result.stderr
        return output if output.strip() else "[No output]"

    except Exception as e:
        return str(e)

# ---------------- TERMINAL DISPLAY ----------------
terminal_html = ""

for item in st.session_state.history:
    terminal_html += f"""
    <div>
        <span class="prompt">visitor@terminal:{st.session_state.cwd}$</span>
        <span class="cmd"> {item['command']}</span>
    </div>
    <div class="output">{item['output']}</div>
    """

# Layout container
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Terminal output box
st.markdown(f"""
<div class="terminal-box" id="terminal">
{terminal_html if terminal_html else "Welcome to Web Terminal\nType 'help' to start\n"}
</div>
""", unsafe_allow_html=True)

# Auto-scroll
st.markdown("""
<script>
var term = document.getElementById("terminal");
if (term) {
    term.scrollTop = term.scrollHeight;
}
</script>
""", unsafe_allow_html=True)

# ---------------- INPUT (BOTTOM LIKE REAL TERMINAL) ----------------
with st.form(key="terminal_form", clear_on_submit=True):
    cols = st.columns([8, 1])

    with cols[0]:
        command = st.text_input(
            "",
            placeholder="visitor@terminal:~$ type command...",
            label_visibility="collapsed"
        )

    with cols[1]:
        submit = st.form_submit_button("Enter")

    if submit and command:
        output = run_command(command)

        if output is not None:
            st.session_state.history.append({
                "command": command,
                "output": output
            })

        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
