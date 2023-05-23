import csv
from google.cloud import dialogflow
from google.api_core.exceptions import InvalidArgument
import streamlit as st
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
import os
import re
import ast
from fuzzywuzzy import fuzz
from datetime import datetime
from traitlets import FuzzyEnum

st.set_page_config(page_title="Chatbot", initial_sidebar_state="collapsed")
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

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

    intent=response.query_result.intent.display_name
    entities_dict = {}
    formatted_str_with_quotes = str({})

    for entity, value in response.query_result.parameters.items():
        if value:
            entities_dict[entity] = value
    for entity, value in entities_dict.items():
        if isinstance(value, list):
            value_str = ', '.join(value)
            formatted_str = "{{{}: '{}'}}".format(entity, value_str)
            formatted_str_with_quotes = re.sub(r'(\w+)(?=:)', r"'\1'", formatted_str)
            
        else:
            formatted_str = "{{{}: '{}'}}".format(entity, value[0])
            formatted_str_with_quotes = re.sub(r'(\w+)(?=:)', r"'\1'", formatted_str)
    entity = ast.literal_eval(formatted_str_with_quotes)
    return intent,entity
# def log_interaction(user_input, response):
#     timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     log_entry = f"[{timestamp}] User: {user_input}\n[{timestamp}] Chatbot: {response}\n\n"
#     with open("chatlog.txt", "a") as file:
#         file.write(log_entry)


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
    input_text = st.text_input("You: ", "", key="input", on_change=clear_text)
    
    with open(st.session_state["f_path"], "a") as f:
        f.write(f"[{datetime.now()}]: [USER]:         {st.session_state.input_text} \n")
    return st.session_state.input_text

with input_container:
    user_input = get_text()

def generate_response(prompt):
    intent,entity = diagflow(prompt)
    def load_job_data(file_path, encoding='utf-8'):
        jobs = []
        with open(file_path, 'r', encoding=encoding) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                jobs.append(row)
        return jobs

    def fuzzy_match(entity_value, job_value):
        if isinstance(entity_value, list):
            return any(fuzz.partial_ratio(val.lower(), job_value.lower()) >= 80 for val in entity_value)
        else:
            return fuzz.partial_ratio(entity_value.lower(), job_value.lower()) >= 80

    def generate_response(intent, entities, jobs):
        filtered_jobs = jobs
        for entity, value in entities.items():
            filtered_jobs = [job for job in filtered_jobs if fuzzy_match(value, job[entity])]

        if filtered_jobs:
            job = filtered_jobs[0]
            if intent == 'education_required':
                if 'education_required' in job:
                    return f"The education required for {', '.join(entities.values())} is {job['education_required']}."
            elif intent == 'experience_required':
                if 'experience_required' in job:
                    return f"The experience required for {', '.join(entities.values())} is {job['experience_required']} years."
            elif intent == 'job_prospects':
                jobs = [job['job_title'] for job in filtered_jobs]
                job_list = ', '.join(jobs)
                return f"The job prospects for {', '.join(entities.values())} are: {job_list}."
            elif intent == 'list_of_companies':
                companies = [job['COMPANY_NAME'] for job in filtered_jobs]
                companies_list = ', '.join(companies)
                return f"The list of companies offering {', '.join(entities.values())} positions is: {companies_list}."
            elif intent == 'qualifications_required':
                quali = [job['QUALIFICATIONS'] for job in filtered_jobs]
                quali_list = ', '.join(quali)
                return f"The qualifications required for {', '.join(entities.values())} are: {quali_list}."
            elif intent == 'salary_info':
                if 'salary_info' in job:
                    return f"The salary information for {', '.join(entities.values())} is: {job['salary_info']}."
            elif intent == 'skills_required':
                skill = [job['SKILLS'] for job in filtered_jobs]
                skill_list = ', '.join(skill)
                return f"The skills required for {', '.join(entities.values())} are: {skill_list}."
        return "I'm sorry, I couldn't find the information you requested."
    file_path = 'final_df.csv'
    jobs = load_job_data(file_path, encoding='utf-8')
    response = generate_response(intent, entity, jobs)
    # log_interaction(prompt, response)
    with open(st.session_state["f_path"], "a") as f:
        f.write(f"[{datetime.now()}]: BOT:         {response} \n")
    return(response)
with response_container:
    if user_input:
        response = generate_response(user_input)
        st.session_state.past.append(user_input)
        st.session_state.generated.append(response)
    
    if st.session_state["generated"]:
        for i in range(len(st.session_state["generated"])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
            message(st.session_state["generated"][i], key=str(i) + "_bot")

with st.sidebar:
    st.sidebar.title("Logs")
    try:
        with open(st.session_state["f_path"], "r") as f:
            st.download_button("Download Logs", f, file_name=now + ".txt", mime="text/csv")
    except:
        st.info("Start Chatting to get the logs")
