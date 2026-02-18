import streamlit as st
import pandas as pd
import joblib
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import base64

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="Smart Accident Risk Dashboard",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===============================
# STYLE & THEME (ROCKER STYLE)
# ===============================
st.markdown("""
<style>
/* Global Styles */
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

.stApp {
    background: linear-gradient(135deg, #410500 0%, #6b0000 25%, #9d0000 50%, #cf1100 75%, #fa3200 100%);
    color: #f5f5f5;
    font-family: 'Roboto', sans-serif;
    min-height: 100vh;
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #410500 0%, #6b0000 100%);
    border-right: 2px solid #fa3200;
    padding-top: 2rem;
}

.sidebar-logo {
    font-size: 1.8rem;
    font-weight: 800;
    color: white;
    margin-bottom: 2rem;
    padding-left: 1.5rem;
    display: flex;
    align-items: center;
    gap: 10px;
}

/* Header Styling */
.rocker-header {
    background: linear-gradient(90deg, #fa3200 0%, #cf1100 50%, #410500 100%);
    padding: 1rem 2rem;
    border-bottom: 2px solid #fa3200;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(250, 50, 0, 0.5), 0 2px 8px rgba(65, 5, 0, 0.3);
}

.search-container {
    background: linear-gradient(90deg, #fff3b2, #ffe995);
    border-radius: 20px;
    padding: 0.5rem 1.5rem;
    border: 2px solid #fa3200;
    width: 300px;
    color: #410500;
    font-weight: 600;
}

/* Card Panels */
.rocker-card {
    background: linear-gradient(135deg, rgba(65, 5, 0, 0.8) 0%, rgba(157, 0, 0, 0.9) 100%);
    border: 2px solid #fa3200;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    transition: transform 0.2s, box-shadow 0.3s;
}

.rocker-card:hover {
    border-color: #fa3200;
    box-shadow: 0 6px 25px rgba(250, 50, 0, 0.6), 0 0 15px rgba(207, 17, 0, 0.4);
    transform: translateY(-2px);
}

.card-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: #fff3b2;
    margin-bottom: 1.5rem;
    display: flex;
    justify-content: space-between;
    text-shadow: 0 2px 4px rgba(89, 0, 0, 0.5);
}

/* Metric Cards */
.metric-card {
    background: linear-gradient(135deg, #410500 0%, #9d0000 100%);
    border-radius: 12px;
    padding: 1.5rem;
    border-bottom: 4px solid #fa3200;
    border-left: 2px solid #cf1100;
    border-top: 1px solid #fa3200;
    box-shadow: 0 4px 12px rgba(250, 50, 0, 0.4), inset 0 1px 0 rgba(255, 241, 178, 0.1);
}

.metric-value {
    font-size: 2rem;
    font-weight: 700;
    color: white;
}

.metric-label {
    font-size: 0.9rem;
    color: #e8dcc8;
}

/* Streamlit Overrides */
.stButton>button {
    background: linear-gradient(90deg, #fa3200, #cf1100, #9d0000, #6b0000) !important;
    color: #fff3b2 !important;
    border: none !important;
    border-radius: 8px !important;
    width: 100%;
    box-shadow: 0 4px 15px rgba(250, 50, 0, 0.6);
    transition: all 0.3s;
    font-weight: bold;
}

.stButton>button:hover {
    box-shadow: 0 6px 20px rgba(250, 50, 0, 0.8) !important;
    transform: translateY(-2px);
}

.stSlider label, .stSelectbox label, [data-testid="stMarkdownContainer"] p, [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
    color: #fff3b2 !important;
}

/* Slider Styling */
.stSlider > div > div > div {
    background: linear-gradient(90deg, #cf1100, #fa3200) !important;
}

/* Selectbox Styling */
.stSelectbox > div > div {
    border: 2px solid #fa3200 !important;
    background: linear-gradient(135deg, #6b0000, #9d0000) !important;
    color: #fff3b2 !important;
}

[data-testid="stSidebar"] section[data-testid="stSidebarNav"] span {
    color: white !important;
}

/* Floating Bot Icon */
.floating-bot-container {
    position: fixed;
    bottom: 30px;
    right: 30px;
    z-index: 1000;
}

.bot-btn {
    background: linear-gradient(135deg, #fa3200, #9d0000); /* Deep Red Gradient */
    width: 65px;
    height: 65px;
    border-radius: 50%;
    border: 2px solid #fa3200;
    color: #fff3b2;
    font-size: 1.5rem;
    box-shadow: 0 5px 15px rgba(250, 50, 0, 0.7);
    cursor: pointer;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    transition: all 0.3s;
    font-weight: bold;
}

.bot-btn:hover {
    transform: scale(1.1) translateY(-2px);
}

.bot-name {
    font-size: 0.6rem;
    font-weight: bold;
    margin-top: -2px;
}

/* Chat Sidebar Right */
.chat-tab {
    background: linear-gradient(180deg, #6b0000 0%, #410500 100%);
    border-left: 2px solid #fa3200;
    height: 100vh;
    padding: 1.5rem;
}

/* Assistant Messages */
[data-testid="chatAvatarIcon-assistant"] {
    border: 2px solid #fa3200;
    background: linear-gradient(135deg, #9d0000, #cf1100) !important;
}

.stChatMessage {
    border-left: 3px solid #fa3200;
    border-radius: 12px;
    padding: 0.8rem;
    margin: 0.5rem 0;
    background: linear-gradient(90deg, rgba(255, 241, 178, 0.08), rgba(250, 50, 0, 0.1));
    border-top: 1px solid #cf1100;
}

</style>
""", unsafe_allow_html=True)

