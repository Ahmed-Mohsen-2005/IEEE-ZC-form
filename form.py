import streamlit as st
import base64
import os
import pandas as pd

# -------------------- Page Config --------------------
st.set_page_config(
    page_title="CS Major Personality Quiz | IEEE ZC",
    page_icon="🔮",
    layout="centered"
)

# -------------------- Data Storage (CSV) --------------------
CSV_FILE = "quiz_results.csv"

def load_data():
    if not os.path.exists(CSV_FILE):
        return pd.DataFrame(columns=["Name", "Major", "Timestamp"])
    return pd.read_csv(CSV_FILE)

def save_data(name, major):
    df = load_data()
    new_entry = pd.DataFrame([[name, major, pd.Timestamp.now()]], columns=["Name", "Major", "Timestamp"])
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)

# -------------------- Helper to Load Local Image --------------------
def get_img_as_base64(file):
    try:
        with open(file, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return None

# Try to load the image
img_tag = ""
if os.path.exists("IEEE.jpg"):
    img_b64 = get_img_as_base64("IEEE.jpg")
    if img_b64:
        img_tag = f'<img src="data:image/jpeg;base64,{img_b64}" class="logo-img">'
else:
    img_tag = '<div style="text-align:center; font-size:40px; margin-bottom:10px;">IEEE ZC 🦅</div>'

# -------------------- 25 Deep & Witty Questions --------------------
questions = [
    ("1. You are given a complex Lego set without instructions. What is your instinct?",
     ["A) Sort all the pieces by color and size before doing anything",
      "B) Start putting pieces together to see what cool shape emerges",
      "C) Look for the base plate and build a solid foundation first"]),

    ("2. If you were a chef, your signature dish would be:",
     ["A) Molecular Gastronomy – calculated precision and chemistry",
      "B) Fusion Cuisine – inventing a new taste that didn't exist before",
      "C) The Classic Steak – perfectly cooked, reliable, and never fails"]),

    ("3. You enter a crowded party. What is the first thing you notice?",
     ["A) The flow of people and where the bottlenecks are",
      "B) The decor, the lighting, and how the vibe was created",
      "C) The exits, the ventilation, and if the music is too loud"]),

    ("4. A zombie apocalypse starts. Your role in the survival group is:",
     ["A) The Strategist: Mapping routes based on zombie density data",
      "B) The Engineer: Building traps and reinforcing the weapons",
      "C) The Sentinel: Securing the perimeter and managing radio comms"]),

    ("5. You are watching a mystery movie. You enjoy it most if:",
     ["A) You can predict the plot twist before it happens",
      "B) The visual effects and world-building are stunning",
      "C) The plot has no loopholes and everything makes logical sense"]),

    ("6. If your brain was a browser, what would it look like?",
     ["A) 50 tabs open, researching connections between random topics",
      "B) A blank canvas ready to design a new website",
      "C) Organized bookmarks, ad-blockers on, and history cleared"]),

    ("7. You buy a new gadget. It stops working. You feel:",
     ["A) Curious: I need to know *why* it failed statistically",
      "B) Challenge Accepted: I bet I can repurpose parts of it",
      "C) Annoyed: A system should be reliable and robust"]),

    ("8. Which quote resonates with your soul?",
     ["A) 'God does not play dice with the universe.' (Einstein)",
      "B) 'The best way to predict the future is to invent it.' (Alan Kay)",
      "C) 'Chaos is the enemy of order.'"]),

    ("9. You are playing a strategy game. Your playstyle is:",
     ["A) Analyze the opponent's weakness and wait for the perfect moment",
      "B) Rush to build a massive economy and overwhelm them",
      "C) Build an impenetrable defense that no one can break"]),

    ("10. You see a painting of a abstract mess. You think:",
     ["A) 'Is there a hidden pattern or message in the chaos?'",
      "B) 'I could paint something better than this.'",
      "C) 'This needs a frame to give it some structure.'"]),

    ("11. If you could time travel, you would go to:",
     ["A) The Future – to see the outcome of current trends",
      "B) The Renaissance – to help Da Vinci invent things",
      "C) The Industrial Revolution – to see how systems were standardized"]),

    ("12. You are organizing your bookshelf. You arrange books by:",
     ["A) Topic/Genre (Logical categorization)",
      "B) Color/Height (Aesthetic creation)",
      "C) Alphabetical Order (Fastest retrieval system)"]),

    ("13. Your friend tells a lie. You catch them because:",
     ["A) Their story probabilities don't add up",
      "B) You crafted a trap question that they fell into",
      "C) You checked the facts/logs and found the inconsistency"]),

    ("14. Which concept scares you more?",
     ["A) Uncertainty (Not knowing the probability of risk)",
      "B) Stagnation (Never creating anything new)",
      "C) Vulnerability (Being exposed to attack)"]),

    ("15. You are lost in a forest. You:",
     ["A) Look at the sun and moss to calculate direction",
      "B) Start building a shelter for the night",
      "C) Find a high ground and signal for help securely"]),

    ("16. If you were a musical instrument, you would be:",
     ["A) A Synthesizer – manipulating waves and frequencies",
      "B) An Electric Guitar – loud, creative, and lead-focused",
      "C) The Drums – keeping the rhythm and holding the band together"]),

    ("17. A perfect day for you is:",
     ["A) Learning a complex new theory that explains the world",
      "B) Finishing a project you’ve been working on for weeks",
      "C) Having zero unexpected problems or emergencies"]),

    ("18. You see a 'Do Not Press' button. You:",
     ["A) Wonder what the probability of an explosion is",
      "B) Want to rewire it to do something else",
      "C) Make sure to put a safety cover over it so no one presses it"]),

    ("19. In a group conversation, you are the one who:",
     ["A) Connects two seemingly unrelated topics",
      "B) Drives the conversation to a new, fun topic",
      "C) Clarifies what someone meant so everyone understands"]),

    ("20. You are buying a car. You care most about:",
     ["A) The fuel efficiency data and resale value curves",
      "B) The customization options and unique features",
      "C) The safety rating and warranty reliability"]),

    ("21. If you had to write a book, it would be:",
     ["A) A detective novel with a complex twist",
      "B) A fantasy novel with a world you built from scratch",
      "C) A survival guide on how to handle any disaster"]),

    ("22. You look at the stars. You wonder:",
     ["A) Is there a mathematical equation for the universe?",
      "B) Can we build a colony up there one day?",
      "C) How can we protect Earth from asteroids?"]),

    ("23. When solving a puzzle, you feel satisfied when:",
     ["A) You understand the trick behind it",
      "B) You finish it and see the final picture",
      "C) All the pieces fit perfectly without forcing them"]),

    ("24. Which word describes your ideal work environment?",
     ["A) Intelligent",
      "B) Innovative",
      "C) Efficient"]),

    ("25. Final Question: What is the meaning of 'Intelligence' to you?",
     ["A) The ability to learn from data and predict outcomes",
      "B) The ability to create tools that didn't exist before",
      "C) The ability to adapt and survive in any system"])
]

scores_map = {"A": "DSAI", "B": "SWE", "C": "IT"}

# -------------------- Init Session State --------------------
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

# -------------------- Global Styling --------------------
st.markdown("""
<style>
    /* --- Main Background --- */
    .stApp {
        background: radial-gradient(circle at 50% 10%, #0a192f 0%, #020c1b 100%);
        color: #ccd6f6;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* --- Sticky Header --- */
    .sticky-header-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 60px;
        background: rgba(2, 12, 27, 0.95);
        backdrop-filter: blur(10px);
        z-index: 999999;
        border-bottom: 1px solid rgba(100, 255, 218, 0.2);
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }
    
    .header-text {
        color: #64ffda;
        font-weight: bold;
        font-size: 1.2rem;
        letter-spacing: 1px;
    }

    .block-container {
        padding-top: 80px !important;
    }

    /* --- Typography --- */
    h1, h2, h3 {
        color: #64ffda !important;
        text-shadow: 0 0 10px rgba(100, 255, 218, 0.3);
    }
    
    /* --- Logo Animation --- */
    .logo-container {
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }
    .logo-img {
        width: 160px;
        border-radius: 50%;
        animation: float 4s ease-in-out infinite;
        box-shadow: 0 0 20px rgba(100, 255, 218, 0.2);
    }
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }

    /* --- Question Box Styling --- */
    .question-box {
        background: rgba(17, 34, 64, 0.6);
        border-left: 4px solid #64ffda;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 15px;
        font-size: 1.1rem;
        font-weight: bold;
        color: #e6f1ff;
    }

    /* --- Input Field --- */
    .stTextInput input {
        background-color: rgba(17, 34, 64, 0.8);
        color: #64ffda;
        border: 1px solid #64ffda;
        border-radius: 8px;
        text-align: center;
        font-size: 1.2rem;
    }
    .stTextInput label {
        color: #ccd6f6 !important;
        font-size: 1.2rem;
        text-align: center;
        width: 100%;
    }

    /* --- Radio Buttons --- */
    .stRadio div[role="radiogroup"] > label {
        background: rgba(255,255,255,0.03);
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 8px;
        border: 1px solid transparent;
        transition: all 0.2s;
        cursor: pointer;
    }
    .stRadio div[role="radiogroup"] > label:hover {
        background: rgba(100, 255, 218, 0.1);
        border-color: #64ffda;
        color: #64ffda !important;
    }

    /* --- Buttons --- */
    div[data-testid="stFormSubmitButton"] button {
        background: transparent;
        color: #64ffda !important;
        border: 2px solid #64ffda;
        border-radius: 8px;
        padding: 10px 30px;
        font-weight: bold;
        transition: 0.3s;
        width: 100%;
    }
    div[data-testid="stFormSubmitButton"] button:hover {
        background: rgba(100, 255, 218, 0.1);
        box-shadow: 0 0 15px rgba(100, 255, 218, 0.3);
        transform: scale(1.02);
    }
    
    .stButton button {
        border-radius: 8px;
        font-weight: bold;
    }

    /* --- Result & Leaderboard Styling --- */
    .winner-title {
        font-size: 3rem;
        font-weight: 800;
        color: #64ffda;
        text-align: center;
        margin-bottom: 10px;
    }
    .winner-desc {
        font-size: 1.2rem;
        color: #8892b0;
        max-width: 600px;
        margin: 0 auto;
        text-align: center;
    }
    .leaderboard-card {
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(100, 255, 218, 0.2);
        border-radius: 10px;
        padding: 20px;
        margin-top: 30px;
    }
    .link-btn {
        display: block;
        width: fit-content;
        margin: 20px auto;
        background: #64ffda;
        color: #0a192f !important;
        padding: 12px 30px;
        border-radius: 5px;
        text-decoration: none;
        font-weight: bold;
        transition: 0.3s;
        text-align: center;
    }
    .link-btn:hover {
        transform: scale(1.05);
        box-shadow: 0 0 20px rgba(100, 255, 218, 0.5);
    }

    #MainMenu, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# -------------------- Sticky Header --------------------
if not st.session_state.submitted:
    st.markdown("""
    <div class="sticky-header-container">
        <div class="header-text">IEEE ZC &nbsp;|&nbsp; CS MAJOR QUIZ</div>
    </div>
    """, unsafe_allow_html=True)

# -------------------- Main Content --------------------
main_placeholder = st.empty()

# 1. State: User Has NOT Submitted
if not st.session_state.submitted:
    with main_placeholder.container():
        st.markdown(f'<div class="logo-container">{img_tag}</div>', unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center;'>Which CS Major Are You?</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #8892b0; margin-bottom: 30px;'>🕵️‍♂️ Detective? 👷 Builder? or 🛡️ Guardian?</p>", unsafe_allow_html=True)

        # --- STEP 1: ASK FOR NAME ---
        if st.session_state.user_name == "":
            st.markdown("### First, tell us who you are:")
            name_input = st.text_input("Enter your full name", placeholder="Ex: Hady Saeed")
            
            if st.button("Start Quiz 🚀"):
                if name_input.strip() != "":
                    st.session_state.user_name = name_input
                    st.rerun()
                else:
                    st.error("Please enter your name to proceed!")
        
        # --- STEP 2: SHOW QUIZ FORM (Only if Name is set) ---
        else:
            st.info(f"Welcome, **{st.session_state.user_name}**! Let's find your path.")
            
            with st.form("quiz_form"):
                for i, (q, options) in enumerate(questions):
                    st.markdown(f'<div class="question-box">{q}</div>', unsafe_allow_html=True)
                    
                    st.radio(
                        label=f"q_{i}", 
                        options=options, 
                        index=None, 
                        key=f"q_{i}", 
                        label_visibility="collapsed"
                    )
                    st.write("") 

                st.markdown("---")
                
                submitted = st.form_submit_button("✨ Reveal My Destiny ✨")
                
                if submitted:
                    answered_count = 0
                    for i in range(len(questions)):
                        if st.session_state.get(f"q_{i}"):
                            answered_count += 1
                    
                    if answered_count < len(questions):
                        st.error(f"⚠️ You missed some questions! Please answer all {len(questions)}. (Answered: {answered_count})")
                    else:
                        st.session_state.submitted = True
                        st.rerun()

# 2. State: User Submitted (RESULT VIEW)
else:
    with main_placeholder.container():
        
        st.markdown(f'<div class="logo-container">{img_tag}</div>', unsafe_allow_html=True)

        # --- Calculate Result ---
        scores = {"DSAI": 0, "SWE": 0, "IT": 0}
        for i in range(len(questions)):
            answer = st.session_state.get(f"q_{i}")
            if answer:
                choice_letter = answer.split(")")[0].strip()
                if choice_letter in scores_map:
                    scores[scores_map[choice_letter]] += 1

        max_score = max(scores.values())
        top_matches = [k for k, v in scores.items() if v == max_score]
        winner = top_matches[0]
        
        # --- Save to CSV (Only once per session) ---
        if "saved" not in st.session_state:
            save_data(st.session_state.user_name, winner)
            st.session_state.saved = True

        # --- Display Result ---
        st.markdown('<div class="result-text">', unsafe_allow_html=True)
        
        if winner == "DSAI":
            st.markdown('<div class="winner-title">🧠 DSAI</div>', unsafe_allow_html=True)
            st.markdown(f"### {st.session_state.user_name}, You are a Data Scientist!")
            st.markdown("""
            <div class="winner-desc">
            You are the <b>Analyst</b>. <br>
            You see the hidden threads that connect the world. While others see chaos, you see probability, patterns, and predictions.<br>
            <i>"The numbers don't lie."</i>
            </div>
            """, unsafe_allow_html=True)

        elif winner == "SWE":
            st.markdown('<div class="winner-title">🛠 SWE</div>', unsafe_allow_html=True)
            st.markdown(f"### {st.session_state.user_name}, You are a Software Engineer!")
            st.markdown("""
            <div class="winner-desc">
            You are the <b>Creator</b>. <br>
            You have the urge to build things that didn't exist before. You look at a problem and immediately think of a tool to fix it.<br>
            <i>"If you can dream it, I can build it."</i>
            </div>
            """, unsafe_allow_html=True)

        elif winner == "IT":
            st.markdown('<div class="winner-title">🛡️ IT</div>', unsafe_allow_html=True)
            st.markdown(f"### {st.session_state.user_name}, You are an IT Specialist!")
            st.markdown("""
            <div class="winner-desc">
            You are the <b>Architect</b>. <br>
            You value stability, security, and efficiency. You are the backbone that keeps the digital world from collapsing.<br>
            <i>"Order out of chaos."</i>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)

        # --- LIVE LEADERBOARD ---
        st.markdown("---")
        st.markdown("## 📊 Live Major Leaderboard")
        
        df = load_data()
        if not df.empty:
            # 1. Stats Chart
            counts = df["Major"].value_counts()
            st.bar_chart(counts, color="#64ffda")
            
            # 2. Recent Responders List
            st.markdown("### 🏆 Recent Responders")
            
            # Styling the dataframe to look 'techy'
            st.dataframe(
                df[["Name", "Major"]].tail(10).iloc[::-1], # Show last 10 reversed
                use_container_width=True,
                hide_index=True
            )
        else:
            st.write("Waiting for data...")

        st.markdown("""
            <br>
            <a href="https://forms.gle/CEu2jWTkhaXwc5dMA" target="_blank" class="link-btn">
                📝 Sign Up For Your Major Introduction Session Here
            </a>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 Play Again", use_container_width=True):
            # Reset state
            st.session_state.submitted = False
            st.session_state.user_name = ""
            if "saved" in st.session_state:
                del st.session_state.saved
            for key in list(st.session_state.keys()):
                if key.startswith("q_"):
                    del st.session_state[key]
            st.rerun()