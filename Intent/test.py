import streamlit as st
from streamlit_chat import message
from streamlit_extras.add_vertical_space import add_vertical_space


if "last" not in st.session_state:
    st.session_state.last = ["Hello"]
    
else:
    # st.session_state.last.append("Hi")
    pass
st.write(len(st.session_state.last))

# colored_header(label='', description='', color_name='blue-30')


if "input_text" not in st.session_state:
        st.session_state.input_text = ""
def clear_text():
    st.session_state.input_text = st.session_state.input
    st.session_state.input = ""
    return st.session_state.input_text
response_container = st.container()
input_container = st.container()
def get_text():
    input_text = st.text_input("You: ", "", key="input", on_change=clear_text)
    return input_text
def generate_response(prompt):
    return prompt


if len(st.session_state.last)%2 !=  0:
    with input_container:
        user_input = get_text()
    if 'generated' not in st.session_state:
        st.session_state['generated'] = ["I'm HugChat, How may I help you?"]

    if 'past' not in st.session_state:
        st.session_state['past'] = ['Hi!']
    with response_container:
        if user_input:
            response = generate_response(user_input)
            st.session_state.past.append(user_input)
            st.session_state.generated.append(response)

        if st.session_state['generated']:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
                message(st.session_state['generated'][i], key=str(i))
        st.session_state.last = st.session_state.last[:-1]
    if "text" not in st.session_state:
        st.session_state.last = ["Hello"]
    else:
        st.session_state.last.append(user_input)
    st.write(st.session_state.input_text)




def on_select():
    st.session_state.last.append(True)
st.checkbox("Hello",on_change=on_select)