# Helper for Chart Colors
CHART_DARK = "#000000"
ACCENT_BLUE = "#ff0000"
ACCENT_RED = "#cc0000"
ACCENT_GREEN = "#ff3333"

# ===============================
# SESSION STATE
# ===============================
if "prediction" not in st.session_state:
    st.session_state.prediction = None
if "chat_msgs" not in st.session_state:
    st.session_state.chat_msgs = []
if "chat_open" not in st.session_state:
    st.session_state.chat_open = False

# ===============================
# LOAD MODEL
# ===============================
@st.cache_resource
def load_artifacts():
    try:
        model = joblib.load("xgb_model.pkl")
        encoders = joblib.load("encoders.pkl")
        target_encoder = joblib.load("target_encoder.pkl")
        return model, encoders, target_encoder
    except:
        return None, None, None

model, encoders, target_encoder = load_artifacts()

if not model:
    st.error("❌ Model files not found. Please train the model first.")
    st.stop()

# ===============================
# OLLAMA CONFIG
# ===============================
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:1b"

def get_ai_summary(question, context):
    prompt = f"""
You are a Traffic Accident Risk Expert.

Prediction Context:
{context}

User Question:
{question}

Explain clearly and simply why this risk level occurred and what factors are dangerous.
"""
    payload = {"model": MODEL_NAME, "prompt": prompt, "stream": False}

    try:
        res = requests.post(OLLAMA_URL, json=payload, timeout=60)
        return res.json().get("response", "No response.")
    except:
        return "⚠️ Ollama is not running."

