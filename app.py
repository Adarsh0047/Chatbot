from google.cloud import dialogflow
from google.api_core.exceptions import InvalidArgument
from n_gram import skill_dict, title_dict, get_company
from n_gram import *
import streamlit as st
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
import os





def diagflow(inp):
    DIALOG_FLOW_PROJECT_ID = "tribal-archery-386911"
    DIALOGFLOW_LANGUAGE_CODE = "en"
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'private_key.json'
    text_input = dialogflow.TextInput(text=inp, language_code=DIALOGFLOW_LANGUAGE_CODE)
    SESSION_ID = 'me'
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOG_FLOW_PROJECT_ID, SESSION_ID)
    query_input = dialogflow.QueryInput(text=text_input)
    try:
      response = session_client.detect_intent(request={"session": session, "query_input": query_input})
    except InvalidArgument:
      raise
    for entity in response.query_result.parameters:
      if entity == "jobtitle":
        job_title = response.query_result.parameters[entity]
      if entity == "location":
        location = response.query_result.parameters[entity]
    if job_title == "":
        for entitity in response.query_result.parameters:
            if entitity == "skills":
                skills = response.query_result.parameters[entitity]
    return job_title, location, skills







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
    job_title, location, skills = diagflow(prompt)
    if job_title and location is not '':
        try:
            response = f"The {job_title} jobs in {location} are available at {match_location(job_title, location, title_dict)}"
        except:
            response = f"The jobs with {job_title} skills in {location} are available at {match_location(job_title, location, skill_dict)}"
    elif job_title == '' and skills == '':
        response = "Sorry request cannot be fulfilled"
    elif job_title == '' and skills is not '':
        response = f"The {job_title} jobs are available at {get_company(job_title, skill_dict)}"
    else:
        response = f"The {job_title} jobs are available at {get_company(job_title, title_dict)}"
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
