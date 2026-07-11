import requests
import streamlit as st

# ─────────────────────────────────────────────
# IBM / HuggingFace Configuration
# ─────────────────────────────────────────────
import os
HF_TOKEN = os.environ.get("HF_TOKEN", "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")

# ─────────────────────────────────────────────
# Page Configuration
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="✈️ AI Travel Planner Agent",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# Custom CSS - Professional Mixed Theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Playfair+Display:wght@700&display=swap');

    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        font-family: 'Poppins', sans-serif;
    }

    /* Hero Header */
    .hero-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 30%, #f093fb 60%, #f5a623 100%);
        padding: 40px 30px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
    }

    .hero-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 60%);
        animation: shimmer 3s infinite;
    }

    @keyframes shimmer {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    .hero-title {
        font-family: 'Playfair Display', serif;
        font-size: 3em;
        color: white;
        margin: 0;
        text-shadow: 2px 4px 8px rgba(0,0,0,0.3);
        letter-spacing: 2px;
    }

    .hero-subtitle {
        font-size: 1em;
        color: rgba(255,255,255,0.9);
        margin: 10px 0 0 0;
        letter-spacing: 3px;
        text-transform: uppercase;
        font-weight: 300;
    }

    .hero-badges {
        margin-top: 15px;
        display: flex;
        justify-content: center;
        gap: 10px;
        flex-wrap: wrap;
    }

    .badge {
        background: rgba(255,255,255,0.2);
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 0.75em;
        border: 1px solid rgba(255,255,255,0.3);
        backdrop-filter: blur(10px);
    }

    /* Stats Bar */
    .stats-bar {
        display: flex;
        justify-content: space-around;
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 20px;
        backdrop-filter: blur(10px);
    }

    .stat-item {
        text-align: center;
        color: white;
    }

    .stat-number {
        font-size: 1.8em;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea, #f5a623);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .stat-label {
        font-size: 0.7em;
        color: rgba(255,255,255,0.6);
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Chat Messages */
    .user-msg {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 15px 20px;
        border-radius: 20px 20px 5px 20px;
        margin: 10px 0;
        max-width: 80%;
        margin-left: auto;
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.3);
        font-size: 0.95em;
        line-height: 1.6;
    }

    .agent-msg {
        background: rgba(255,255,255,0.07);
        color: white;
        padding: 15px 20px;
        border-radius: 20px 20px 20px 5px;
        margin: 10px 0;
        max-width: 85%;
        border-left: 4px solid #f5a623;
        box-shadow: 0 5px 20px rgba(0,0,0,0.2);
        font-size: 0.95em;
        line-height: 1.8;
        backdrop-filter: blur(10px);
    }

    .msg-label-user {
        font-size: 0.7em;
        color: rgba(255,255,255,0.6);
        text-align: right;
        margin-bottom: 5px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .msg-label-agent {
        font-size: 0.7em;
        color: #f5a623;
        margin-bottom: 5px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Sidebar */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%) !important;
        border-right: 1px solid rgba(255,255,255,0.1);
    }

    [data-testid="stSidebar"] * {
        color: white !important;
    }

    .sidebar-header {
        background: linear-gradient(135deg, #667eea, #f5a623);
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 20px;
        font-weight: 600;
        font-size: 1.1em;
        color: white;
        letter-spacing: 1px;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 20px !important;
        font-weight: 600 !important;
        letter-spacing: 1px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3) !important;
        font-family: 'Poppins', sans-serif !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5) !important;
    }

    /* Input */
    .stChatInput > div {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 15px !important;
        color: white !important;
    }

    /* Welcome Card */
    .welcome-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 20px;
        padding: 40px;
        text-align: center;
        color: white;
        backdrop-filter: blur(10px);
    }

    .welcome-emoji {
        font-size: 4em;
        margin-bottom: 15px;
    }

    .welcome-title {
        font-size: 1.5em;
        font-weight: 600;
        margin-bottom: 10px;
        background: linear-gradient(135deg, #667eea, #f5a623);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .welcome-text {
        color: rgba(255,255,255,0.6);
        font-size: 0.9em;
        line-height: 1.8;
    }

    .suggestion-chips {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        justify-content: center;
        margin-top: 20px;
    }

    .chip {
        background: rgba(102, 126, 234, 0.2);
        border: 1px solid rgba(102, 126, 234, 0.4);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 0.8em;
        cursor: pointer;
    }

    /* Selectbox & Slider */
    .stSelectbox > div, .stMultiSelect > div {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 10px !important;
        color: white !important;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# AI Model Setup
# ─────────────────────────────────────────────
from huggingface_hub import InferenceClient

client = InferenceClient(api_key=HF_TOKEN)

SYSTEM_PROMPT = """You are an expert AI Travel Planner for Indian travellers.
Help users plan amazing trips within India and abroad.
Suggest destinations, create itineraries, recommend hotels and transport,
give food tips, and manage budgets in Indian Rupees (₹).
Be friendly, enthusiastic and well-organized.
Always format itineraries with clear Day-wise plans.
Use emojis to make responses more engaging."""

def travel_agent(user_message, history):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for turn in history[-5:]:
        messages.append({"role": "user", "content": turn["user"]})
        messages.append({"role": "assistant", "content": turn["assistant"]})
    messages.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model="mistralai/Mistral-7B-Instruct-v0.3",
        messages=messages,
        max_tokens=1000
    )
    return response.choices[0].message.content

# ─────────────────────────────────────────────
# Hero Header
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
    <p class="hero-title">✈️ AI Travel Planner</p>
    <p class="hero-subtitle">Your Intelligent Travel Companion</p>
    <div class="hero-badges">
        <span class="badge">🤖 IBM Granite Powered</span>
        <span class="badge">🌍 IBM SkillsBuild AICTE 2026</span>
        <span class="badge">⚡ Real-time AI Planning</span>
        <span class="badge">🏆 EduNet Foundation</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Stats Bar
# ─────────────────────────────────────────────
st.markdown("""
<div class="stats-bar">
    <div class="stat-item">
        <div class="stat-number">500+</div>
        <div class="stat-label">Destinations</div>
    </div>
    <div class="stat-item">
        <div class="stat-number">24/7</div>
        <div class="stat-label">AI Support</div>
    </div>
    <div class="stat-item">
        <div class="stat-number">100%</div>
        <div class="stat-label">Personalized</div>
    </div>
    <div class="stat-item">
        <div class="stat-number">Free</div>
        <div class="stat-label">Forever</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Session State
# ─────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state["history"] = []

# ─────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-header">🗺️ Quick Trip Planner</div>', unsafe_allow_html=True)

    destination = st.text_input("📍 Where to?", placeholder="e.g., Goa, Manali, Paris")
    days = st.slider("📅 Trip Duration (Days)", 1, 15, 5)
    budget = st.selectbox("💰 Budget", ["Budget (₹5,000-15,000)", "Mid-Range (₹15,000-40,000)", "Luxury (₹40,000+)"])
    interests = st.multiselect("🎯 Your Interests", [
        "🏖️ Beaches", "🏔️ Mountains", "🏛️ History & Culture",
        "🍜 Food & Cuisine", "🛍️ Shopping", "🌿 Nature & Wildlife",
        "🕌 Religious Sites", "🎭 Nightlife", "👨‍👩‍👧 Family Activities",
        "🏄 Adventure Sports"
    ])

    if st.button("🚀 Generate My Trip Plan!", use_container_width=True):
        if destination:
            interest_str = ", ".join(interests) if interests else "general sightseeing"
            msg = f"Plan a complete {days}-day trip to {destination}. Budget: {budget}. Interests: {interest_str}. Include day-wise itinerary, hotel recommendations, transport options, food spots, and budget breakdown in Indian Rupees (₹)."
            st.session_state["quick_msg"] = msg
        else:
            st.warning("Please enter a destination!")

    st.markdown("---")

    st.markdown("**💡 Try asking:**")
    suggestions = [
        "Best places in Rajasthan?",
        "Budget trip to Kerala?",
        "What to pack for Manali?",
        "Best time to visit Goa?",
        "5 days in Ladakh plan?"
    ]
    for s in suggestions:
        if st.button(f"💬 {s}", use_container_width=True, key=s):
            st.session_state["quick_msg"] = s

    st.markdown("---")

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state["history"] = []
        st.rerun()

    st.markdown("""
    <div style='text-align:center; color:rgba(255,255,255,0.4); font-size:0.7em; margin-top:20px;'>
        Powered by IBM Granite<br>IBM SkillsBuild AICTE 2026<br>
        Built by Sandesh Padwal
    </div>
    """, unsafe_allow_html=True)

if not st.session_state["history"]:
    st.markdown("""
    <div class="welcome-card">
        <div class="welcome-emoji">🌍</div>
        <div class="welcome-title">Welcome, Traveller!</div>
        <div class="welcome-text">
            I'm your AI-powered travel companion, ready to help you plan<br>
            the perfect trip anywhere in the world!<br><br>
            Ask me about destinations, itineraries, budgets, hotels,<br>
            local food, packing tips, and much more!
        </div>
        <div class="suggestion-chips">
            <span class="chip">🏖️ Plan a Goa trip</span>
            <span class="chip">🏔️ Best hill stations</span>
            <span class="chip">✈️ International travel tips</span>
            <span class="chip">💰 Budget travel India</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    for turn in st.session_state["history"]:
        st.markdown(f"""
        <div class="msg-label-user">You 👤</div>
        <div class="user-msg">{turn["user"]}</div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div class="msg-label-agent">✈️ Travel Agent</div>
        <div class="agent-msg">{turn["assistant"]}</div>
        """, unsafe_allow_html=True)

user_input = st.chat_input("✈️ Ask your travel question...")

if "quick_msg" in st.session_state:
    user_input = st.session_state.pop("quick_msg")

if user_input:
    with st.spinner("🌍 Planning your perfect trip..."):
        try:
            response = travel_agent(user_input, st.session_state["history"])
            st.session_state["history"].append({
                "user": user_input,
                "assistant": response
            })
            st.rerun()
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
