import requests
import streamlit as st

IBM_API_KEY = "wqHj1OXHRzg9dEKHG0JMXBr6B3hcc5tOcyR6ZnNSBzkQ"
PROJECT_ID  = "36d81710-8763-410a-acc5-f32c33e0e8c2"
WATSONX_URL = "https://eu-gb.ml.cloud.ibm.com"
IAM_URL     = "https://iam.cloud.ibm.com/identity/token"
GRANITE_MODEL = "ibm/granite-3-8b-instruct"

def get_token():
    resp = requests.post(IAM_URL, data={
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": IBM_API_KEY
    })
    resp.raise_for_status()
    return resp.json()["access_token"]

def call_granite(prompt):
    token = get_token()
    url = f"{WATSONX_URL}/ml/v1/text/generation?version=2024-05-01"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    body = {
        "model_id": GRANITE_MODEL,
        "project_id": PROJECT_ID,
        "input": prompt,
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 800,
            "repetition_penalty": 1.1
        }
    }
    resp = requests.post(url, headers=headers, json=body)
    resp.raise_for_status()
    return resp.json()["results"][0]["generated_text"].strip()

SYSTEM_PROMPT = """You are an expert AI Travel Planner. Help users plan amazing trips.
Suggest destinations, create itineraries, recommend hotels and transport,
give food tips, and manage budgets. Be friendly and well-organized.
Always format itineraries with clear Day-wise plans."""

def build_prompt(history, user_msg):
    prompt = SYSTEM_PROMPT + "\n\n"
    for turn in history[-5:]:
        prompt += f"Human: {turn['user']}\nAssistant: {turn['assistant']}\n\n"
    prompt += f"Human: {user_msg}\nAssistant:"
    return prompt

st.set_page_config(page_title="AI Travel Planner", page_icon="✈️", layout="wide")
st.title("✈️ AI Travel Planner Agent")
st.caption("Powered by IBM Granite | IBM SkillsBuild AICTE 2026")

if "history" not in st.session_state:
    st.session_state["history"] = []

with st.sidebar:
    st.header("🗺️ Quick Trip Planner")
    destination = st.text_input("📍 Destination", placeholder="e.g., Goa, Paris")
    days = st.slider("📅 Number of Days", 1, 15, 5)
    budget = st.selectbox("💰 Budget", ["Low", "Medium", "High"])
    interests = st.multiselect("🎯 Interests", [
        "Beaches", "History", "Food",
        "Adventure", "Shopping", "Nature"
    ])
    if st.button("🚀 Generate Trip Plan", use_container_width=True):
        if destination:
            msg = f"Plan a {days}-day trip to {destination}. Budget: {budget}. Interests: {', '.join(interests) if interests else 'General'}."
            st.session_state["quick_msg"] = msg
        else:
            st.warning("Please enter a destination!")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state["history"] = []
        st.rerun()

for turn in st.session_state["history"]:
    with st.chat_message("user"):
        st.write(turn["user"])
    with st.chat_message("assistant"):
        st.write(turn["assistant"])

user_input = st.chat_input("Ask your travel question...")
if "quick_msg" in st.session_state:
    user_input = st.session_state.pop("quick_msg")

if user_input:
    with st.spinner("🔄 Planning your trip..."):
        try:
            prompt = build_prompt(st.session_state["history"], user_input)
            response = call_granite(prompt)
            st.session_state["history"].append({
                "user": user_input,
                "assistant": response
            })
            st.rerun()
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")