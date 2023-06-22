from google.cloud import dialogflow
from google.api_core.exceptions import InvalidArgument
from n_gram import skill_dict, title_dict, get_company
from n_gram import *
import streamlit as st
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
import os
from datetime import datetime

if not os.path.exists("logs"):
    os.makedirs("logs")
now = datetime.now()
now = re.sub(r'[^\w_. -]', '_', now.strftime("%d/%m/%Y %H:%M:%S"))
path = os.path.join("logs", f"{now}.txt")
if "f_path" not in st.session_state:
  st.session_state["f_path"] = path


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
    job_title = ""
    location = ""
    skills = ""
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


st.set_page_config(page_title="Chatbot", initial_sidebar_state="collapsed")

st.title("Chatbot")
if "generated" not in st.session_state:
    st.session_state["generated"] = ["Hello! Welcome"]

if "past" not in st.session_state:
    st.session_state["past"] = ["Hi!"]


response_container = st.container()
colored_header(label='', description='', color_name='blue-30')
input_container = st.container()


def get_text():
    if "input_text" not in st.session_state:
        st.session_state.input_text = ""

    def clear_text():
        st.session_state.input_text = st.session_state.input
        st.session_state.input = ""
    # with st.form("my_form", clear_on_submit=True):
    input_text = st.text_input("You: ", "", key="input", on_change=clear_text)
    # submitted = st.form_submit_button("Go")
    
    # if submitted:
    # with open(st.session_state["f_path"], "a") as f:
    #     f.write(f"{datetime.now()}: USER:         {input_text} \n")
    return st.session_state.input_text
with input_container:
    user_input = get_text()
st.session_state["rerun"].append("False")
def get_feedback_and_write(query, response):
    with open(st.session_state["f_path"], "a") as f:
        f.write(f"{datetime.now()}: USER:         {query} \n")
    
    col1, col2, col3 = st.columns(3)
    with st.form("my_form"):
        with col1:
            expected = st.checkbox("Answered as expected")
        with col2:
            unexpected = st.checkbox("Unexpected Answer")
        with col3:
            wrong = st.checkbox("Wrong Answer")
        # option = st.selectbox(
        # 'Feedback',
        # ('Expected', 'Unexpected', 'No Answer'))
        if expected == True:
            with open(st.session_state["f_path"], "a") as f:
                f.write(f"[{datetime.now()}] bot(expected):         {response} \n")
            st.session_state["rerun"].append("False")
        elif unexpected == True:
            with open(st.session_state["f_path"], "a") as f:
                f.write(f"[{datetime.now()}] bot(unexpected):         {response} \n")
            st.session_state["rerun"].append("False")
        elif wrong == True:
            with open(st.session_state["f_path"], "a") as f:
                f.write(f"[{datetime.now()}] bot(No Answer):         {response} \n")
            st.session_state["rerun"].append("False")



def generate_response(prompt):
    job_title, location, skills = diagflow(prompt)
    if job_title and location != '':
        try:
            response = f"The {job_title} jobs in {location} are available at {match_location(job_title, location, title_dict)}"
        except:
            response = f"The jobs with {job_title} skills in {location} are available at {match_location(job_title, location, skill_dict)}"
    elif job_title == '' and skills == '':
        response = "Sorry request cannot be fulfilled"
    elif job_title == '' and location == '' and skills != '':
        response = f"The companies that need {skills} skills are {set([(next(iter(company.keys()))) for company in get_company(skills, skill_dict)])}"
    elif job_title == '' and (skills != '' and location != ''):
        response = f"The companies that need {skills} skills are {set([(next(iter(company.keys()))) for company in get_company(skills, skill_dict)])} which are located at {set([(next(iter(company.values()))) for company in get_company(skills, skill_dict)])}"
    else:
        try:
            response = f"The {job_title} jobs are available at {set([(next(iter(company.keys()))) for company in get_company(job_title, title_dict)])} which are located at {set([(next(iter(company.values()))) for company in get_company(job_title, title_dict)])}"
        except:
            response = f"The {job_title} jobs are available at {set([(next(iter(company.keys()))) for company in get_company(job_title, skill_dict)])} which are located at {set([(next(iter(company.values()))) for company in get_company(job_title, skill_dict)])}"
    return response
    # else:
    #      with open(st.session_state["f_path"], "a") as f:
    #         f.write(f"[{datetime.now()}] bot(expected):         {response} \n")
   
with response_container:
    if st.session_state.rerun[-1] == "True":
        if user_input:
            response = generate_response(user_input)
            st.session_state.past.append(user_input)
            st.session_state.generated.append(response)
              

        if st.session_state["generated"]:
            for i in range(len(st.session_state["generated"])):
                message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
                message(st.session_state["generated"][i], key=str(i) + "_bot")
        
    else:
        st.session_state.rerun.append("True")

with st.sidebar:
    st.sidebar.title("Logs")
    try:
        with open(st.session_state["f_path"], "r") as f:
            st.download_button("Download Logs", f, file_name=now + ".txt", mime="text/csv")
    except:
        st.info("Start Chatting to get the logs")
get_feedback_and_write(st.session_state.past[-1],st.session_state.generated[-1]) 

