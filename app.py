import io
import streamlit as st
from contextlib import redirect_stdout
from dotenv import load_dotenv
from src.formatting import parse_agent_chain, history
from src.llm import run_agent, load_memory


load_dotenv()

if 'memory' not in st.session_state:
    st.session_state.memory = load_memory()

if 'prompts' not in st.session_state:
    st.session_state.prompts = []

if 'chains' not in st.session_state:
    st.session_state.chains = []


output = st.empty()
input = st.empty()
with input.container():
    text = st.text_input('Enter Query', key=f'a{0}')

    tools = st.multiselect(
        'Select tools',
        ['python_repl', 'terminal', 'llm-math', 'serpapi'],
        [],
        key=f'b{1}',
    )
    submit = st.button('Submit', key=f'c{2}')


def run_agent_chain(i=1):
    global submit
    output.markdown(history(
        st.session_state.prompts,
        st.session_state.chains,
    ), unsafe_allow_html=True)

    if submit:
        submit = False
        st.session_state.prompts.append(text)
        try:
            with io.StringIO() as buf, redirect_stdout(buf):
                final_output = run_agent(
                    tools,
                    st.session_state.memory,
                    text,
                )
                chain = buf.getvalue()
            print(chain)
            st.session_state.chains.append(
                f'{parse_agent_chain(chain)}\n\n**{final_output}**'
            )

        except ValueError as e:
            err = f':red[{e}]'
            st.session_state.chains.append(err)

        run_agent_chain(i + 1)


run_agent_chain()
