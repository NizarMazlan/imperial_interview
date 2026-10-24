import streamlit as st
import time
import random

# Page Configuration
st.set_page_config(
    page_title="Imperial Video Interview Simulator (Kira Style)",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.2rem;
        color: #002147;
        font-weight: 700;
        text-align: center;
        margin-bottom: 20px;
    }
    .timer-box {
        padding: 25px;
        border-radius: 15px;
        background-color: #002147;
        color: white;
        text-align: center;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 20px;
        box-shadow: 0px 4px 15px rgba(0, 33, 71, 0.3);
    }
    .prompt-box {
        padding: 25px;
        border-radius: 12px;
        background-color: #f1f5f9;
        border-left: 6px solid #002147;
        font-size: 1.2rem;
        color: #1e293b;
        margin-bottom: 25px;
    }
    .tip-box {
        padding: 15px;
        border-radius: 8px;
        background-color: #e2e8f0;
        font-size: 0.95rem;
        color: #334155;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State Variables
if "stage" not in st.session_state:
    st.session_state.stage = "setup" # setup, prep, recording, completed
if "selected_category" not in st.session_state:
    st.session_state.selected_category = "Motivation & Career Plans"
if "current_prompt" not in st.session_state:
    st.session_state.current_prompt = ""
if "timer_running" not in st.session_state:
    st.session_state.timer_running = False

# Question Bank based on Imperial MSc BA & AI past interviews[cite: 1, 5]
QUESTION_BANK = {
    "Motivation & Career Plans": [
        "Tell me about yourself, your career plans after graduation, and why you want to study the MSc Business Analytics & AI programme at Imperial.",
        "How do you bridge your past academic/professional background with your future aspirations in AI and Business Analytics?",
        "Why is Imperial College Business School your top choice compared to other institutions?"
    ],
    "Core Competency (STAR Behavioral)": [
        "Describe a time when you worked with incomplete, messy, or ambiguous data to solve a complex business challenge.",
        "Tell me about a situation where you had to lead a technical project or resolve a conflict within a multidisciplinary team.",
        "Describe a time you encountered a significant failure or resistance while implementing a data-driven solution and how you adapted."
    ],
    "Curveball / Unexpected": [
        "What do you think of the color red?",
        "If you could have dinner with any historical figure in data science or computing, who would it be and why?",
        "What is a piece of conventional wisdom in business or technology that you strongly disagree with?"
    ],
    "Written Assessment Prompt": [
        "Discuss how generative AI is transforming modern retail supply chains and customer personalization. (Target 60–80 concise, high-impact words).",
        "Evaluate the trade-offs between predictive model accuracy and ethical data interpretability in corporate decision-making."
    ]
}

# Sidebar Navigation & Global Reset
st.sidebar.markdown("### 🎙️ Interview Practice Studio")
st.sidebar.markdown("Simulate the exact timed pressure of **Kira Talent** used by Imperial College Business School[cite: 2].")
st.sidebar.markdown("---")

nav_mode = st.sidebar.radio(
    "Session Mode:",
    ["🚀 Practice Interview Session", "📊 Review & Past Notes"]
)

if nav_mode == "🚀 Practice Interview Session":
    st.markdown('<p class="main-header">Imperial MSc Admissions Video Interview Simulator</p>', unsafe_allow_html=True)
    
    # Global Exit/Restart Button available at any active interview stage
    if st.session_state.stage != "setup":
        if st.sidebar.button("🚪 Exit / Reset Session", type="secondary", use_container_width=True):
            st.session_state.stage = "setup"
            st.session_state.timer_running = False
            st.rerun()

    # STAGE 1: SETUP
    if st.session_state.stage == "setup":
        st.markdown("### Select Question Category")
        category = st.selectbox(
            "Choose prompt category:",
            list(QUESTION_BANK.keys())
        )
        st.session_state.selected_category = category
        
        st.markdown(f"**Category Selected:** `{category}`")
        st.info("💡 **Kira Flow Reminder:** You will get **30 seconds of prep time** followed by **1 minute of live response time** (or 5 minutes for written prompts)[cite: 2]. Use the start buttons to control when each countdown begins!")
        
        if st.button("▶️ Begin Session", type="primary", use_container_width=True):
            st.session_state.current_prompt = random.choice(QUESTION_BANK[category])
            st.session_state.stage = "prep"
            st.session_state.timer_running = False
            st.rerun()

    # STAGE 2: PREPARATION (30 Seconds)
    elif st.session_state.stage == "prep":
        st.markdown(f"### ⏳ Step 1 of 2: Preparation Window (30s)")
        st.markdown(f'<div class="prompt-box"><b>Prompt:</b> {st.session_state.current_prompt}</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown("#### Scratchpad / Outline (Punchline Method):")
            st.text_area("Jot down 2-3 key points:", placeholder="- Key point 1...\n- Key point 2...\n- Key point 3...", height=150)
            
        with col2:
            st.markdown("#### Preparation Timer Controls")
            timer_container = st.empty()
            
            if not st.session_state.timer_running:
                timer_container.markdown('<div class="timer-box">00:30</div>', unsafe_allow_html=True)
                
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    if st.button("▶️ Start Prep Countdown", type="primary", use_container_width=True):
                        st.session_state.timer_running = True
                        st.rerun()
                with col_btn2:
                    if st.button("⏩ Skip Prep & Go to Response", use_container_width=True):
                        st.session_state.stage = "recording"
                        st.session_state.timer_running = False
                        st.rerun()
            else:
                # Active Prep Countdown Loop
                for remaining in range(30, -1, -1):
                    timer_container.markdown(f'<div class="timer-box">00:{remaining:02d}</div>', unsafe_allow_html=True)
                    if remaining == 0:
                        st.session_state.stage = "recording"
                        st.session_state.timer_running = False
                        st.rerun()
                    time.sleep(1)

    # STAGE 3: RECORDING / WRITING (60s / 300s)
    elif st.session_state.stage == "recording":
        is_written = ("Written" in st.session_state.selected_category)
        rec_duration = 300 if is_written else 60
        mode_label = "WRITING TIME" if is_written else "LIVE RECORDING"
        
        st.markdown(f"### 🔴 Step 2 of 2: {mode_label}")
        st.markdown(f'<div class="prompt-box"><b>Prompt:</b> {st.session_state.current_prompt}</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if is_written:
                st.markdown("#### Type your response here:")
                written_response = st.text_area("Draft response:", height=200, placeholder="Type your response here...")
                word_count = len(written_response.split()) if written_response else 0
                st.metric("Word Count (Target: 60-80 words)", f"{word_count} words")
            else:
                st.markdown("""
                <div class="tip-box">
                <b>Webcam Simulation Active:</b><br>
                • Look directly into the <b>webcam lens</b> (not your screen)[cite: 1, 5].<br>
                • Speak clearly at 130–150 WPM[cite: 1, 5].<br>
                • Keep talking until time expires or click finish when done[cite: 5].
                </div>
                """, unsafe_allow_html=True)
                
        with col2:
            st.markdown(f"#### {mode_label} Controls")
            timer_container = st.empty()
            
            if not st.session_state.timer_running:
                mins, secs = divmod(rec_duration, 60)
                timer_container.markdown(f'<div class="timer-box">🔴 {mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)
                
                if st.button("▶️ Start Response Timer", type="primary", use_container_width=True):
                    st.session_state.timer_running = True
                    st.rerun()
            else:
                # End Button available while timer is counting down
                if st.button("⏹️ End Response & Complete", type="primary", use_container_width=True):
                    st.session_state.stage = "completed"
                    st.session_state.timer_running = False
                    st.rerun()

                # Active Countdown Loop
                for remaining in range(rec_duration, -1, -1):
                    mins, secs = divmod(remaining, 60)
                    timer_container.markdown(f'<div class="timer-box">🔴 {mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)
                    if remaining == 0:
                        st.session_state.stage = "completed"
                        st.session_state.timer_running = False
                        st.rerun()
                    time.sleep(1)

    # STAGE 4: COMPLETED SUMMARY
    elif st.session_state.stage == "completed":
        st.markdown("### ✅ Practice Simulation Complete!")
        st.markdown(f'<div class="prompt-box"><b>Completed Prompt:</b> {st.session_state.current_prompt}</div>', unsafe_allow_html=True)
        
        st.success("Great job keeping your composure and practicing under pressure!")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Practice Another Prompt", type="primary", use_container_width=True):
                st.session_state.stage = "setup"
                st.session_state.timer_running = False
                st.rerun()
        with col2:
            if st.button("🔁 Repeat Same Category", use_container_width=True):
                st.session_state.current_prompt = random.choice(QUESTION_BANK[st.session_state.selected_category])
                st.session_state.stage = "prep"
                st.session_state.timer_running = False
                st.rerun()

elif nav_mode == "📊 Review & Past Notes":
    st.markdown('<p class="main-header">📊 Interview Strategy & Frameworks Review</p>', unsafe_allow_html=True)
    st.markdown("Quick reference to keep in mind while running your simulations:")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### 🎯 The Punchline Method
        * Know your main takeaway before you start speaking[cite: 1, 5].
        * Avoid rambling; structured bullet points prevent you from cutting off mid-sentence[cite: 1, 2, 5].
        """)
        st.markdown("""
        ### 🔄 The Adaptable STAR Story
        * Keep **one** powerful technical/teamwork project ready in your mind[cite: 1, 5].
        * Adapt the Action and Result depending on the question context[cite: 1, 5].
        """)
    with col2:
        st.markdown("""
        ### 🎨 Handling Curveballs (e.g. Color Red)
        * There are **no wrong answers**[cite: 1, 5].
        * Keep smiling, maintain positive body language, and talk continuously[cite: 1, 5].
        """)
        st.markdown("""
        ### 📝 Written Prompt Rules
        * Aim for **60–80 high-impact words** to ensure clarity and check grammar[cite: 1, 5].
        """)