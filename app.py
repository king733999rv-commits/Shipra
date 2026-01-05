import streamlit as st
import yt_dlp
import os
import json
import datetime

# --- डेटा मैनेजमेंट (ट्रैकर) ---
STATS_FILE = "shipra_stats.json"

def load_stats():
    if not os.path.exists(STATS_FILE):
        return {"total_visits": 0, "total_downloads": 0}
    try:
        with open(STATS_FILE, "r") as f:
            return json.load(f)
    except:
        return {"total_visits": 0, "total_downloads": 0}

def save_stats(stats):
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f, indent=4)

# स्टैट्स लोड करें
stats = load_stats()

# विज़िटर काउंट (सेशन आधारित)
if 'visited' not in st.session_state:
    stats["total_visits"] += 1
    save_stats(stats)
    st.session_state['visited'] = True

# --- एस्थेटिक UI डिज़ाइन ---
st.set_page_config(page_title="Shipra MP3", page_icon="🎵")

st.markdown("""
    <style>
    .main { text-align: center; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #ff4b4b; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎵 Shipra: Universal MP3 Converter")
st.write("सभ्य और सुरक्षित तरीके से किसी भी लिंक को ऑडियो में बदलें।")

# --- डैशबोर्ड ---
col1, col2 = st.columns(2)
col1.metric("कुल विज़िटर्स", stats["total_visits"])
col2.metric("कुल डाउनलोड्स", stats["total_downloads"])

st.divider()

# --- कनवर्टर सेक्शन ---
url = st.text_input("यहाँ वीडियो का लिंक डालें:", placeholder="https://...")

if st.button("MP3 तैयार करें"):
    if url:
        with st.spinner("प्रक्रिया जारी है... कृपया रुकें।"):
            try:
                # फाइल सेटिंग्स
                temp_name = f"Shipra_Audio_{datetime.datetime.now().strftime('%H%M%S')}"
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'outtmpl': f"{temp_name}.%(ext)s",
                    'quiet': True,
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    title = info.get('title', 'Shipra_Song')
                    file_path = f"{temp_name}.mp3"

                if os.path.exists(file_path):
                    with open(file_path, "rb") as f:
                        st.audio(f.read(), format="audio/mp3")
                        st.download_button(
                            label="📥 फाइल डाउनलोड करें",
                            data=f,
                            file_name=f"{title}.mp3",
                            mime="audio/mpeg"
                        )
                    
                    # स्टैट्स अपडेट
                    stats["total_downloads"] += 1
                    save_stats(stats)
                    st.success(f"सफलतापूर्वक कन्वर्ट हुआ: {title}")
                    
                    # सफाई
                    os.remove(file_path)
                    st.rerun()

            except Exception as e:
                st.error("त्रुटि: लिंक सही नहीं है या यह साइट सपोर्टेड नहीं है।")
    else:
        st.warning("कृपया लिंक पेस्ट करें।")

st.divider()
st.caption("© 2026 Shipra | Aesthetic & Secure Design")
