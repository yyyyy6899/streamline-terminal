import streamlit as st
import subprocess

st.set_page_config(page_title="Web Terminal", layout="wide")

st.title("💻 Web Terminal (Linux Commands)")
st.write("Run Linux commands from your browser (limited access recommended)")

# Store command history
if "history" not in st.session_state:
    st.session_state.history = []

# Input box
command = st.text_input("Enter Linux command:")

# Run button
if st.button("Run Command"):
    if command.strip() == "":
        st.warning("Please enter a command")
    else:
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True
            )

            output = result.stdout if result.stdout else result.stderr

            # Save history
            st.session_state.history.append({
                "command": command,
                "output": output
            })

        except Exception as e:
            st.error(str(e))

# Show output
st.subheader("📄 Output")

if st.session_state.history:
    for item in reversed(st.session_state.history):
        st.code(f"$ {item['command']}\n{item['output']}", language="bash")
else:
    st.write("No commands run yet.")

# Clear history
if st.button("Clear History"):
    st.session_state.history = []
