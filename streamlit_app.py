import streamlit as st
import subprocess
import os

st.set_page_config(page_title="Terminal Portfolio", layout="wide")

# ---------------------- SESSION STATE ----------------------
if "history" not in st.session_state:
    st.session_state.history = []

if "cwd" not in st.session_state:
    st.session_state.cwd = os.getcwd()

# ---------------------- STYLES ----------------------
st.markdown("""
<style>
body {
    background-color: #0d1117;
}
.terminal {
    background-color: #0d1117;
    color: #c9d1d9;
    font-family: monospace;
    padding: 20px;
    border-radius: 10px;
    height: 500px;
    overflow-y: auto;
    border: 1px solid #30363d;
}
.prompt {
    color: #58a6ff;
}
.command {
    color: #c9d1d9;
}
.output {
    color: #8b949e;
}
.title {
    color: #58a6ff;
    font-size: 22px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------- ASCII HEADER ----------------------
header = r"""
  _____       _   _       _             
 / ____|     | | (_)     | |            
| (___   __ _| |_ _ _ __ | | ___   __ _ 
 \___ \ / _` | __| | '_ \| |/ _ \ / _` |
 ____) | (_| | |_| | | | | | (_) | (_| |
|_____/ \__,_|\__|_|_| |_|_|\___/ \__, |
                                   __/ |
                                  |___/ 
"""

# ---------------------- BUILT-IN COMMANDS ----------------------
def handle_builtin(cmd):
    if cmd == "help":
        return """Available commands:
- help     → show this message
- about    → about me
- clear    → clear terminal
- ls, pwd, cd → system commands supported
"""
    elif cmd == "about":
        return """Hi, my name is Your Name!
I'm a full-stack developer.
I build terminal-style web apps and cool UI projects."""
    elif cmd == "clear":
        st.session_state.history = []
        st.rerun()
    return None

# ---------------------- TERMINAL OUTPUT ----------------------
terminal_content = f"<pre class='output'>{header}\nWelcome to my terminal portfolio.\nType 'help' to get started.\n\n</pre>"

for item in st.session_state.history:
    terminal_content += f"""
    <div>
        <span class="prompt">visitor@web-terminal:~$</span>
        <span class="command">{item['command']}</span>
    </div>
    <pre class="output">{item['output']}</pre>
    """

st.markdown(f"<div class='terminal' id='terminal'>{terminal_content}</div>", unsafe_allow_html=True)

# Auto scroll
st.markdown("""
<script>
var terminal = document.getElementById("terminal");
if (terminal) {
    terminal.scrollTop = terminal.scrollHeight;
}
</script>
""", unsafe_allow_html=True)

# ---------------------- INPUT ----------------------
command = st.text_input("visitor@web-terminal:~$", key="input")

if command:
    command = command.strip()

    # Built-in commands
    built_in = handle_builtin(command)

    if built_in is not None:
        output = built_in
    else:
        try:
            if command.startswith("cd "):
                path = command[3:].strip()
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
                output = result.stdout + result.stderr
                if output.strip() == "":
                    output = "[No output]"
        except Exception as e:
            output = str(e)

    st.session_state.history.append({
        "command": command,
        "output": output
    })

    st.rerun()
