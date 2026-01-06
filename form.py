import streamlit as st
import base64
import os
import pandas as pd
import random

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
    # Check if name exists to prevent duplicates (optional, basic check)
    if name not in df["Name"].values:
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

# -------------------- Questions Data (Indirect & Shufflable) --------------------
# Structure: Each item is a dictionary with 'question' and a list of 'options'.
# Each option has 'text' and 'type' (DSAI, SWE, IT).
# We will shuffle the options list before displaying.

raw_questions = [
    {
        "q": "1. You are given a complex Lego set without instructions. What is your instinct?",
        "options": [
            {"text": "I categorize the pieces by size and color so I know exactly what I'm working with.", "type": "DSAI"},
            {"text": "I just start putting pieces together to see what cool shape emerges.", "type": "SWE"},
            {"text": "I look for the base plate; I need a solid foundation before I build anything.", "type": "IT"}
        ]
    },
    {
        "q": "2. If you were a chef, your signature philosophy would be:",
        "options": [
            {"text": "Precision. Every ingredient must be measured perfectly for the best result.", "type": "DSAI"},
            {"text": "Invention. I want to create a taste that has never existed before.", "type": "SWE"},
            {"text": "Consistency. A meal that is reliable, hearty, and never fails the customer.", "type": "IT"}
        ]
    },
    {
        "q": "3. You walk into a crowded party. You immediately notice:",
        "options": [
            {"text": "The hidden patterns in how people are moving and grouping.", "type": "DSAI"},
            {"text": "The vibe, the decor, and how the atmosphere was crafted.", "type": "SWE"},
            {"text": "The exits, the ventilation, and whether the music is too loud.", "type": "IT"}
        ]
    },
    {
        "q": "4. In a survival scenario, you contribute by:",
        "options": [
            {"text": "Mapping the area and calculating the best routes for resources.", "type": "DSAI"},
            {"text": "Crafting traps and tools out of random scraps we find.", "type": "SWE"},
            {"text": "Securing the perimeter and ensuring our shelter is impenetrable.", "type": "IT"}
        ]
    },
    {
        "q": "5. You enjoy a movie most when:",
        "options": [
            {"text": "You can solve the mystery before the main character does.", "type": "DSAI"},
            {"text": "The world-building is unique and visually stunning.", "type": "SWE"},
            {"text": "The plot has zero loopholes and everything makes logical sense.", "type": "IT"}
        ]
    },
    {
        "q": "6. If your brain was a desk, it would be:",
        "options": [
            {"text": "Covered in sticky notes connecting different ideas together.", "type": "DSAI"},
            {"text": "Messy, but full of half-finished sketches and prototypes.", "type": "SWE"},
            {"text": "Perfectly organized, with everything labeled and in its drawer.", "type": "IT"}
        ]
    },
    {
        "q": "7. A new gadget stops working. Your immediate reaction:",
        "options": [
            {"text": "I need to investigate *why* this specific failure happened.", "type": "DSAI"},
            {"text": "Challenge accepted. I bet I can make it do something else.", "type": "SWE"},
            {"text": "Annoyance. Things should just work reliably.", "type": "IT"}
        ]
    },
    {
        "q": "8. Which concept is most appealing to you?",
        "options": [
            {"text": "Truth (Uncovering reality)", "type": "DSAI"},
            {"text": "Creation (Bringing ideas to life)", "type": "SWE"},
            {"text": "Order (Taming chaos)", "type": "IT"}
        ]
    },
    {
        "q": "9. In a strategy game, you win by:",
        "options": [
            {"text": "Studying your opponent until you predict their next move.", "type": "DSAI"},
            {"text": "Overwhelming them with a massive army you built quickly.", "type": "SWE"},
            {"text": "Building an unbreakable defense that wears them down.", "type": "IT"}
        ]
    },
    {
        "q": "10. You see abstract art. You think:",
        "options": [
            {"text": "Is there a hidden message or code in this mess?", "type": "DSAI"},
            {"text": "I could make something cooler than this.", "type": "SWE"},
            {"text": "It needs a frame to give it some structure.", "type": "IT"}
        ]
    },
    {
        "q": "11. Ideally, you would want to be known as:",
        "options": [
            {"text": "The Genius who understood the universe.", "type": "DSAI"},
            {"text": "The Visionary who invented the future.", "type": "SWE"},
            {"text": "The Commander who kept everyone safe.", "type": "IT"}
        ]
    },
    {
        "q": "12. You are organizing books. You sort them by:",
        "options": [
            {"text": "Subject and Genre (Logical association).", "type": "DSAI"},
            {"text": "Color and Size (Aesthetic appeal).", "type": "SWE"},
            {"text": "Alphabetical Order (Fastest retrieval).", "type": "IT"}
        ]
    },
    {
        "q": "13. You catch a friend lying because:",
        "options": [
            {"text": "The probability of their story being true is statistically zero.", "type": "DSAI"},
            {"text": "You tricked them into revealing the truth.", "type": "SWE"},
            {"text": "You checked the facts and found a contradiction.", "type": "IT"}
        ]
    },
    {
        "q": "14. What scares you the most?",
        "options": [
            {"text": "Not knowing the answer.", "type": "DSAI"},
            {"text": "Never creating anything meaningful.", "type": "SWE"},
            {"text": "Being vulnerable or exposed.", "type": "IT"}
        ]
    },
    {
        "q": "15. You are lost in a forest. You:",
        "options": [
            {"text": "Analyze the sun and moss to calculate a direction.", "type": "DSAI"},
            {"text": "Start building a shelter before it gets dark.", "type": "SWE"},
            {"text": "Find high ground and signal for help securely.", "type": "IT"}
        ]
    },
    {
        "q": "16. If you were an instrument, you would be:",
        "options": [
            {"text": "A Piano – complex, mathematical, and capable of everything.", "type": "DSAI"},
            {"text": "An Electric Guitar – loud, creative, and limitless.", "type": "SWE"},
            {"text": "The Drums – the heartbeat that keeps the band together.", "type": "IT"}
        ]
    },
    {
        "q": "17. A perfect day is:",
        "options": [
            {"text": "Learning a mind-blowing new concept.", "type": "DSAI"},
            {"text": "Finishing a project you've been working on.", "type": "SWE"},
            {"text": "Having zero unexpected problems.", "type": "IT"}
        ]
    },
    {
        "q": "18. You see a 'Do Not Press' button. You:",
        "options": [
            {"text": "Wonder what the consequences are.", "type": "DSAI"},
            {"text": "Want to rewire it to do something cool.", "type": "SWE"},
            {"text": "Make sure no one else presses it.", "type": "IT"}
        ]
    },
    {
        "q": "19. In a conversation, you usually:",
        "options": [
            {"text": "Connect two seemingly unrelated topics.", "type": "DSAI"},
            {"text": "Drive the conversation to new, fun ideas.", "type": "SWE"},
            {"text": "Clarify what people mean so everyone understands.", "type": "IT"}
        ]
    },
    {
        "q": "20. When buying a car, you check:",
        "options": [
            {"text": "The specs, data, and efficiency charts.", "type": "DSAI"},
            {"text": "The customization options and features.", "type": "SWE"},
            {"text": "The safety rating and reliability warranty.", "type": "IT"}
        ]
    },
    {
        "q": "21. If you wrote a book, it would be:",
        "options": [
            {"text": "A complex mystery thriller.", "type": "DSAI"},
            {"text": "A fantasy novel with a new world.", "type": "SWE"},
            {"text": "A guide on how to survive anything.", "type": "IT"}
        ]
    },
    {
        "q": "22. Looking at the stars, you wonder:",
        "options": [
            {"text": "Is there an equation that explains all of this?", "type": "DSAI"},
            {"text": "Can we build a colony up there one day?", "type": "SWE"},
            {"text": "How can we protect Earth from asteroids?", "type": "IT"}
        ]
    },
    {
        "q": "23. Satisfaction is:",
        "options": [
            {"text": "Understanding the 'Why'.", "type": "DSAI"},
            {"text": "Seeing the 'What'.", "type": "SWE"},
            {"text": "Ensuring the 'How'.", "type": "IT"}
        ]
    },
    {
        "q": "24. Your ideal workspace is:",
        "options": [
            {"text": "Intelligent.", "type": "DSAI"},
            {"text": "Innovative.", "type": "SWE"},
            {"text": "Efficient.", "type": "IT"}
        ]
    },
    {
        "q": "25. Intelligence is:",
        "options": [
            {"text": "The ability to predict outcomes from data.", "type": "DSAI"},
            {"text": "The ability to create tools that didn't exist.", "type": "SWE"},
            {"text": "The ability to adapt and survive.", "type": "IT"}
        ]
    }
]

