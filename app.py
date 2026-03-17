import streamlit as st
import streamlit.components.v1 as components
import math
import random

# --- 1. RAGA DATABASE ---
ragas_db = {
    "Yaman": {"aaroh": ["S", "R", "G", "M", "P", "D", "N"], "avroh": ["S", "N", "D", "P", "M", "G", "R"]},
    "Bhairavi": {"aaroh": ["S", "r", "g", "m", "P", "d", "n"], "avroh": ["S", "n", "d", "P", "m", "g", "r"]},
    "Bhupali": {"aaroh": ["S", "R", "G", "P", "D"], "avroh": ["S", "D", "P", "G", "R"]},
    "Shivaranjani": {"aaroh": ["S", "R", "g", "P", "D"], "avroh": ["S", "D", "P", "g", "R"]},
    "Malkauns": {"aaroh": ["S", "g", "m", "d", "n"], "avroh": ["S", "n", "d", "m", "g"]},
    "Khamaj": {"aaroh": ["S", "G", "m", "P", "D", "N"], "avroh": ["S", "n", "D", "P", "m", "G", "R"]},
    "Bhimpalasi": {"aaroh": ["S", "g", "m", "P", "n"], "avroh": ["S", "n", "D", "P", "m", "g", "R"]},
    "Desh": {"aaroh": ["S", "R", "m", "P", "N"], "avroh": ["S", "n", "D", "P", "m", "G", "R"]},
    "Pahari": {"aaroh": ["S", "R", "G", "P", "D"], "avroh": ["S", "N", "D", "P", "G", "R"]},
    "Ahir Bhairav": {"aaroh": ["S", "r", "G", "m", "P", "D", "n"], "avroh": ["S", "n", "D", "P", "m", "G", "r"]}
}

# --- 2. INTERACTIVE COMPONENT GENERATOR ---
def create_interactive_wheel(aaroh, avroh):
    """Generates an HTML/JS snippet for a single-ring interactive instrument."""
    swaras = ['S', 'r', 'R', 'g', 'G', 'm', 'M', 'P', 'd', 'D', 'n', 'N']
    base_freq = 261.63  # Middle C (Sa)
    
    # CSS styling
    html = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        /* ADDED: transform: translateX(-50px) to shift the whole UI left by exactly one button width */
        .container { position: relative; width: 400px; height: 400px; margin: 0 auto; transform: translateX(-50px); font-family: sans-serif; }
        .ring { position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%); border: 2px dashed #bbb; border-radius: 50%; z-index: 1; pointer-events: none; width: 280px; height: 280px; }
        .btn { 
            position: absolute; transform: translate(-50%, -50%); border-radius: 50%; 
            display: flex; justify-content: center; align-items: center; cursor: pointer; 
            z-index: 2; box-shadow: 0 4px 6px rgba(0,0,0,0.3); 
            transition: transform 0.1s, box-shadow 0.1s, filter 0.1s; user-select: none; 
            -webkit-tap-highlight-color: transparent; 
            width: 50px; height: 50px; border: 2px solid #fff; font-weight: bold; font-size: 18px;
        }
        
        /* GLOW EFFECT */
        .btn:active { 
            transform: translate(-50%, -50%) scale(0.9); 
            box-shadow: 0 0 20px 8px rgba(255, 215, 0, 0.8); 
            filter: brightness(1.2); 
        }
    </style>
    </head>
    <body>
    <div class="container">
        <div class="ring"></div>
    """

    # Generate buttons in a single circle
    for i, note in enumerate(swaras):
        freq = base_freq * (2 ** (i / 12))
        angle = math.radians(i * 30 - 90) # -90 puts 'S' at the top (12 o'clock)
        
        # Single radius for all notes
        r = 140
        cx = 200
        cy = 200
        
        x, y = cx + r * math.cos(angle), cy + r * math.sin(angle)
        
        # Color Logic 
        if note in aaroh and note in avroh:
            bg_color = '#FFD700' # Gold (Both)
            text_color = '#000000' # Black text for contrast
        elif note in aaroh:
            bg_color = '#4CAF50' # Green (Aaroh only)
            text_color = '#FFFFFF' # White text
        elif note in avroh:
            bg_color = '#FF9800' # Orange (Avroh only)
            text_color = '#FFFFFF' # White text
        else:
            bg_color = '#222222' # Black (Not used)
            text_color = '#FFFFFF' # White text
        
        html += f'<div class="btn" style="left:{x}px; top:{y}px; background:{bg_color}; color:{text_color};" onmousedown="playNote({freq})" ontouchstart="playNote({freq})">{note}</div>\n'
        
    html += """
    </div>
    <script>
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        let audioCtx;

        function playNote(freq) {
            if (!audioCtx) audioCtx = new AudioContext(); 
            
            const osc = audioCtx.createOscillator();
            const gainNode = audioCtx.createGain();
            
            osc.type = 'triangle'; 
            osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
            
            osc.connect(gainNode);
            gainNode.connect(audioCtx.destination);
            
            osc.start();
            
            gainNode.gain.setValueAtTime(0, audioCtx.currentTime);
            gainNode.gain.linearRampToValueAtTime(0.8, audioCtx.currentTime + 0.05);
            gainNode.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 1.2);
            
            osc.stop(audioCtx.currentTime + 1.3);
        }
    </script>
    </body>
    </html>
    """
    return html

# --- 3. STREAMLIT APP LAYOUT ---
st.set_page_config(page_title="Play Your Raga", layout="centered")

st.title("🎼 Play & Know Your Raga")

# Legend for the new color scheme
st.markdown("### Color Legend")
col1, col2, col3, col4 = st.columns(4)
col1.markdown("🟡 **Gold:** Both (Aaroh & Avroh)")
col2.markdown("🟢 **Green:** Aaroh only")
col3.markdown("🟠 **Orange:** Avroh only")
col4.markdown("⚫ **Black:** Not in Raga")

st.markdown("---")

tab1, tab2 = st.tabs(["🎹 Play & Explore", "🧠 Guess the Raga"])

with tab1:
    st.subheader("Explore the Scale")
    selected_raga = st.selectbox("Select a Raga:", list(ragas_db.keys()))
    
    raga_data = ragas_db[selected_raga]
    instrument_html = create_interactive_wheel(raga_data["aaroh"], raga_data["avroh"])
    components.html(instrument_html, height=420)

with tab2:
    st.subheader("Ear Training & Visual Quiz")
    st.markdown("Look at the colored scale and play the notes. Can you identify the Raga?")
    
    if "quiz_raga" not in st.session_state:
        st.session_state.quiz_raga = random.choice(list(ragas_db.keys()))
        
    def next_question():
        st.session_state.quiz_raga = random.choice(list(ragas_db.keys()))

    quiz_data = ragas_db[st.session_state.quiz_raga]
    quiz_html = create_interactive_wheel(quiz_data["aaroh"], quiz_data["avroh"])
    components.html(quiz_html, height=420)

    guess = st.selectbox("Which raga is this?", ["Select your guess..."] + list(ragas_db.keys()), key="quiz_select")
    
    if guess != "Select your guess...":
        if guess == st.session_state.quiz_raga:
            st.success(f"Correct! It is Raga {st.session_state.quiz_raga}.")
            st.button("Next Raga", on_click=next_question)
        else:
            st.error("Not quite! Check the colors to see which notes are used ascending vs descending.")