# ===============================
# SIDEBAR: INPUTS
# ===============================
with st.sidebar:
    st.markdown('<div class="sidebar-logo">🚦 Risk Prediction</div>', unsafe_allow_html=True)
    
    st.markdown("### 📝 Conditions")
    speed = st.slider("🚗 Speed (mph)", 0, 120, 60)
    vehicle_age = st.slider("🚙 Vehicle Age", 0, 30, 5)
    
    st.markdown("---")
    wind = st.slider("💨 Wind (km/h)", 0, 100, 10)
    rain = st.slider("🌧️ Rain (mm)", 0.0, 50.0, 0.0)
    humidity = st.slider("💧 Humidity (%)", 0, 100, 50)
    
    st.markdown("---")
    weather = st.selectbox("☁️ Weather", encoders['Weather_Condition'].classes_)
    surface = st.selectbox("🛣️ Surface", encoders['Road_Surface'].classes_)
    lighting = st.selectbox("💡 Lighting", encoders['Lighting_Condition'].classes_)
    traffic = st.selectbox("🚦 Traffic", encoders['Traffic_Density'].classes_)

    st.write("")
    predict_btn = st.button("PREDICT RISK", type="primary")

    if predict_btn:
        input_dict = {
            'Speed_Limit': speed, 'Vehicle_Age_Years': vehicle_age,
            'WindSpeed_kmh': wind, 'Rainfall_mm': rain, 'Humidity_%': humidity,
            'Weather_Condition': weather, 'Road_Surface': surface,
            'Lighting_Condition': lighting, 'Traffic_Density': traffic
        }

        # Preprocess
        feature_names = model.get_booster().feature_names
        input_df = pd.DataFrame(columns=feature_names)
        input_df.loc[0] = 0

        for col, val in input_dict.items():
            if col in encoders:
                input_df[col] = encoders[col].transform([val])[0]
            else:
                input_df[col] = val

        # Predict
        pred_idx = model.predict(input_df)[0]
        probs = model.predict_proba(input_df)[0]
        label = target_encoder.inverse_transform([pred_idx])[0]

        st.session_state.prediction = {
            "label": label,
            "probs": probs,
            "probs_dict": {c: p for c, p in zip(target_encoder.classes_, probs)},
            "input": input_dict
        }
        st.session_state.chat_msgs = [{"role": "assistant", "content": f"Prediction Complete. Risk: **{label}**."}]

# ===============================
# MAIN LAYOUT
# ===============================

# 1. Custom CSS for Floating Bot Button
st.markdown("""
<style>
div[data-testid="stVerticalBlock"] > div:has(button[key="toggle_chat"]) {
    position: fixed;
    bottom: 30px;
    right: 30px;
    z-index: 9999;
    text-align: center;
}
button[key="toggle_chat"] {
    width: 120px !important;
    height: 50px !important;
    border-radius: 25px !important;
    background: linear-gradient(135deg, #fa3200, #cf1100, #410500) !important; /* Deep Red Gradient */
    box-shadow: 0 4px 15px rgba(250, 50, 0, 0.7) !important;
    font-size: 16px !important;
    font-weight: bold !important;
    color: #fff3b2 !important;
    border: 2px solid #fa3200 !important;
    transition: all 0.3s !important;
}
</style>
""", unsafe_allow_html=True)

# Toggle Button
if st.button("🤖 AI Bot", key="toggle_chat"):
    st.session_state.chat_open = not st.session_state.chat_open
    st.rerun()

# 2. Layout Distribution
if st.session_state.chat_open:
    col_main, col_chat = st.columns([3, 1], gap="medium")
else:
    col_main = st.container()