# -------------------- Session State & Randomization --------------------
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

# We shuffle options ONCE per session so they don't jump around on every click
if "shuffled_questions" not in st.session_state:
    # Deep copy and shuffle options
    shuffled = []
    for item in raw_questions:
        q_copy = item.copy()
        # Shuffle the list of options
        q_copy["options"] = random.sample(item["options"], len(item["options"]))
        shuffled.append(q_copy)
    st.session_state.shuffled_questions = shuffled

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

        # --- STEP 1: ASK FOR NAME & SHOW LEADERBOARD ---
        if st.session_state.user_name == "":
            st.markdown("### First, tell us who you are:")
            name_input = st.text_input("Enter your full name", placeholder="Ex: Hady Saeed")
            
            col1, col2, col3 = st.columns([1,1,1])
            with col2:
                if st.button("Start Quiz 🚀", use_container_width=True):
                    if name_input.strip() != "":
                        st.session_state.user_name = name_input
                        st.rerun()
                    else:
                        st.error("Please enter your name to proceed!")
            
            # --- LEADERBOARD AT START ---
            st.markdown("---")
            st.markdown("### 📊 Previous Responders")
            
            df = load_data()
            if not df.empty:
                # Stats
                counts = df["Major"].value_counts()
                st.bar_chart(counts, color="#64ffda")
                
                # List
                st.dataframe(
                    df[["Name", "Major"]].tail(10).iloc[::-1], # Show last 10 reversed
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.caption("Be the first to answer!")

        # --- STEP 2: SHOW QUIZ FORM (Only if Name is set) ---
        else:
            st.info(f"Welcome, **{st.session_state.user_name}**! Let's find your path.")
            
            with st.form("quiz_form"):
                # Use the SHUFFLED questions from session state
                for i, q_data in enumerate(st.session_state.shuffled_questions):
                    st.markdown(f'<div class="question-box">{q_data["q"]}</div>', unsafe_allow_html=True)
                    
                    # Extract just text for the radio button
                    option_texts = [opt["text"] for opt in q_data["options"]]
                    
                    st.radio(
                        label=f"q_{i}", 
                        options=option_texts, 
                        index=None, 
                        key=f"q_{i}", 
                        label_visibility="collapsed"
                    )
                    st.write("") 

                st.markdown("---")
                
                submitted = st.form_submit_button("✨ Reveal My Destiny ✨")
                
                if submitted:
                    answered_count = 0
                    current_questions = st.session_state.shuffled_questions
                    
                    # Check completeness
                    for i in range(len(current_questions)):
                        if st.session_state.get(f"q_{i}"):
                            answered_count += 1
                    
                    if answered_count < len(current_questions):
                        st.error(f"⚠️ You missed some questions! Please answer all {len(current_questions)}. (Answered: {answered_count})")
                    else:
                        st.session_state.submitted = True
                        st.rerun()

# 2. State: User Submitted (RESULT VIEW)
else:
    with main_placeholder.container():
        
        st.markdown(f'<div class="logo-container">{img_tag}</div>', unsafe_allow_html=True)

        # --- Calculate Result using the Hidden Type ---
        scores = {"DSAI": 0, "SWE": 0, "IT": 0}
        
        current_questions = st.session_state.shuffled_questions
        
        for i, q_data in enumerate(current_questions):
            user_answer_text = st.session_state.get(f"q_{i}")
            if user_answer_text:
                # Find which type this answer belongs to
                for opt in q_data["options"]:
                    if opt["text"] == user_answer_text:
                        scores[opt["type"]] += 1
                        break

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
            # Reshuffle for next time
            if "shuffled_questions" in st.session_state:
                del st.session_state.shuffled_questions
            for key in list(st.session_state.keys()):
                if key.startswith("q_"):
                    del st.session_state[key]
            st.rerun()