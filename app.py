import streamlit as st
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
st.set_page_config(page_title="Chatbot")

st.title("Chatbot")
if "generated" not in st.session_state:
    st.session_state["generated"] = ["Hello! Welcome"]

if "past" not in st.session_state:
    st.session_state["past"] = ["Hi!"]

input_container = st.container()
colored_header(label='', description='', color_name='blue-30')
response_container = st.container()

def get_text():
    with st.form("my_form", clear_on_submit=True):
        input_text = st.text_input("You: ", "", key="input")
        submitted = st.form_submit_button("Go")
        if submitted:
            return input_text
with input_container:
    user_input = get_text()

def generate_response(prompt):
    response =  prompt
    return response

with response_container:
    if user_input:
        response = generate_response(user_input)
        st.session_state.past.append(user_input)
        st.session_state.generated.append(response)
    
    if st.session_state["generated"]:
        for i in range(len(st.session_state["generated"])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
            message(st.session_state["generated"][i], key=str(i) + "_bot")