with col_main:
    # Top Header Bar
    st.markdown("""
    <div class="rocker-header">
        <div class="search-container">🔍 Type to search...</div>
        <div style="display:flex; align-items:center; gap:20px;">
            <span>🇺🇸 EN</span>
            <span>🔔</span>
            <span>👤 Kazim Haider Syed</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.prediction:
        pred = st.session_state.prediction
        
        # Charts Row
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="rocker-card"><div class="card-title">Risk Overview</div>', unsafe_allow_html=True)
            prob_df = pd.DataFrame({"Risk": list(pred['probs_dict'].keys()), "Prob": list(pred['probs_dict'].values())})
            fig, ax = plt.subplots(figsize=(6, 4))
            fig.patch.set_facecolor(CHART_DARK)
            ax.set_facecolor(CHART_DARK)
            x = range(len(prob_df))
            ax.plot(x, prob_df['Prob'], color=ACCENT_BLUE, linewidth=3)
            ax.fill_between(x, prob_df['Prob'], alpha=0.3, color=ACCENT_BLUE)
            ax.set_xticks(x)
            ax.set_xticklabels(prob_df['Risk'], color='#ffffff')
            ax.tick_params(colors='#ffffff')
            ax.spines['bottom'].set_color('#ff0000')
            ax.spines['left'].set_color('#ff0000')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            st.pyplot(fig)
            st.markdown('</div>', unsafe_allow_html=True)

        with c2:
            st.markdown('<div class="rocker-card"><div class="card-title">Impact Factor</div>', unsafe_allow_html=True)
            factors = ['Speed', 'Rain', 'Wind', 'Traffic']
            traffic_map = {'Low': 0.3, 'Medium': 0.6, 'High': 0.9}
            traffic_val = traffic_map.get(pred['input']['Traffic_Density'], 0.5)
            vals = [pred['input']['Speed_Limit']/120, pred['input']['Rainfall_mm']/50, pred['input']['WindSpeed_kmh']/100, traffic_val]
            fig2, ax2 = plt.subplots(figsize=(6, 4))
            fig2.patch.set_facecolor(CHART_DARK)
            ax2.set_facecolor(CHART_DARK)
            ax2.bar(factors, vals, color=ACCENT_RED, alpha=0.9)
            ax2.tick_params(colors='#ffffff')
            ax2.spines['bottom'].set_color('#ff0000')
            ax2.spines['left'].set_color('#ff0000')
            ax2.spines['top'].set_visible(False)
            ax2.spines['right'].set_visible(False)
            st.pyplot(fig2)
            st.markdown('</div>', unsafe_allow_html=True)

        # Metrics Row
        m1, m2, m3, m4 = st.columns(4)
        risk_color = ACCENT_RED if pred['label'] == 'High' else ACCENT_GREEN
        m1.markdown(f"""<div class="metric-card"><div class="metric-label">CURRENT RISK</div>
                    <div class="metric-value" style="color:{risk_color}">{pred['label']}</div></div>""", unsafe_allow_html=True)
        m2.markdown(f"""<div class="metric-card" style="border-color:#d4a574"><div class="metric-label">CONFIDENCE</div>
                    <div class="metric-value">{pred['probs_dict'][pred['label']]:.1%}</div></div>""", unsafe_allow_html=True)
        m3.markdown(f"""<div class="metric-card" style="border-color:#c9a87e"><div class="metric-label">WEATHER</div>
                    <div class="metric-value">{pred['input']['Weather_Condition']}</div></div>""", unsafe_allow_html=True)
        m4.markdown(f"""<div class="metric-card" style="border-color:#b8986b"><div class="metric-label">AVG SPEED</div>
                    <div class="metric-value">{pred['input']['Speed_Limit']}mph</div></div>""", unsafe_allow_html=True)
    else:
        st.info("👈 Use the sidebar to set accident conditions and generate the Risk Report.")

# 3. Chat Area (Right Side)
if st.session_state.chat_open:
    with col_chat:
        st.markdown('<h3 style="color:white; margin-bottom:1rem;">🤖 AI Assistant</h3>', unsafe_allow_html=True)
        
        # Scrollable area for messages
        chat_container = st.container(height=600)
        with chat_container:
            for msg in st.session_state.chat_msgs:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])
        
        prompt = st.chat_input("Ask a question...")
        if prompt:
            # 1. Add and show user message immediately
            st.session_state.chat_msgs.append({"role": "user", "content": prompt})
            with chat_container:
                with st.chat_message("user"):
                    st.markdown(prompt)
            
            # 2. Show thinking spinner
            with chat_container:
                with st.chat_message("assistant"):
                    with st.spinner("Analyzing risk factors..."):
                        ctx = f"Risk: {st.session_state.prediction['label'] if st.session_state.prediction else 'None'}"
                        response = get_ai_summary(prompt, ctx)
                        st.markdown(response)
            
            # 3. Save to state and refresh
            st.session_state.chat_msgs.append({"role": "assistant", "content": response})
            st.rerun()
